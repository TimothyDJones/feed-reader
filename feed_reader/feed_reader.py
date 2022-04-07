# Standard Libraries
import asyncio
from datetime import datetime
import future
import logging
from pprint import (pformat, pprint)
from random import choice
from time import mktime
import yaml

# Third-party Libaries
from aiohttp import (ClientSession, ClientResponseError)
from bs4 import BeautifulSoup
import feedparser
from pytz import timezone
import validators
import yattag

# Local Libraries


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s|%(levelname)-8s| %(message)s'
DATE_FORMAT = '%G-%m-%d %H:%M:%S'

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)
LOG = logging.getLogger(__name__)

DEFAULT_URLS = [
    "https://hnrss.org/newest",
    "http://xkcd.com/atom.xml",
    "http://feeds.mashable.com/Mashable"
]


__all__ = ["FeedReader"]

class FeedReader(object):
    def __init__(self, urls, full_articles=False, tz="UTC"):
    
        self.logger = LOG
        
        self.urls = urls or DEFAULT_URLS
        self.full_articles = full_articles
        self.tz = timezone(tz)

        self.feed_items = None
        
        self._default_response = {
            "title": "Not Found",
            "description": "Unknown or malformed URL.",
            "last_updated": datetime.utcnow(),
            "items": list()
        }
        
        self._default_url = choice(DEFAULT_URLS)
        
        # Create the event loop.
        self.loop = asyncio.get_event_loop()
        
        self.logger.debug("Feed reader initialized.")

    async def get_feed(self, session, url):
        """
        Retrieve specified URL via asynchronous session.
        This method retrieves "raw" RSS XML to be parsed separately, so
        we return "text" from HTTP response.
        """
        try:
            async with session.get(url, raise_for_status=True) as response:
                return await response.text()
        except ClientResponseError:
            msg = "Unable to connect to URL: {u}".format(u=url)
            self.logger.error(msg)
    
    async def parse_feed(self, url=None, newer_than=None):
        """
        Calls "get_feed()" to get feed data and then parses the content
        returned.
        """
        url = url or self._default_url
        if not validators.url(url):
            return self._default_response
            
        async with ClientSession() as session:
            msg = "Attempting to retrieve and parse '{u}'...".format(u=url)
            self.logger.debug(msg)
            content = await self.get_feed(session=session, url=url)
            
            # Parse content using FeedParser library into 
            # structured data.
            data = feedparser.parse(content)
            last_updated = datetime.fromtimestamp(
                mktime(data.feed.updated_parsed
                    or data.feed.published_parsed
                    or data.feed.date_parsed)
                ).astimezone(self.tz)
            
            feed_result = {
                "title": data.feed.title,
                "description": self.check_attr(data.feed, "description", "Unknown"),
                "last_updated": last_updated,
                "items": list()
            }
            
            
            for entry in data.entries:
#                self.logger.debug("ENTRY: {e}".format(e=pformat(object=entry, indent=2)))
                published = datetime.fromtimestamp(
                    mktime(entry.updated_parsed)
                ).astimezone(self.tz)
#                published = datetime.now()
                if newer_than:
                    if newer_than <= published:
                        continue
                try:
                    feed_result["items"].append(
                        {
                            "id": entry.id,
                            "title": entry.title,
                            "summary": entry.summary,
                            "authors": self.check_attr(entry, "author", "Unknown"),
                            "links": entry.links,
                            "published": published
                        }
                    )
                    msg = "Added entry with id {id}.".format(id=entry.id)
                    self.logger.debug(msg)
                except AttributeError:
                    self.logger.error("Unable to parse feed entry.")
            
            msg = "Feed retrieval and parsing completed for {ft}.".format(
                ft=data.feed.title)
            self.logger.debug(msg)
            
            return (feed_result)

    def get_feeds(self):
        """
        Retrieve *list* of feeds via asynchronous processing.
        """
        feeds = [self.parse_feed(url=feed_url) for feed_url in self.urls]
        future = asyncio.gather(*feeds, return_exceptions=True, loop=self.loop)
        
        self.loop.run_until_complete(future)

        results = [feed for feed in future.result()]
        
        return (results)


    def sort_feed_items(self, sort_key, reverse=True):
        sorted_entries = sorted(self.feed_items, key=lambda x: x.get(sort_key, None))
        if reverse:
            self.feed_items = sorted_entries.reverse()
        else:
            self.feed_items = sorted_entries
    
    @staticmethod
    def check_attr(obj, attr, default=None):
        """
        Checks an object for a given attribute. If found, the value
        of the attribute is returned. Otherwise, the optional default
        value is returned.
        """
        return (getattr(obj, attr) if hasattr(obj, attr) else default)