# Feed Reader

Simple RSS/Atom feed reader built with:
- [Python](https://www.python.org/)
- [FeedParser](https://pythonhosted.org/feedparser/) - a Python module for downloading and parsing syndicated feeds
- [asyncio](https://docs.python.org/3/library/asyncio.html) - a Python library to write concurrent code using the `async/await` syntax
- [Yattag](https://www.yattag.org/) - a Python library for generating HTML or XML in a Pythonic way

Multiple RSS/Atom feeds are retrieved and parsed concurrently. The resulting feed items are written to an HTML file for viewing.


## References
[feed-reader.py](https://github.com/gkbrk/scripts/blob/master/feed-reader.py)
[scraper](https://pastebin.com/RRm7RH6t)