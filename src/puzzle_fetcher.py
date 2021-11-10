import requests
from bs4 import BeautifulSoup

def fetch() -> str:
    'Return today’s letters, grouped by side, with groups separated by spaces (upo xts eil ncy)'
    response = requests.get('https://www.nytimes.com/puzzles/letter-boxed')
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    game_data_script = [script.text for script in scripts if script.text.startswith('window.gameData')][0]
    search = '"sides":'
    sides_start = game_data_script.index(search) + len(search) + 1
    sides_data = game_data_script[sides_start:sides_start + 23]   # "UPO","XTS","EIL","NCY"
    return sides_data.replace('"', '').replace(',', ' ').lower()  # upo xts eil ncy

if __name__ == '__main__':
    print(fetch())
