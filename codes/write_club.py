import requests
from bs4 import BeautifulSoup
import sqlite3
import sys


clubs_data=[]       #shortcut, name, members, city
runners_data=[]     #reg_number, name, age, gender, club

def parse_club_info(html):
        parsed = BeautifulSoup(html, 'html.parser')
        club = parsed.select('.panel-body')[0]
        info=club.select('.row')
        club_data=[]
        for i in info:
            info2=i.select('.col-md-8')
            data=info2[0].get_text()
            data = data.replace("\t","").strip()
            club_data.append(data)
        clubs_data.append([club_data[1], club_data[7], club_data[4], club_data[10]])


def parse_club_runners(html):
        parsed = BeautifulSoup(html, 'html.parser')
        section = parsed.select('.panel.panel-default.panel-registrations')
        table = section[0].select('.table-responsive')
        for rows in table:
                rows = rows.select('tbody tr')
                for row in rows:
                        elements = row.select('td')
                        reg_number = elements[1].get_text()
                        club = reg_number[:3]
                        link = elements[0].select('a')
                        name = link[0].get_text()
                        if len(link)==1:
                                
                                continue
                        gender, date = None, None
                        info = link[1].get('data-content')
                        items = info.split('<br>')
                       
                        for item in items:
                                if "Pohlavie" in item:
                                        gender = item.split(':')[-1].strip()
                                        gender = gender.replace("</b>","").strip()
                                if "Dátum" in item:
                                        date = item.split(':')[-1].strip()
                                        date = date.replace("</b>","").strip()
                                        year = 2024-int(date[-4:])
                                        break
                        runners_data.append([reg_number, name, year, gender, club, 0])
           
        
        
def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None
        
def fill_database_clubs(conn):
        cursor = conn.cursor()
        query="INSERT INTO clubs (shortcut, name, members, city) VALUES (?, ?, ?, ?)"
        for x in clubs_data:
                cursor.execute(query, x)
                conn.commit()

def fill_database_runners(conn):
        cursor = conn.cursor()
        query="INSERT INTO runners (reg_number, name, age, gender, club, num_competitions) VALUES (?, ?, ?, ?, ?, ?)"
        for x in runners_data:               
                cursor.execute(query, x)
                conn.commit()

def main():
        start_url = sys.argv[1]                 #start_url = "https://is.orienteering.sk/clubs/"+id
        html = fetch_html(start_url)
        if html is None:
                return
        parse_club_info(html)
        parse_club_runners(html)
        conn = sqlite3.connect('orienteering.db')
        fill_database_clubs(conn)
        fill_database_runners(conn)
        conn.close()



if __name__ == "__main__":
        main()