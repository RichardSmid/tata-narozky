from bs4 import BeautifulSoup
import requests

html = requests.get('https://www.youtube.com/watch?v=Z1RJmh_OqeA').text
soup = BeautifulSoup(html, "lxml")

links = soup.find_all("link")
author = "NONE"

for link in links:
    if '"name"' in str(link):
        author = str(link)[15:]
        author = author[:author.find('"')]
        break

name = soup.find_all("title")[0].text

print(author, name[:len(name)-10])