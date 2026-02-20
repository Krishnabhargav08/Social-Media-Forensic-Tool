"""
Analysis Service
Performs sentiment analysis, cyberbullying detection, and fake profile detection
Supports both basic TextBlob analysis and advanced AI analysis
"""

import re
from textblob import TextBlob
from collections import Counter

class AnalysisService:
    """Service for analyzing scraped social media data"""
    
    def __init__(self):
        # Cyberbullying keywords database
        self.cyberbullying_keywords = [
            'stupid', 'idiot', 'hate', 'ugly', 'loser', 'kill yourself',
            'die', 'nobody likes', 'worthless', 'pathetic', 'disgusting',
            'fat', 'dumb', 'retard', 'freak', 'weak', 'failure'
        ]
        
        # Fraud/scam keywords
        self.fraud_keywords = [
            'click here', 'free money', 'double your', 'get rich',
            'investment opportunity', 'guaranteed returns', 'act now',
            'limited time', 'you won', 'claim your prize', 'verify account',
            'urgent action', 'suspended account', 'confirm identity'
        ]
        
        # Advanced AI service (optional)
        self.advanced_ai = None
    
    def analyze_all(self, data_collected):
        """Perform comprehensive analysis on collected data"""
        
        if not data_collected or len(data_collected) == 0:
            return {
                'sentiment': {},
                'cyberbullying': {},
                'fraud_detection': {},
                'fake_profile': {},
                'risk_score': 0
            }
        
        # Get the latest scraped data
        latest_data = data_collected[-1]
        posts = latest_data.get('posts', [])
        metadata = latest_data.get('metadata', {})
        
        # Try advanced AI analysis first
        advanced_analysis = self._try_advanced_ai_analysis(posts)
        
        # Perform traditional analyses
        sentiment_results = self.analyze_sentiment(posts)
        cyberbullying_results = self.detect_cyberbullying(posts)
        fraud_results = self.detect_fraud_patterns(posts)
        fake_profile_results = self.detect_fake_profile(metadata, posts)
        
        # Merge advanced AI results if available
        if advanced_analysis:
            sentiment_results['ai_enhanced'] = True
            sentiment_results['advanced_analysis'] = advanced_analysis
            
            # Enhance scores with AI insights if available
            if 'gpt4_analysis' in advanced_analysis and isinstance(advanced_analysis['gpt4_analysis'], dict):
                gpt4 = advanced_analysis['gpt4_analysis']
                if 'cyberbullying_score' in gpt4:
                    cyberbullying_results['ai_score'] = gpt4['cyberbullying_score']
                if 'fraud_score' in gpt4:
                    fraud_results['ai_score'] = gpt4['fraud_score']
    
    def _try_advanced_ai_analysis(self, posts):
        """Try to use advanced AI analysis if available"""
        try:
            # Lazy load advanced AI service
            if self.advanced_ai is None:
                from services.advanced_ai_service import AdvancedAIService
                self.advanced_ai = AdvancedAIService()
            
            return self.advanced_ai.get_comprehensive_analysis(posts)
        except Exception as e:
            print(f"ℹ️  Advanced AI not available: {e}")
            return None
        
        # Calculate overall risk score (0-100)
        risk_score = self._calculate_risk_score(
            sentiment_results,
            cyberbullying_results,
            fraud_results,
            fake_profile_results
        )
        
        return {
            'sentiment': sentiment_results,
            'cyberbullying': cyberbullying_results,
            'fraud_detection': fraud_results,
            'fake_profile': fake_profile_results,
            'risk_score': risk_score
        }
    
    def analyze_sentiment(self, posts):
        """Analyze sentiment of posts"""
        if not posts:
            return {'overall': 'neutral', 'positive': 0, 'negative': 0, 'neutral': 0}
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for post in posts:
            content = post.get('content', '')
            
            try:
                # Use TextBlob for sentiment analysis
                blob = TextBlob(content)
                polarity = blob.sentiment.polarity
                
                if polarity > 0.1:
                    sentiment = 'positive'
                    positive_count += 1
                elif polarity < -0.1:
                    sentiment = 'negative'
                    negative_count += 1
                else:
                    sentiment = 'neutral'
                    neutral_count += 1
                
                sentiments.append({
                    'post_id': post.get('post_id'),
                    'sentiment': sentiment,
                    'polarity': round(polarity, 3),
                    'subjectivity': round(blob.sentiment.subjectivity, 3)
                })
            except:
                # Fallback to neutral if analysis fails
                sentiments.append({
                    'post_id': post.get('post_id'),
                    'sentiment': 'neutral',
                    'polarity': 0,
                    'subjectivity': 0
                })
        
        # Determine overall sentiment
        total = len(posts)
        if negative_count > positive_count and negative_count > neutral_count:
            overall = 'negative'
        elif positive_count > negative_count and positive_count > neutral_count:
            overall = 'positive'
        else:
            overall = 'neutral'
        
        return {
            'overall': overall,
            'positive_percentage': round((positive_count / total) * 100, 2) if total > 0 else 0,
            'negative_percentage': round((negative_count / total) * 100, 2) if total > 0 else 0,
            'neutral_percentage': round((neutral_count / total) * 100, 2) if total > 0 else 0,
            'detailed_sentiments': sentiments
        }
    
    def detect_cyberbullying(self, posts):
        """Detect cyberbullying patterns"""
        if not posts:
            return {'detected': False, 'confidence': 0, 'incidents': []}
        
        incidents = []
        total_flags = 0
        
        for post in posts:
            content = post.get('content', '').lower()
            matched_keywords = []
            
            for keyword in self.cyberbullying_keywords:
                if keyword in content:
                    matched_keywords.append(keyword)
                    total_flags += 1
            
            if matched_keywords:
                incidents.append({
                    'post_id': post.get('post_id'),
                    'content': post.get('content'),
                    'matched_keywords': matched_keywords,
                    'severity': 'high' if len(matched_keywords) > 2 else 'medium'
                })
        
        detected = len(incidents) > 0
        confidence = min((total_flags / len(posts)) * 100, 100) if posts else 0
        
        return {
            'detected': detected,
            'confidence': round(confidence, 2),
            'incidents_count': len(incidents),
            'total_flags': total_flags,
            'incidents': incidents
        }
    
    def detect_fraud_patterns(self, posts):
        """Detect fraud and scam patterns"""
        if not posts:
            return {'detected': False, 'confidence': 0, 'suspicious_posts': []}
        
        suspicious_posts = []
        total_flags = 0
        
        for post in posts:
            content = post.get('content', '').lower()
            matched_patterns = []
            
            # Check for fraud keywords
            for keyword in self.fraud_keywords:
                if keyword in content:
                    matched_patterns.append(keyword)
                    total_flags += 1
            
            # Check for suspicious patterns
            if re.search(r'https?://', content):  # Contains URLs
                matched_patterns.append('contains_url')
            
            if re.search(r'\$\d+', content):  # Contains money amounts
                matched_patterns.append('money_reference')
            
            if matched_patterns:
                suspicious_posts.append({
                    'post_id': post.get('post_id'),
                    'content': post.get('content'),
                    'patterns': matched_patterns,
                    'risk_level': 'high' if len(matched_patterns) > 3 else 'medium'
                })
        
        detected = len(suspicious_posts) > 0
        confidence = min((total_flags / len(posts)) * 100, 100) if posts else 0
        
        return {
            'detected': detected,
            'confidence': round(confidence, 2),
            'suspicious_count': len(suspicious_posts),
            'total_flags': total_flags,
            'suspicious_posts': suspicious_posts
        }
    
    def detect_fake_profile(self, metadata, posts):
        """Detect potential fake profile indicators"""
        risk_factors = []
        risk_score = 0
        
        # Check account age
        account_age = metadata.get('account_age_days', 0)
        if account_age < 30:
            risk_factors.append('Very new account (< 30 days)')
            risk_score += 25
        elif account_age < 90:
            risk_factors.append('New account (< 90 days)')
            risk_score += 15
        
        # Check follower/following ratio
        followers = metadata.get('followers', 0)
        following = metadata.get('following', 0)
        
        if following > 0:
            ratio = followers / following
            if ratio < 0.1:  # Following way more than followers
                risk_factors.append('Suspicious follower ratio')
                risk_score += 20
        
        if followers < 50:
            risk_factors.append('Very low follower count')
            risk_score += 15
        
        # Check posting patterns
        total_posts = metadata.get('total_posts', 0)
        if total_posts < 5:
            risk_factors.append('Very few posts')
            risk_score += 20
        elif total_posts > 500 and account_age < 180:
            risk_factors.append('Unusual posting frequency')
            risk_score += 15
        
        # Check content diversity
        if posts:
            contents = [post.get('content', '') for post in posts]
            unique_ratio = len(set(contents)) / len(contents)
            if unique_ratio < 0.5:  # Many duplicate posts
                risk_factors.append('High content duplication')
                risk_score += 20
        
        is_fake = risk_score >= 50
        
        return {
            'is_potentially_fake': is_fake,
            'fake_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'account_age_days': account_age,
            'follower_ratio': round(followers / following, 2) if following > 0 else 0
        }
    
    def _calculate_risk_score(self, sentiment, cyberbullying, fraud, fake_profile):
        """Calculate overall risk score (0-100)"""
        score = 0
        
        # Cyberbullying contributes most to risk (0-40 points)
        if cyberbullying['detected']:
            score += min(cyberbullying['confidence'] * 0.4, 40)
        
        # Fraud detection (0-30 points)
        if fraud['detected']:
            score += min(fraud['confidence'] * 0.3, 30)
        
        # Fake profile indicators (0-20 points)
        score += min(fake_profile['fake_score'] * 0.2, 20)
        
        # Negative sentiment (0-10 points)
        if sentiment['overall'] == 'negative':
            score += min(sentiment['negative_percentage'] * 0.1, 10)
        
        return min(round(score, 2), 100)
