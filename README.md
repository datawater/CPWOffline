# CPWOffline
Badly scraped [chess programming wiki](https://chessprogramming.org) for offline use

Scraping was done at July 13 2024 12:34AM GMT+4 Time. (1721680489 Seconds after epoch)

### Why
I was going on a 6 hour train ride without internet access.

### How
A very simple and bad 100 LOC multi-threaded scraper was written in python using requests and bs4. It inputs an article list and dumps the articles into the current directory. It also downloads images and links them. It has some quality of life features, like not downloading files if it already sees them.

The resulting scrape is about 270MBs in size, 162MBs which of are images

Python script usage:
```
python3 export.py [ARTICLE_LIST_FILENAME]
```

### TODOs
- [ ] Add proper flag parsing to the script