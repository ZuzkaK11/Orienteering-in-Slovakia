import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import subprocess
import sys
from datetime import datetime


stages_info=[]

def parse_competition_info(html):
        parsed = BeautifulSoup(html, 'html.parser')
        info = parsed.select('.panel.panel-default')[0]
        stages = parsed.select('.panel.panel-default')[1]
        
        if len(info.select(".col-md-8"))==0:
                info = parsed.select('.panel.panel-default')[1]
                stages = parsed.select('.panel.panel-default')[2]
        stage = stages.select('tr')
        for row in stage[1:]:
                element = row.select('td')
                stage_info=[]
                for x in element:
                        stage_info.append(x.get_text())
                stages_info.append(stage_info)

        i = info.select(".col-md-8")
        id = i[0].get_text()
        place = i[2].get_text().replace("\n","").strip()
        org = i[5].get_text().replace("\n","").strip()
        for i in stages_info:
                i.insert(0, int(id))
                i.append(place)
                i.append(org)
        
        
def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None
        
def fill_database_competitions(conn, org):
        cursor = conn.cursor()
        query_select = "SELECT name FROM competitions WHERE event_id = ? and name = ?"
        query = "INSERT INTO competitions (event_id, name, date, classification, runners, place, org) VALUES ( ?, ?, ?, ?, ?, ?, ?)"
        stages = 0
        for x in stages_info:
                stages+=1
                competition_id = int(x[0])
                competition_name = x[1]
                competition_date = x[2]
                competition_type = x[3]
                x[-1]=org
                competition_date = datetime.strptime(competition_date, "%d.%m.%Y").date()
                x[2]=competition_date
                if competition_date <= datetime.today().date() and "tafety" not in competition_type:
                        cursor.execute(query_select, (competition_id, competition_name,))
                        existing_competition = cursor.fetchone()
                        if not existing_competition:
                                cursor.execute(query, x)
                                conn.commit()
                                last_row_id = cursor.lastrowid
                                subprocess.run(["python", "write_competition_entries.py", "https://is.orienteering.sk/competitions/"+str(competition_id)+'/entries', str(last_row_id), str(stages)])
                                
        

def main():
        start_url = sys.argv[1]         #start_url = "https://is.orienteering.sk/competitions/"+id
        org = sys.argv[2]
        html = fetch_html(start_url)
        if html is None:
                return
        parse_competition_info(html)
        conn = sqlite3.connect('orienteering.db')
        fill_database_competitions(conn, org)
        conn.close()



if __name__ == "__main__":
        main()