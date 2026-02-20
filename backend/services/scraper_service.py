"""
Data Scraper Service
Collects publicly available social media data
Supports both simulated mode (default) and real API integration (optional)
"""

import random
from datetime import datetime, timedelta
from flask import current_app

class ScraperService:
    """Service for scraping social media data"""
    
    def __init__(self):
        self.supported_platforms = ['twitter', 'instagram', 'facebook', 'linkedin', 'reddit']
        self.use_real_scraping = False
        self.twitter_client = None
        self.instagram_loader = None
        self.reddit_client = None
    
    def _initialize_apis(self):
        """Initialize API clients if credentials are available"""
        try:
            self.use_real_scraping = current_app.config.get('USE_REAL_SCRAPING', False)
            
            if self.use_real_scraping:
                # Try to import and initialize Twitter API
                if current_app.config.get('TWITTER_BEARER_TOKEN'):
                    try:
                        import tweepy
                        self.twitter_client = tweepy.Client(
                            bearer_token=current_app.config['TWITTER_BEARER_TOKEN']
                        )
                        print("✅ Twitter API initialized")
                    except ImportError:
                        print("⚠️  tweepy not installed. Run: pip install tweepy")
                    except Exception as e:
                        print(f"⚠️  Twitter API error: {e}")
                
                # Try to import and initialize Instagram API
                if current_app.config.get('INSTAGRAM_ACCESS_TOKEN'):
                    try:
                        import instaloader
                        self.instagram_loader = instaloader.Instaloader()
                        print("✅ Instagram API initialized")
                    except ImportError:
                        print("⚠️  instaloader not installed. Run: pip install instaloader")
                    except Exception as e:
                        print(f"⚠️  Instagram API error: {e}")
                
                # Try to import and initialize Reddit API
                if current_app.config.get('REDDIT_CLIENT_ID'):
                    try:
                        import praw
                        self.reddit_client = praw.Reddit(
                            client_id=current_app.config['REDDIT_CLIENT_ID'],
                            client_secret=current_app.config['REDDIT_CLIENT_SECRET'],
                            user_agent=current_app.config.get('REDDIT_USER_AGENT', 'ForensicTool/1.0')
                        )
                        print("✅ Reddit API initialized")
                    except ImportError:
                        print("⚠️  praw not installed. Run: pip install praw")
                    except Exception as e:
                        print(f"⚠️  Reddit API error: {e}")
        except Exception as e:
            print(f"⚠️  API initialization error: {e}")
    
    def scrape_profile(self, platform, username):
        """
        Scrape user profile data
        Uses real APIs if available, otherwise falls back to simulated data
        """
        
        if platform.lower() not in self.supported_platforms:
            raise ValueError(f"Platform {platform} not supported")
        
        # Initialize APIs on first use
        if self.use_real_scraping is False:
            self._initialize_apis()
        
        # Try real scraping first
        if self.use_real_scraping:
            try:
                if platform.lower() == 'twitter' and self.twitter_client:
                    return self._scrape_twitter_real(username)
                elif platform.lower() == 'instagram' and self.instagram_loader:
                    return self._scrape_instagram_real(username)
                elif platform.lower() == 'reddit' and self.reddit_client:
                    return self._scrape_reddit_real(username)
            except Exception as e:
                print(f"⚠️  Real scraping failed for {platform}: {e}, falling back to simulated mode")
        
        # Fall back to simulated data
        return self._scrape_simulated(platform, username)
        # Fall back to simulated data
        return self._scrape_simulated(platform, username)
    
    def _scrape_twitter_real(self, username):
        """Scrape real Twitter data using API"""
        try:
            # Get user by username
            user = self.twitter_client.get_user(username=username, user_fields=['created_at', 'description', 'location', 'public_metrics', 'verified'])
            user_data = user.data
            
            # Get user tweets
            tweets = self.twitter_client.get_users_tweets(
                id=user_data.id,
                max_results=20,
                tweet_fields=['created_at', 'public_metrics', 'entities']
            )
            
            posts = []
            if tweets.data:
                for tweet in tweets.data:
                    posts.append({
                        'post_id': tweet.id,
                        'content': tweet.text,
                        'timestamp': tweet.created_at.isoformat() if tweet.created_at else datetime.utcnow().isoformat(),
                        'likes': tweet.public_metrics['like_count'],
                        'comments': tweet.public_metrics['reply_count'],
                        'shares': tweet.public_metrics['retweet_count'],
                        'hashtags': [tag['tag'] for tag in tweet.entities.get('hashtags', [])] if hasattr(tweet, 'entities') else []
                    })
            
            return {
                'username': username,
                'platform': 'twitter',
                'scraped_at': datetime.utcnow().isoformat(),
                'profile': {
                    'display_name': user_data.name,
                    'bio': user_data.description or '',
                    'location': user_data.location or 'Unknown',
                    'verified': user_data.verified or False,
                    'joined_date': user_data.created_at.isoformat() if user_data.created_at else None
                },
                'posts': posts,
                'metadata': {
                    'total_posts': user_data.public_metrics['tweet_count'],
                    'followers': user_data.public_metrics['followers_count'],
                    'following': user_data.public_metrics['following_count'],
                    'account_age_days': (datetime.utcnow() - user_data.created_at).days if user_data.created_at else 0
                }
            }
        except Exception as e:
            raise Exception(f"Twitter scraping failed: {str(e)}")
    
    def _scrape_instagram_real(self, username):
        """Scrape real Instagram data using Instaloader"""
        try:
            profile = instaloader.Profile.from_username(self.instagram_loader.context, username)
            
            posts = []
            for post in profile.get_posts():
                if len(posts) >= 20:
                    break
                posts.append({
                    'post_id': post.shortcode,
                    'content': post.caption or '',
                    'timestamp': post.date.isoformat(),
                    'likes': post.likes,
                    'comments': post.comments,
                    'shares': 0,
                    'hashtags': post.caption_hashtags if post.caption else []
                })
            
            return {
                'username': username,
                'platform': 'instagram',
                'scraped_at': datetime.utcnow().isoformat(),
                'profile': {
                    'display_name': profile.full_name or username,
                    'bio': profile.biography or '',
                    'location': 'Unknown',
                    'verified': profile.is_verified,
                    'joined_date': None
                },
                'posts': posts,
                'metadata': {
                    'total_posts': profile.mediacount,
                    'followers': profile.followers,
                    'following': profile.followees,
                    'account_age_days': 0
                }
            }
        except Exception as e:
            raise Exception(f"Instagram scraping failed: {str(e)}")
    
    def _scrape_reddit_real(self, username):
        """Scrape real Reddit data using PRAW"""
        try:
            redditor = self.reddit_client.redditor(username)
            
            posts = []
            for submission in redditor.submissions.new(limit=20):
                posts.append({
                    'post_id': submission.id,
                    'content': submission.title + '\\n' + (submission.selftext or ''),
                    'timestamp': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'likes': submission.score,
                    'comments': submission.num_comments,
                    'shares': 0,
                    'hashtags': [],
                    'subreddit': f"r/{submission.subreddit.display_name}",
                    'awards': submission.total_awards_received
                })
            
            return {
                'username': username,
                'platform': 'reddit',
                'scraped_at': datetime.utcnow().isoformat(),
                'profile': {
                    'display_name': redditor.name,
                    'bio': '',
                    'location': 'Unknown',
                    'verified': redditor.is_gold or redditor.is_mod,
                    'joined_date': datetime.fromtimestamp(redditor.created_utc).isoformat()
                },
                'posts': posts,
                'metadata': {
                    'total_posts': len(list(redditor.submissions.new(limit=None))),
                    'followers': 0,
                    'following': 0,
                    'account_age_days': (datetime.utcnow() - datetime.fromtimestamp(redditor.created_utc)).days
                }
            }
        except Exception as e:
            raise Exception(f"Reddit scraping failed: {str(e)}")
    
    def _scrape_simulated(self, platform, username):
        """Generate simulated profile data (original behavior)"""
        profile_data = {
            'username': username,
            'platform': platform,
            'scraped_at': datetime.utcnow().isoformat(),
            'profile': self._generate_profile_data(username, platform),
            'posts': self._generate_posts_data(username, platform),
            'metadata': {
                'total_posts': random.randint(10, 500),
                'followers': random.randint(100, 10000),
                'following': random.randint(50, 5000),
                'account_age_days': random.randint(30, 3650)
            }
        }
        
        return profile_data
    
    def _generate_profile_data(self, username, platform):
        """Generate simulated profile data"""
        return {
            'display_name': username.title(),
            'bio': f"Sample bio for {username}",
            'location': random.choice(['New York', 'London', 'Tokyo', 'Unknown']),
            'verified': random.choice([True, False]),
            'profile_image_url': f"https://example.com/{username}.jpg",
            'joined_date': (datetime.utcnow() - timedelta(days=random.randint(30, 1000))).isoformat()
        }
    
    def _generate_posts_data(self, username, platform):
        """Generate simulated posts data"""
        posts = []
        
        # Sample post templates for different risk levels
        safe_posts = [
            "Just had an amazing day!",
            "Check out this new product",
            "Happy to share my thoughts",
            "Great experience today",
            "TIL something interesting today" if platform == 'reddit' else "Sharing my experience",
            "AMA: I work in tech" if platform == 'reddit' else "Working on new projects"
        ]
        
        suspicious_posts = [
            "Click here for free money!",
            "I can double your investment in 24 hours",
            "You won a prize! Click this link",
            "Get rich quick with this method",
            "Upvote this for free karma!" if platform == 'reddit' else "Follow for follow!"
        ]
        
        cyberbullying_posts = [
            "You're so stupid",
            "Nobody likes you",
            "You should just quit",
            "Everyone is laughing at you"
        ]
        
        # Mix different types of posts
        num_posts = random.randint(5, 15)
        
        for i in range(num_posts):
            post_type = random.choices(
                ['safe', 'suspicious', 'cyberbullying'],
                weights=[0.7, 0.2, 0.1]
            )[0]
            
            if post_type == 'safe':
                content = random.choice(safe_posts)
            elif post_type == 'suspicious':
                content = random.choice(suspicious_posts)
            else:
                content = random.choice(cyberbullying_posts)
            
            post = {
                'post_id': f"{platform}_{i}_{random.randint(1000, 9999)}",
                'content': content,
                'timestamp': (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
                'likes': random.randint(0, 500) if platform != 'reddit' else random.randint(0, 10000),  # Reddit upvotes can be higher
                'comments': random.randint(0, 100),
                'shares': random.randint(0, 50) if platform != 'reddit' else 0,  # Reddit doesn't have shares
                'hashtags': [f"#{word}" for word in content.split()[:2]] if platform != 'reddit' else [],
                'subreddit': f"r/{random.choice(['technology', 'askreddit', 'pics', 'news', 'science'])}" if platform == 'reddit' else None,
                'awards': random.randint(0, 5) if platform == 'reddit' else None
            }
            
            posts.append(post)
        
        return posts
    
    def scrape_specific_content(self, platform, content_id):
        """Scrape specific content (post, comment, etc.)"""
        # Simulated specific content scraping
        return {
            'content_id': content_id,
            'platform': platform,
            'scraped_at': datetime.utcnow().isoformat(),
            'content': "Sample content",
            'author': "sample_user",
            'timestamp': datetime.utcnow().isoformat()
        }
