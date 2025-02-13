import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import subprocess
import sys
from datetime import datetime

def parse_competition_info(html):
        parsed = BeautifulSoup(html, 'html.parser')
        info = parsed.select('.panel.panel-default')[0]
        i = info.select(".col-md-8")
        id = i[0].get_text()
        return id
        
        
def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None
        
def fill_database_competitions(conn, id, info):
        cursor = conn.cursor()
        query = "INSERT INTO competitions (event_id, name, date, classification, runners, place, org) VALUES ( ?, ?, ?, ?, ?, ?, ?)"
        date = info[0]
        name = info[1]
        place = info[2]
        name_lower=name.lower()
        if "nočn" in name_lower:
                classification="Nočný OB"
        elif "stredn" in name_lower:
                classification="Stredná trať"
        elif "dlh" in name_lower:
                classification="Dlhá trať"
        elif "šprint" in name_lower:
                classification="Šprint"
        elif "skráten" in name_lower:
                classification="Skrátená trať"
        else:
                classification=""

        org = info[5]
        date = datetime.strptime(date, "%d.%m.%Y").date()
        cursor.execute(query, (id, name, date, classification, 0, place, org,))
        conn.commit()
        
                                
def main():
        start_url = sys.argv[1]
        info = sys.argv[2:]
        html = fetch_html(start_url)
        if html is None:
                return
        id = parse_competition_info(html)
        conn = sqlite3.connect('orienteering.db')
        fill_database_competitions(conn, id, info)
        conn.close()


if __name__ == "__main__":
        main()