import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

years = list(range(1999, 2025))


def parse_competitions(html):
        parsed = BeautifulSoup(html, 'html.parser')
        races = parsed.select('table tbody tr')
        sites = parsed.select('.pagination a')
        for i in range (len(sites)):
            for race in races:
                    
                    elements = race.select('td')
                    date=elements[0].get_text().replace("\t","").strip()
                    name=elements[1].select('a')[0].get_text().replace("\n","").strip()
                    link=elements[1].select('a')[0].get("href")
                    place=elements[2].get_text().strip()
                    type=elements[3].get_text().strip()
                    classification=elements[4].get_text().strip()
                    org=elements[5].get_text().strip()

                    if org=="XOB FBA":
                           org="FBA"
                    info=[date, name, place, type, classification, org]
                    if type=="OB" and (classification=="SRJ" or classification=="MSR"):
                        dates = date.split("-")
                        href = "https://is.orienteering.sk"+link
                        for d_str in dates:
                            d_str = d_str.strip()
                            d = datetime.strptime(d_str, "%d.%m.%Y").date()
                            if d.year < 2018:
                                info[0]=d_str
                                subprocess.run(["python", "write_competition_old.py", href, *info])
                            else:
                                break
                        if d.year >= 2018:
                            subprocess.run(["python", "write_competition.py", href, org])
            next = sites[-1].get("href")
            html = requests.get("https://is.orienteering.sk"+next).text
            parsed = BeautifulSoup(html, 'html.parser')
            races = parsed.select('table tbody tr')
            sites = parsed.select('.pagination a')


def fetch_html(url):
        try:
                response = requests.get(url)
                response.raise_for_status()
                return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None


def main():
        start_url = "https://is.orienteering.sk/competitions/filter"
        for i in years:  
            html = fetch_html(start_url+'/'+str(i)+'/0')
            if html is None:
                return
            parse_competitions(html)


if __name__ == "__main__":
        main()