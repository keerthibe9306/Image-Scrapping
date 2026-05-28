import re
import requests
from urllib.parse import quote_plus

query = 'cat'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}
url = f'https://duckduckgo.com/?q={quote_plus(query)}&iax=images&ia=images'
print('GET', url)
resp = requests.get(url, headers=headers, timeout=20)
print('status', resp.status_code)
print('cookies', resp.cookies.get_dict())
text = resp.text
m = re.search(r'vqd=\'([0-9-]+)\'', text)
if not m:
    m = re.search(r'vqd=\"([0-9-]+)\"', text)
print('vqd-match', bool(m), m.group(1) if m else None)
if m:
    vqd = m.group(1)
    api_url = f'https://duckduckgo.com/i.js?l=us-en&o=json&q={quote_plus(query)}&vqd={vqd}'
    print('API', api_url)
    headers2 = headers.copy()
    headers2.update({'Referer': 'https://duckduckgo.com/', 'Accept': 'application/json, text/javascript, */*; q=0.01'})
    resp2 = requests.get(api_url, headers=headers2, cookies=resp.cookies, timeout=20)
    print('api status', resp2.status_code)
    print('api text head', resp2.text[:1000])
else:
    print('no vqd token')
