#!/usr/bin/env python3

import bs4
from bs4 import BeautifulSoup
import requests



def get_content(url,params=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url,params=params,headers=headers)
    if r.status_code == 200:
        return r.content

html = get_content("https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits")
soup = BeautifulSoup(html,'html.parser')
sections = soup.find_all(["h1","h2","h3","h4"])

for section in sections:

    if section.find('strong'):
        section_name = section.strong.contents[0]
    elif section.find('em'):
        section_name = section.em.contents[0]
    else:
        continue

    node = section

    while True:
        node = node.find_next()
        if node.name.startswith('h'): break
        if node.name == 'a' and not node.has_attr('class'):
            subreddit = node.contents[0]
            if type(subreddit) is not bs4.element.NavigableString or not subreddit.startswith('/r/'):
                continue
            print(section_name,subreddit[3:],sep=",")

