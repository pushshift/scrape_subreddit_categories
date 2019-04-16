#!/usr/bin/env python3

import bs4
from bs4 import BeautifulSoup
import requests
import sys


def get_content(url,params=None):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url,params=params,headers=headers)
    if r.status_code == 200:
        return r.content

def get_section_name(node):

    if node.find('strong'):
        try:
            section_name = node.strong.em.contents[0]
        except:
            section_name = node.strong.contents[0]
    elif node.find('em'):
        section_name = node.em.contents[0]
    else:
        section_name = node.contents[0]
    try:
        return section_name
    except:
        print(node)
        sys.exit()

def process_node(node):

    current_level = 1
    section_name = get_section_name(node)

    if section_name == 'NSFW (Porn)':
        return

    categories.append(section_name)

    while True:

        node = node.find_next()
        if node is None:
            return
        if node.name.startswith('h') and node.name[1].isdigit():
            next_level = int(node.name[1])
            if next_level == 1:
                categories[:] = []
                return
            elif next_level > current_level:
                section_name = get_section_name(node)
                categories.append(section_name)
                current_level = next_level
            elif next_level == current_level:
                del categories[-1]
                section_name = get_section_name(node)
                categories.append(section_name)
            elif next_level < current_level:
                remove_length = (current_level - next_level) + 1
                del categories[-remove_length:]
                section_name = get_section_name(node)
                categories.append(section_name)
                current_level = next_level

        if node.name == 'a' and not node.has_attr('class'):
            subreddit = node.contents[0]
            if type(subreddit) is not bs4.element.NavigableString or not subreddit.startswith('/r/'):
                continue
            print(",".join(categories),node.contents[0],sep=",")


for page in ['https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits','https://www.reddit.com/r/ListOfSubreddits/wiki/games50k','https://www.reddit.com/r/ListOfSubreddits/wiki/nsfw']:

    html = get_content(page)
    soup = BeautifulSoup(html,'html.parser')
    sections = soup.find_all("h1",attrs={'class': None})
    categories = []

    for section in sections:
        process_node(section)

