from bs4 import BeautifulSoup
import requests
NUMBER_LINKS = 100

def grab(link):
    try:
        r  = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")
        linklist = [k.get('href') for k in soup.find_all('a')] # Grab all the hrefs of all the a tags
        linklist = list(filter(lambda x : x != None, linklist)) # Filter out None elements
        linklist = list(filter(lambda x : x.startswith('http'), linklist)) # Filter out weird non-links
        return linklist
    except Exception as e: # Catch any request connection errors (SSLError...)
        return []

url = input("Enter a website to crawl : ")
links = grab(url) # Generate initial list of links to scrape

for l in links:
    newlinks = grab(l)
    for nl in newlinks:
        if nl not in links: links.append(nl)
    if len(links) >= NUMBER_LINKS:
        break

if len(links) < NUMBER_LINKS:
    print('Failed to acquire {} links - got only {}'.format(NUMBER_LINKS, len(links)))
else:
    print(*links[:NUMBER_LINKS], sep = "\n")
