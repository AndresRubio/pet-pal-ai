import requests
import xml.etree.ElementTree as ET
import os

excluded_urls = ['https://www.zooplus.com/']


def extract_urls_from_sitemap(sitemap_url=os.getenv('SITEMAP_URL')):
    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)
    urls = [child[0].text for child in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')]
    return urls


def extract_urls_from_local():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, 'urls.txt'), 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    return lines
