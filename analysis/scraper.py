import requests
import bs4 as bs

resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})

def get_spy_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    
    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        if ticker == 'FB':
            ticker = 'META'

        tickers.append(ticker)

    return tickers

