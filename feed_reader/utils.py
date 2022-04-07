# Standard Libraries
import datetime
import os

# Third-party Libaries
from bs4 import BeautifulSoup

def check_attr(obj, attr, default=None):
    """
    Checks an object for a given attribute. If found, the value
    of the attribute is returned. Otherwise, the optional default
    value is returned.
    """
    return (getattr(obj, attr) if hasattr(obj, attr) else default)

def clean_html(html):
    """
    Strips HTML content of tags/formatting and returns plain text.
    """
    soup = BeautifulSoup(html, "html.parser")
    return (soup.get_text())

def save_html_to_file(html_content):
    """
    Save HTML content to file
    """
    script_path = os.path.abspath(__file__)
    file_name = os.path.join(
        os.path.dirname(os.path.dirname(script_path)), "data",
        "feed_{dt}.html".format(dt=datetime.now().strftime("%Y_%m_%d")))
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)