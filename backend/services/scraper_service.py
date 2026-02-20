"""
Data Scraper Service
Collects publicly available social media data
NOTE: This is a simulated scraper for demonstration. 
In production, use official APIs (Twitter API, Instagram API, etc.)
"""

import random
from datetime import datetime, timedelta

class ScraperService:
    """Service for scraping social media data"""
    
    def __init__(self):
        self.supported_platforms = ['twitter', 'instagram', 'facebook', 'linkedin']
    
    def scrape_profile(self, platform, username):
        """
        Scrape user profile data
        NOTE: This is simulated data for demonstration purposes.
        In production, integrate with official social media APIs.
        """
        
        if platform.lower() not in self.supported_platforms:
            raise ValueError(f"Platform {platform} not supported")
        
        # Simulated profile data
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
            "Great experience today"
        ]
        
        suspicious_posts = [
            "Click here for free money!",
            "I can double your investment in 24 hours",
            "You won a prize! Click this link",
            "Get rich quick with this method"
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
                'likes': random.randint(0, 500),
                'comments': random.randint(0, 100),
                'shares': random.randint(0, 50),
                'hashtags': [f"#{word}" for word in content.split()[:2]]
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
