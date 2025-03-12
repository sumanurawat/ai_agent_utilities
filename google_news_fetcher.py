from GoogleNews import GoogleNews
import pandas as pd

def fetch_news_by_topic(topic, start_date=None, end_date=None, language='en'):
    googlenews = GoogleNews(lang=language)
    if start_date and end_date:
        googlenews.set_time_range(start_date, end_date)
    googlenews.search(topic)
    result = googlenews.result()
    return pd.DataFrame(result)

def fetch_news_by_date(date, language='en'):
    googlenews = GoogleNews(lang=language)
    googlenews.set_time_range(date, date)
    googlenews.search('')
    result = googlenews.result()
    return pd.DataFrame(result)

def fetch_news_by_keyword(keyword, start_date=None, end_date=None, language='en'):
    googlenews = GoogleNews(lang=language)
    if start_date and end_date:
        googlenews.set_time_range(start_date, end_date)
    googlenews.search(keyword)
    result = googlenews.result()
    return pd.DataFrame(result)

def fetch_news_by_location(location, start_date=None, end_date=None, language='en'):
    googlenews = GoogleNews(lang=language)
    if start_date and end_date:
        googlenews.set_time_range(start_date, end_date)
    googlenews.search(location)
    result = googlenews.result()
    return pd.DataFrame(result)

def fetch_news_by_source(source, start_date=None, end_date=None, language='en'):
    googlenews = GoogleNews(lang=language)
    if start_date and end_date:
        googlenews.set_time_range(start_date, end_date)
    googlenews.search(source)
    result = googlenews.result()
    return pd.DataFrame(result)

def fetch_news_by_language(language, start_date=None, end_date=None):
    googlenews = GoogleNews(lang=language)
    if start_date and end_date:
        googlenews.set_time_range(start_date, end_date)
    googlenews.search('')
    result = googlenews.result()
    return pd.DataFrame(result)