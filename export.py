import requests
import os.path
import sys
from pathlib import Path
from multiprocessing import Pool
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def download_image(image_url: str) -> str:
    parsed = urlparse(image_url)

    image_url_built = "https://"

    if parsed.netloc == '':
        image_url_built += "chessprogramming.org"
    else:
        image_url_built += parsed.netloc

    image_url_built += parsed.path

    path = Path("." + parsed.path)
    if os.path.exists(path):
        return str(path)

    try:
        path.parent.mkdir(parents = True, exist_ok = True)
    except:
        return image_url_built

    print("downloading image", image_url_built)

    r = requests.get(image_url_built, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'})

    if r.status_code != 200:
        print("Couldn't download image: '{}'. Status code: {}.".format(image_url, r.status_code))
        return "";

    file = open(path, "wb")
    file.write(r.content)

    return str(path)

def process_article(article_raw: str):
    article = article_raw.strip()
    print("Downloading article \"" + article + "\"")

    if os.path.exists(article + ".html"):
        return

    article_url = "https://chessprogramming.org/index.php?title=" + article.replace(" ", "_") + "&printable=yes"
    article_request = requests.get(article_url)

    if article_request.status_code != 200:
        return

    html = article_request.text

    soup = BeautifulSoup(html, "html.parser")
    for image in soup.find_all('img'):
        if not image.has_attr('src'):
           continue

        path = download_image(image.attrs['src'])
        image.attrs['src'] = path.removeprefix("./")

    for link in soup.find_all("a"):
        if not link.has_attr('href'):
            continue

        if link.attrs['href'].startswith("https"):
            continue

        prefix_removed = link.attrs['href'].removeprefix("/").replace("_", " ")

        if prefix_removed[0] == '#':
            prefix_removed
        elif '#' in prefix_removed:
            prefix_removed = prefix_removed.replace("#", ".html#")
        else:
            prefix_removed += ".html"

        link.attrs['href'] = prefix_removed

    file = open(article + ".html", "w")
    file.write(str(soup))

def main():
    argc = len(sys.argv)
    if argc != 2:
        print("Expected input filename. Usage: python3 export.py [FILENAME]")
        return

    if not os.path.exists(sys.argv[1]):
        print("Input file doesnt exist. Usage: python3 export.py [FILENAME]")
        return

    articles_list = open(sys.argv[1], "r").readlines()

    with Pool(16) as p:
        p.map(process_article, articles_list)

if __name__ == "__main__":
    main()
