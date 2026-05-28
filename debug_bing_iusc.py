import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
query = 'cat'
url = f'https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2'
resp = requests.get(url, headers=headers, timeout=20)
print('status', resp.status_code)
text = resp.text
soup = BeautifulSoup(text, 'html.parser')
items = soup.select('a.iusc')
print('iusc count', len(items))
for i, item in enumerate(items[:20]):
    m_text = item.get('m')
    print('item', i, 'm exists', bool(m_text))
    if m_text:
        try:
            data = json.loads(m_text)
            print('  image', data.get('murl'))
            print('  thumb', data.get('turl'))
            print('  page', data.get('purl'))
        except Exception as e:
            print('  json error', e)
