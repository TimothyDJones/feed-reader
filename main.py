# Standard Libraries
from pprint import (pformat, pprint)

# Third-party Libaries

# Local Libraries
from feed_reader.feed_reader import (FeedReader)

if __name__ == "__main__":
    urls = [
        "https://jvns.ca/atom.xml",
        "http://www.reddit.com/r/python/.rss"
    ]

    fr = FeedReader(urls=urls)
    items = fr.get_feeds()
    # for item in items:
    #     print("{i}".format(i=pformat(object=item, indent=2)))

    print(fr.generate_html(items))