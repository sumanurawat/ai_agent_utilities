import praw
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import from the module path - this should work regardless of how the file is run
from ai_agent_utilities.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

def scrape_reddit_posts(
    subreddit_name='wallstreetbets', 
    limit=1000, 
    sort_by='new',
    time_filter='all',
    output_file=None
):
    """
    Scrape posts from specified subreddit with configurable sorting
    
    Args:
        subreddit_name (str): Name of the subreddit to scrape
        limit (int): Number of posts to scrape
        sort_by (str): How to sort posts. Options:
            - 'new': Most recent posts
            - 'hot': Currently popular posts
            - 'top': Highest voted posts (use with time_filter)
            - 'rising': Posts currently gaining popularity
            - 'controversial': Posts with mixed votes
        time_filter (str): Time filter for 'top' and 'controversial' sorts. Options:
            - 'all': All time
            - 'day': Past 24 hours
            - 'week': Past week
            - 'month': Past month
            - 'year': Past year
        output_file (str, optional): Path to save CSV output
        
    Returns:
        pandas.DataFrame: DataFrame containing scraped posts
    """
    # Check if credentials are available
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError("Error: Reddit API credentials not available. Please check your .env file.")

    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="reddit-post-scraper"
    )
    
    print(f"Scraping up to {limit} posts from r/{subreddit_name} sorted by '{sort_by}'...")
    posts = []
    subreddit = reddit.subreddit(subreddit_name)
    
    # Get posts based on sorting method
    if sort_by == 'new':
        submissions = subreddit.new(limit=limit)
    elif sort_by == 'hot':
        submissions = subreddit.hot(limit=limit)
    elif sort_by == 'top':
        submissions = subreddit.top(time_filter=time_filter, limit=limit)
    elif sort_by == 'rising':
        submissions = subreddit.rising(limit=limit)
    elif sort_by == 'controversial':
        submissions = subreddit.controversial(time_filter=time_filter, limit=limit)
    else:
        raise ValueError(f"Invalid sort_by value: {sort_by}. Valid options are: new, hot, top, rising, controversial")
    
    for post in submissions:
        posts.append({
            'title': post.title,
            'score': post.score,
            'created_utc': post.created_utc
        })
    
    df = pd.DataFrame(posts)
    
    # Save to CSV if output_file is specified
    if output_file:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Successfully scraped {len(posts)} posts and saved to {output_file}")
    
    return df

if __name__ == "__main__":
    # When run directly, make sure we can import from parent package
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape Reddit posts')
    parser.add_argument('--subreddit', type=str, default='wallstreetbets', help='Subreddit to scrape')
    parser.add_argument('--limit', type=int, default=1000, help='Number of posts to scrape')
    parser.add_argument('--sort', type=str, default='hot', choices=['new', 'hot', 'top', 'rising', 'controversial'], 
                       help='How to sort posts')
    parser.add_argument('--time', type=str, default='all', choices=['all', 'day', 'week', 'month', 'year'],
                       help='Time filter for top/controversial sorts')
    parser.add_argument('--output', type=str, default='outputs/reddit_posts.csv', help='Output file path')
    
    args = parser.parse_args()
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Scrape posts
    scrape_reddit_posts(
        subreddit_name=args.subreddit,
        limit=args.limit,
        sort_by=args.sort,
        time_filter=args.time,
        output_file=args.output
    )