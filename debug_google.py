import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
query = 'cat'
url = f'https://www.google.com/search?q={quote_plus(query)}&tbm=isch'
response = requests.get(url, headers=headers, timeout=20)
print('status', response.status_code)
print('len', len(response.text))
print('--- body snippet ---')
print(response.text[:2000])
print('--- img tags ---')
print(len(BeautifulSoup(response.text, 'html.parser').find_all('img')))
