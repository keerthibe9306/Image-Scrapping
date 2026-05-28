import requests
from urllib.parse import quote_plus

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}
query = 'cat'
url = f'https://duckduckgo.com/?q={quote_plus(query)}&iax=images&ia=images'
print('url', url)
response = requests.get(url, headers=headers, timeout=20)
print('status', response.status_code)
print('body len', len(response.text))
print(response.text[:2000])
