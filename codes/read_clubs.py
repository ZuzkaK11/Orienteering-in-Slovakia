import requests
from bs4 import BeautifulSoup
import subprocess

def parse_clubs(html):
        parsed = BeautifulSoup(html, 'html.parser')
        clubs = parsed.select('table tbody tr')
        for club in clubs:
                elements = club.select('td')
                id = elements[0].get_text()
                subprocess.run(["python", "write_club.py", "https://is.orienteering.sk/clubs/"+str(id)])


def fetch_html(url):
        try:
                response = requests.get(url)
                response.raise_for_status()
                return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None

def main():
        start_url = "https://is.orienteering.sk/clubs"
        html = fetch_html(start_url)
        if html is None:
                return
        parse_clubs(html)


if __name__ == "__main__":
        main()