"""
Advanced AI Analysis Service
Provides intelligent analysis using OpenAI GPT-4 or HuggingFace transformers
Falls back to basic TextBlob analysis if APIs are not available
"""

from flask import current_app
from textblob import TextBlob
import json

class AdvancedAIService:
    """Service for advanced AI-powered analysis"""
    
    def __init__(self):
        self.use_advanced_ai = False
        self.openai_client = None
        self.sentiment_pipeline = None
        self.toxicity_pipeline = None
    
    def _initialize_ai(self):
        """Initialize AI models if available"""
        try:
            self.use_advanced_ai = current_app.config.get('USE_ADVANCED_AI', False)
            
            if self.use_advanced_ai:
                # Try to initialize OpenAI
                openai_key = current_app.config.get('OPENAI_API_KEY')
                if openai_key:
                    try:
                        import openai
                        openai.api_key = openai_key
                        self.openai_client = openai
                        print("✅ OpenAI GPT-4 initialized")
                    except ImportError:
                        print("⚠️  openai not installed. Run: pip install openai")
                    except Exception as e:
                        print(f"⚠️  OpenAI initialization error: {e}")
                
                # Try to initialize HuggingFace transformers
                try:
                    from transformers import pipeline
                    self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
                    self.toxicity_pipeline = pipeline("text-classification", model="unitary/toxic-bert")
                    print("✅ HuggingFace transformers initialized")
                except ImportError:
                    print("⚠️  transformers not installed. Run: pip install transformers torch")
                except Exception as e:
                    print(f"⚠️  Transformers initialization error: {e}")
        except Exception as e:
            print(f"⚠️  AI initialization error: {e}")
    
    def analyze_with_gpt4(self, posts_data):
        """Analyze posts using GPT-4"""
        if not self.openai_client:
            return None
        
        try:
            # Prepare posts summary
            posts_text = "\n\n".join([f"Post {i+1}: {post.get('content', '')}" for i, post in enumerate(posts_data[:10])])
            
            prompt = f"""Analyze these social media posts and provide a detailed forensic analysis in JSON format:

Posts:
{posts_text}

Provide analysis with:
1. Overall sentiment (positive/negative/neutral)
2. Cyberbullying indicators (score 0-100, patterns detected)
3. Fraud/scam indicators (score 0-100, red flags)
4. Mental health concerns (score 0-100, warning signs)
5. Risk assessment (low/medium/high/critical)
6. Key findings and recommendations

Return valid JSON only."""

            response = self.openai_client.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a forensic social media analyst. Provide detailed, accurate analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                return json.loads(result)
            except:
                # If not valid JSON, return as text
                return {"gpt4_analysis": result}
                
        except Exception as e:
            print(f"⚠️  GPT-4 analysis failed: {e}")
            return None
    
    def analyze_with_transformers(self, posts_data):
        """Analyze posts using HuggingFace transformers"""
        if not self.sentiment_pipeline:
            return None
        
        try:
            results = {
                'sentiments': [],
                'toxicity_scores': [],
                'risk_indicators': []
            }
            
            for post in posts_data[:20]:
                content = post.get('content', '')
                
                if not content:
                    continue
                
                # Sentiment analysis
                sentiment = self.sentiment_pipeline(content[:512])[0]  # Truncate to 512 chars
                results['sentiments'].append({
                    'label': sentiment['label'],
                    'score': sentiment['score']
                })
                
                # Toxicity detection
                if self.toxicity_pipeline:
                    toxicity = self.toxicity_pipeline(content[:512])[0]
                    results['toxicity_scores'].append({
                        'label': toxicity['label'],
                        'score': toxicity['score']
                    })
            
            # Calculate aggregates
            positive_count = sum(1 for s in results['sentiments'] if s['label'] == 'POSITIVE')
            negative_count = sum(1 for s in results['sentiments'] if s['label'] == 'NEGATIVE')
            total = len(results['sentiments'])
            
            toxic_count = sum(1 for t in results['toxicity_scores'] if t['label'] == 'toxic' and t['score'] > 0.5)
            
            return {
                'sentiment_summary': {
                    'positive_percentage': round((positive_count / total * 100) if total > 0 else 0, 2),
                    'negative_percentage': round((negative_count / total * 100) if total > 0 else 0, 2),
                    'neutral_percentage': round(((total - positive_count - negative_count) / total * 100) if total > 0 else 0, 2)
                },
                'toxicity_summary': {
                    'toxic_posts': toxic_count,
                    'toxic_percentage': round((toxic_count / total * 100) if total > 0 else 0, 2)
                },
                'detailed_results': results
            }
            
        except Exception as e:
            print(f"⚠️  Transformers analysis failed: {e}")
            return None
    
    def get_comprehensive_analysis(self, posts_data):
        """Get comprehensive analysis using best available AI"""
        
        # Initialize AI on first use
        if self.use_advanced_ai is False:
            self._initialize_ai()
        
        analysis_results = {}
        
        # Try GPT-4 first (most comprehensive)
        if self.openai_client:
            gpt4_results = self.analyze_with_gpt4(posts_data)
            if gpt4_results:
                analysis_results['gpt4_analysis'] = gpt4_results
                analysis_results['ai_provider'] = 'OpenAI GPT-4'
        
        # Try HuggingFace transformers
        if self.sentiment_pipeline:
            transformer_results = self.analyze_with_transformers(posts_data)
            if transformer_results:
                analysis_results['transformer_analysis'] = transformer_results
                if 'ai_provider' not in analysis_results:
                    analysis_results['ai_provider'] = 'HuggingFace Transformers'
        
        # If no advanced AI available, return None to fall back to basic analysis
        if not analysis_results:
            return None
        
        return analysis_results
