import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}
query = 'cat'
url = f'https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2'
print('url', url)
response = requests.get(url, headers=headers, timeout=20)
print('status', response.status_code)
text = response.text
print('len', len(text))
print('first snippet')
print(text[:1200].replace('\n','\\n'))
print('--- soup imgs ---')
soup = BeautifulSoup(text, 'html.parser')
img_tags = soup.find_all('img')
print('img count', len(img_tags))
for i, tag in enumerate(img_tags[:30]):
    print(i, tag.get('src'), tag.get('data-src'), tag.get('data-thumburl'), tag.get('data-fallback'))
