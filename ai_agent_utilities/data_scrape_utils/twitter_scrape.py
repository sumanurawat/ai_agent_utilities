import pandas as pd
import os
import datetime
import json
from dotenv import load_dotenv
import ntscraper
import time  # Import the time module

# Load environment variables
load_dotenv()

# Create scraper object
scraper = ntscraper.Nitter()

def retry_operation(operation, max_retries=3):
    """Simple retry mechanism for unstable API calls"""
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                print(f"Attempt {attempt+1} failed: {e}. Retrying...")
                time.sleep(2)  # Add a delay between retries
            else:
                raise  # Re-raise the last exception if all retries failed

def scrape_twitter(
    query,
    limit=100,
    since=None,
    until=None,
    include_replies=False,
    min_likes=0,
    min_retweets=0,
    exclude_retweets=False,
    language=None,
    output_file=None,
    return_type='dataframe'
):
    """
    Scrape Twitter posts based on search query and filters
    (Same docstring as before)
    """
    global scraper

    if since:
        query += f" since:{since}"
    if until:
        query += f" until:{until}"
    if language:
        query += f" lang:{language}"
    if exclude_retweets and "-filter:retweets" not in query:
        query += " -filter:retweets"
    if not include_replies and "-filter:replies" not in query:
        query += " -filter:replies"

    print(f"Scraping up to {limit} tweets for query: {query}")

    try:
        result = retry_operation(lambda: scraper.get_tweets(query, number=limit))
        raw_tweets = result.get("tweets", [])  # Use .get() to handle missing key
    except Exception as e:
        print(f"Error during scraping: {e}")
        return [] if return_type == 'dict' else pd.DataFrame() if return_type == 'dataframe' else "[]"

    tweets = []
    for tweet in raw_tweets:
        likes = int(tweet.get("likes", 0))
        retweets = int(tweet.get("retweets", 0))

        if likes < min_likes or retweets < min_retweets:
            continue

        tweet_data = {
            'id': tweet.get("tweet_id", ""),
            'content': tweet.get("text", ""),
            'user': tweet.get("user", {}).get("username", ""),
            'display_name': tweet.get("user", {}).get("name", ""),
            'url': f'https://twitter.com/{tweet.get("user", {}).get("username", "")}/status/{tweet.get("tweet_id", "")}',
            'like_count': likes,
            'retweet_count': retweets,
            'reply_count': int(tweet.get("replies", 0)),
            'date': tweet.get("date", ""),
            'language': tweet.get("language", "")
        }

        if "media" in tweet and tweet["media"]:
            media_urls = [media.get("url") for media in tweet["media"] if "url" in media]  # More concise list comprehension
            if media_urls:
                tweet_data['media_urls'] = media_urls

        tweets.append(tweet_data)

    if return_type == 'dict':
        result = tweets
    elif return_type == 'json':
        result = json.dumps(tweets, default=str)
    else:
        result = pd.DataFrame(tweets)

    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        if output_file.endswith('.csv') and return_type != 'json':
            (result if isinstance(result, pd.DataFrame) else pd.DataFrame(tweets)).to_csv(output_file, index=False)
        else:
            with open(output_file, 'w') as f:
                f.write(result if return_type == 'json' else json.dumps(tweets, indent=4, default=str))
        print(f"Saved {len(tweets)} tweets to {output_file}")

    return result

def scrape_user_timeline(
    username,
    limit=100,
    exclude_replies=False,
    exclude_retweets=False,
    min_likes=0,
    output_file=None,
    return_type='dataframe'
):
    """
    Scrape tweets from a specific user's timeline
    (Same docstring as before)
    """
    global scraper

    print(f"Scraping up to {limit} tweets from user: {username}")

    query = f"from:{username}"
    if exclude_retweets:
        query += " -filter:retweets"
    if exclude_replies:
        query += " -filter:replies"

    try:
        result = retry_operation(lambda: scraper.get_tweets(query, number=limit))
        raw_tweets = result.get("tweets", [])  # Use .get() to handle missing key
    except Exception as e:
        print(f"Error during scraping: {e}")
        return [] if return_type == 'dict' else pd.DataFrame() if return_type == 'dataframe' else "[]"

    tweets = []
    for tweet in raw_tweets:
        likes = int(tweet.get("likes", 0))
        if likes < min_likes:
            continue

        tweet_data = {
            'id': tweet.get("tweet_id", ""),
            'content': tweet.get("text", ""),
            'user': username,
            'display_name': tweet.get("user", {}).get("name", username),
            'url': f'https://twitter.com/{username}/status/{tweet.get("tweet_id", "")}',
            'like_count': likes,
            'retweet_count': int(tweet.get("retweets", 0)),
            'reply_count': int(tweet.get("replies", 0)),
            'date': tweet.get("date", ""),
        }

        if "media" in tweet and tweet["media"]:
            media_urls = [media.get("url") for media in tweet["media"] if "url" in media]
            if media_urls:
                tweet_data['media_urls'] = media_urls

        tweets.append(tweet_data)

    if return_type == 'dict':
        result = tweets
    elif return_type == 'json':
        result = json.dumps(tweets, default=str)
    else:
        result = pd.DataFrame(tweets)

    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        if output_file.endswith('.csv') and return_type != 'json':
            (result if isinstance(result, pd.DataFrame) else pd.DataFrame(tweets)).to_csv(output_file, index=False)
        else:
            with open(output_file, 'w') as f:
                f.write(result if return_type == 'json' else json.dumps(tweets, indent=4, default=str))
        print(f"Saved {len(tweets)} tweets to {output_file}")

    return result

def scrape_detailed_tweet(
    tweet_id=None,
    tweet_url=None,
    output_file=None,
    return_type='dict'
):
    """
    Get information about a specific tweet.
    (Same docstring as before)
    """
    if not tweet_id and not tweet_url:
        raise ValueError("Either tweet_id or tweet_url must be provided")

    if tweet_url and not tweet_id:
        try:
            tweet_id = tweet_url.split("/status/")[1].split("?")[0]
        except:
            raise ValueError(f"Could not extract tweet ID from URL: {tweet_url}")

    global scraper

    try:
        print(f"Retrieving tweet with ID: {tweet_id}")

        # Fallback: Use tweet ID as a search query.  This is the most reliable method.
        search_query = f"url:{tweet_id}"
        result = retry_operation(lambda: scraper.get_tweets(search_query, number=1))
        if not result or "tweets" not in result or not result["tweets"]:
            raise ValueError(f"Could not find tweet with ID: {tweet_id}")
        tweet = result["tweets"][0]  # Access the first (and only) tweet directly

        tweet_data = {
            'id': tweet.get("tweet_id", ""),
            'content': tweet.get("text", ""),
            'user': tweet.get("user", {}).get("username", ""),
            'display_name': tweet.get("user", {}).get("name", ""),
            'url': f'https://twitter.com/{tweet.get("user", {}).get("username", "")}/status/{tweet_id}',
            'like_count': int(tweet.get("likes", 0)),
            'retweet_count': int(tweet.get("retweets", 0)),
            'reply_count': int(tweet.get("replies", 0)),
            'date': tweet.get("date", "")
        }

        if "media" in tweet and tweet["media"]:
            media_urls = [media.get("url") for media in tweet["media"] if "url" in media]
            if media_urls:
                tweet_data['media_urls'] = media_urls

    except Exception as e:
        print(f"Error retrieving tweet: {e}")
        return {} if return_type == 'dict' else "{}"

    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(tweet_data, f, indent=4, default=str)
        print(f"Saved tweet data to {output_file}")

    return tweet_data if return_type == 'dict' else json.dumps(tweet_data, default=str)

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    os.makedirs('outputs/twitter', exist_ok=True)

    # Example 1: Basic search query with date range
    print("\n=== Example 1: Basic search query ===")
    basic_result = scrape_twitter(
        query="$GME",
        limit=50,
        since="2024-01-01",
        until="2024-05-31",
        language="en",
        output_file="outputs/twitter/twitter_gme_basic.csv"
    )

    # Example 2: User timeline scraping
    print("\n=== Example 2: User timeline ===")
    user_tweets = scrape_user_timeline(
        username="elonmusk",
        limit=20,
        exclude_replies=True,
        exclude_retweets=True,
        output_file="outputs/twitter/twitter_elonmusk.csv"
    )

    # Example 3: High-engagement tweets about AI
    print("\n=== Example 3: High-engagement tweets ===")
    ai_tweets = scrape_twitter(
        query="artificial intelligence",
        limit=30,
        min_likes=1000,
        min_retweets=100,
        output_file="outputs/twitter/twitter_ai_trending.json",
        return_type="json"
    )

    # Example 4: Get a specific tweet
    print("\n=== Example 4: Get a specific tweet ===")
    try:
        tweet_result = scrape_detailed_tweet(
            tweet_url="https://twitter.com/elonmusk/status/1585841080431321088",
            output_file="outputs/twitter/specific_tweet.json"
        )
        print(f"Retrieved tweet from {tweet_result.get('user', 'unknown')}")
    except Exception as e:
        print(f"Error retrieving specific tweet: {e}")

    print("\nAll examples completed. Check the 'outputs/twitter' directory for files.")