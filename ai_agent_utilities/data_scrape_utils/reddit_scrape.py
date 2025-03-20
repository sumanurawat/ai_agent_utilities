import praw
import os
import pandas as pd
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import from the module path
from ai_agent_utilities.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

def scrape_reddit(
    subreddit_name='wallstreetbets',
    limit=100,
    sort_by='hot',
    time_filter='all',
    search_query=None,
    include_comments=False,
    comment_limit=0,
    min_score=0,
    exclude_nsfw=True,
    include_fields=None,
    output_file=None,
    return_type='dataframe'
):
    """
    Comprehensive function to scrape Reddit posts with multiple options.
    
    Args:
        subreddit_name (str): Name of the subreddit to scrape
        limit (int): Maximum number of posts to scrape
        sort_by (str): How to sort posts ('new', 'hot', 'top', 'rising', 'controversial')
        time_filter (str): Time filter for 'top' and 'controversial' sorts
            ('all', 'day', 'week', 'month', 'year')
        search_query (str, optional): Search for specific terms within the subreddit
        include_comments (bool): Whether to include comments in the results
        comment_limit (int): Maximum number of comments to include per post (0 for none)
        min_score (int): Minimum score (upvotes) for posts to include
        exclude_nsfw (bool): Whether to exclude NSFW posts
        include_fields (list, optional): Specific post fields to include. If None, includes:
            ['id', 'title', 'score', 'url', 'author', 'created_utc', 'num_comments', 'selftext']
        output_file (str, optional): Path to save CSV output
        return_type (str): Format to return data ('dataframe', 'dict', 'json')
        
    Returns:
        pandas.DataFrame, dict, or str: Scraped posts in the requested format
    """
    # Check if credentials are available
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError("Reddit API credentials not available. Please check your .env file.")

    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="reddit-scraper-bot"
    )
    
    # Default fields to include if none specified
    if include_fields is None:
        include_fields = ['id', 'title', 'score', 'url', 'author', 'created_utc', 
                          'num_comments', 'selftext']
    
    print(f"Scraping up to {limit} posts from r/{subreddit_name} sorted by '{sort_by}'...")
    posts = []
    subreddit = reddit.subreddit(subreddit_name)
    
    # Get submissions based on sort and search criteria
    if search_query:
        submissions = subreddit.search(search_query, sort=sort_by, time_filter=time_filter, limit=limit)
    elif sort_by == 'new':
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
        raise ValueError(f"Invalid sort_by value: {sort_by}")
    
    for post in submissions:
        # Skip NSFW posts if requested
        if exclude_nsfw and post.over_18:
            continue
            
        # Skip posts below minimum score
        if post.score < min_score:
            continue
            
        # Extract requested post data
        post_data = {}
        for field in include_fields:
            # Handle author specially to avoid None errors
            if field == 'author':
                post_data[field] = post.author.name if post.author else '[deleted]'
            # Convert timestamp to readable date
            elif field == 'created_utc':
                timestamp = post.created_utc
                post_data[field] = timestamp
                post_data['created_date'] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                try:
                    post_data[field] = getattr(post, field)
                except AttributeError:
                    post_data[field] = None
        
        # Add comments if requested
        if include_comments and comment_limit > 0:
            comments = []
            post.comments.replace_more(limit=0)  # Only get direct comments
            for comment in list(post.comments)[:comment_limit]:
                comments.append({
                    'id': comment.id,
                    'author': comment.author.name if comment.author else '[deleted]',
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc
                })
            post_data['comments'] = comments
            
        posts.append(post_data)
    
    # Convert to requested return format
    if return_type == 'dict':
        result = posts
    elif return_type == 'json':
        import json
        result = json.dumps(posts)
    else:  # dataframe
        result = pd.DataFrame(posts)
        
        # If comments are included, they're in a nested structure that doesn't work well in a flat DataFrame
        if include_comments and comment_limit > 0:
            # Drop the comments column from the main dataframe
            result_without_comments = result.drop(columns=['comments'])
            
            # Create a separate dataframe for comments with post_id reference
            all_comments = []
            for post in posts:
                post_id = post['id']
                if 'comments' in post:
                    for comment in post['comments']:
                        comment['post_id'] = post_id
                        all_comments.append(comment)
            
            # Return main dataframe and comments dataframe
            if all_comments:
                result = {
                    'posts': result_without_comments,
                    'comments': pd.DataFrame(all_comments)
                }
            else:
                result = result_without_comments
    
    # Save to CSV if output_file is specified
    if output_file and return_type == 'dataframe':
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        if isinstance(result, dict):  # We have posts and comments
            result['posts'].to_csv(output_file, index=False)
            comment_file = output_file.replace('.csv', '_comments.csv')
            result['comments'].to_csv(comment_file, index=False)
            print(f"Saved {len(result['posts'])} posts to {output_file}")
            print(f"Saved {len(result['comments'])} comments to {comment_file}")
        else:
            result.to_csv(output_file, index=False)
            print(f"Saved {len(result)} posts to {output_file}")
    
    return result

def scrape_detailed_posts(
    subreddit_name='wallstreetbets',
    limit=5,
    sort_by='hot',
    time_filter='all',
    search_query=None,
    comment_depth=3,  # How many levels of nested comments to retrieve
    output_file=None,
):
    """
    Get comprehensive information about a small number of Reddit posts,
    including all comments, metadata, and awards.
    
    Args:
        subreddit_name (str): Name of the subreddit to scrape
        limit (int): Maximum number of posts to retrieve (keep small, e.g. 5-10)
        sort_by (str): How to sort posts ('new', 'hot', 'top', 'rising', 'controversial')
        time_filter (str): Time filter for 'top' and 'controversial' sorts
        search_query (str, optional): Search for specific terms within the subreddit
        comment_depth (int): How many levels of nested comments to retrieve
        output_file (str, optional): Path to save JSON output
        
    Returns:
        dict: Detailed post data including all available information
    """
    # Check if credentials are available
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError("Reddit API credentials not available. Please check your .env file.")

    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="reddit-detailed-scraper"
    )
    
    print(f"Scraping {limit} detailed posts from r/{subreddit_name} sorted by '{sort_by}'...")
    detailed_posts = []
    subreddit = reddit.subreddit(subreddit_name)
    
    # Get submissions based on sort and search criteria
    if search_query:
        submissions = subreddit.search(search_query, sort=sort_by, time_filter=time_filter, limit=limit)
    elif sort_by == 'new':
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
        raise ValueError(f"Invalid sort_by value: {sort_by}")
    
    # Process each submission to get detailed info
    for submission in submissions:
        # Get all post attributes dynamically
        post_data = {}
        
        # Get all post attributes that don't require API calls
        for attr in dir(submission):
            # Skip private/special methods and attributes
            if attr.startswith('_') or attr in ('subreddit', 'author', 'comments'):
                continue
                
            # Skip methods (we only want data attributes)
            if callable(getattr(submission, attr)):
                continue
                
            try:
                value = getattr(submission, attr)
                # Convert non-serializable objects to strings
                if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    value = str(value)
                post_data[attr] = value
            except:
                # Skip any attributes that cause errors
                continue
        
        # Add special handling for common attributes
        post_data['author'] = submission.author.name if submission.author else '[deleted]'
        post_data['subreddit'] = submission.subreddit.display_name
        post_data['permalink'] = f"https://www.reddit.com{submission.permalink}"
        
        # Convert created_utc to readable date
        if 'created_utc' in post_data:
            timestamp = post_data['created_utc']
            post_data['created_date'] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Handle awards
        try:
            post_data['awards'] = [
                {
                    'name': award['name'],
                    'description': award['description'],
                    'count': award['count']
                }
                for award in submission.all_awardings
            ]
        except:
            post_data['awards'] = []
        
        # Process comments
        post_data['comments'] = []
        
        # Get all comments, replacing "more comments" links
        submission.comments.replace_more(limit=None)
        
        # Function to recursively get comment info
        def get_comment_info(comment, depth=0):
            if depth > comment_depth:
                return None
                
            comment_data = {
                'id': comment.id,
                'author': comment.author.name if comment.author else '[deleted]',
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc,
                'created_date': datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'permalink': f"https://www.reddit.com{comment.permalink}",
                'replies': []
            }
            
            # Add awards to comments
            try:
                comment_data['awards'] = [
                    {
                        'name': award['name'],
                        'description': award['description'],
                        'count': award['count']
                    }
                    for award in comment.all_awardings
                ]
            except:
                comment_data['awards'] = []
            
            # Process replies recursively
            for reply in comment.replies:
                reply_data = get_comment_info(reply, depth + 1)
                if reply_data:
                    comment_data['replies'].append(reply_data)
                    
            return comment_data
        
        # Process top-level comments
        for comment in submission.comments:
            comment_data = get_comment_info(comment)
            if comment_data:
                post_data['comments'].append(comment_data)
        
        detailed_posts.append(post_data)
    
    # Save to JSON if output_file is specified
    if output_file:
        import json
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(detailed_posts, f, indent=4)
        print(f"Saved {len(detailed_posts)} detailed posts to {output_file}")
    
    return detailed_posts

if __name__ == "__main__":
    # When run directly, make sure we can import from parent package
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs/reddit', exist_ok=True)
    
    """
    USAGE EXAMPLES
    
    This section demonstrates various ways to use the scrape_reddit function.
    Each example shows different parameters and use cases.
    
    Available parameters:
    --------------------
    subreddit_name: str (default='wallstreetbets')
        The name of the subreddit to scrape (without the r/ prefix)
    
    limit: int (default=100)
        Maximum number of posts to retrieve
    
    sort_by: str (default='hot')
        How to sort the posts. Options:
        - 'hot': Currently popular posts
        - 'new': Most recent posts
        - 'top': Highest scored posts (use with time_filter)
        - 'rising': Posts gaining popularity
        - 'controversial': Posts with mixed votes
    
    time_filter: str (default='all')
        Time period for 'top' and 'controversial' sorts. Options:
        - 'all': All time
        - 'day': Past 24 hours
        - 'week': Past week
        - 'month': Past month
        - 'year': Past year
    
    search_query: str (default=None)
        Search for specific terms within the subreddit
    
    include_comments: bool (default=False)
        Whether to include comments with each post
    
    comment_limit: int (default=0)
        Maximum number of comments to retrieve per post (0 for none)
    
    min_score: int (default=0)
        Minimum score (upvotes) for posts to include
    
    exclude_nsfw: bool (default=True)
        Whether to exclude NSFW posts
    
    include_fields: list (default=None)
        Specific post fields to include. If None, includes:
        ['id', 'title', 'score', 'url', 'author', 'created_utc', 
         'num_comments', 'selftext']
    
    output_file: str (default=None)
        Path to save CSV output. If None, doesn't save to file
    
    return_type: str (default='dataframe')
        Format to return data:
        - 'dataframe': pandas DataFrame (default)
        - 'dict': Python dictionary
        - 'json': JSON string
    """
    
    # Example 1: Basic usage - Get top posts from r/investing
    print("\n=== Example 1: Basic scraping ===")
    basic_result = scrape_reddit(
        subreddit_name='investing',
        limit=5,
        sort_by='top', # choices: 'hot', 'new', 'top', 'rising', 'controversial'
        time_filter='week', # choices: 'all', 'day', 'week', 'month', 'year'
        output_file='outputs/reddit/investing_basic.csv'
    )
    
    # Example 2: Advanced usage - Search for Tesla-related posts with comments
    print("\n=== Example 2: Search with comments ===")
    tesla_result = scrape_reddit(
        subreddit_name='investing',
        search_query='tesla',
        sort_by='top',
        time_filter='month',
        include_comments=True,
        comment_limit=3,
        min_score=10,
        output_file='outputs/reddit/tesla_investing.csv'
    )
    
    # Example 3: Custom fields and JSON output
    print("\n=== Example 3: Custom fields and JSON output ===")
    custom_fields = ['id', 'title', 'score', 'num_comments', 'created_utc']
    json_result = scrape_reddit(
        subreddit_name='wallstreetbets',
        limit=3,
        include_fields=custom_fields,
        return_type='json'
    )

    # Pretty print and save JSON to file
    import json
    # Convert back to Python object to pretty print
    json_data = json.loads(json_result)
    # Pretty format with indentation
    pretty_json = json.dumps(json_data, indent=4)
    # Save to file
    json_output_file = 'outputs/reddit/wallstreetbets_custom.json'
    with open(json_output_file, 'w') as f:
        f.write(pretty_json)
    print(f"Saved pretty-printed JSON result to {json_output_file}")
    
    print("\nAll examples completed. Check the 'outputs/reddit' directory for files.")
    
    # Example 4: Get detailed information with all comments
    print("\n=== Example 4: Detailed post information with full comments ===")
    detailed_posts = scrape_detailed_posts(
        subreddit_name='explainlikeimfive',  # This subreddit often has detailed discussions
        limit=2,  # Keep it small since we're getting ALL comments
        sort_by='top',
        time_filter='week',
        comment_depth=3,  # Get 3 levels of nested comments
        output_file='outputs/reddit/detailed_posts.json'
    )
    print(f"Retrieved {len(detailed_posts)} detailed posts with complete comment trees")
