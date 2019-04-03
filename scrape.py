from requests import get
from contextlib import closing
from html.parser import HTMLParser

class SimpleHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="div":
            print(attrs)

def simple_get(url):
    with closing(get(url, stream=True)) as resp:
        return str(resp.content)

if __name__ == "__main__":
    content = simple_get("http://www.puzzles.com/products/rushhour/RHfromMarkRiedel/Jam.html?2")
    parser = SimpleHTMLParser()
    parser.feed(content)
