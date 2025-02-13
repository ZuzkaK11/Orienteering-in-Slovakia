import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import subprocess
import sys
from datetime import datetime

update_runners = []
categories = []
count_categories = []
        

def parse_applications(html, stage, competition_id):
        parsed = BeautifulSoup(html, 'html.parser')
        categories_names = parsed.select('.panel-body a')
        runners_cat = parsed.select('.table-responsive')
        for i in categories_names:
                x = i.get_text().strip()
                if x[-1]=='A' or x[-1]=='E':
                        x=x[:-2]
                x = x.replace(" ","").strip()
                categories.append(x)
        for category in runners_cat:
                runners = category.select('tr')
                for runner in runners[1:]:
                        elements = runner.select('td')
                        apply = elements[stage+3].get_text() 
                        id = elements[1].get_text()
                        if apply=="Áno":
                                update_runners.append(id) 
                count_categories.append(len(runners[1:]))
                
def update_runners_db(conn):
        cursor = conn.cursor() 
        for runner_id in update_runners:
                cursor.execute("SELECT num_competitions FROM runners WHERE reg_number = ?", (runner_id,))
                current_count = cursor.fetchone()
                if current_count!=None:
                    new_count = current_count[0] + 1
                    cursor.execute("UPDATE runners SET num_competitions = ? WHERE reg_number = ?", (new_count, runner_id))
                    conn.commit()
                   
def fill_database_competitions_categories(conn, competition_id):
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO competitions_categories (id) VALUES (?)", (competition_id,))
        conn.commit()
        cursor.execute("PRAGMA table_info(competitions_categories)")
        existing_columns = [column[1] for column in cursor.fetchall()]

        for category, count in zip(categories, count_categories):
                if category in existing_columns:
                        update_query = f"UPDATE competitions_categories SET {category} = ? WHERE id = ?"
                        cursor.execute(update_query, (count, competition_id))
                        conn.commit()


def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
                print("Chyba:", e)
                return None
    

def main():
        start_url = sys.argv[1]         #start_url = "https://is.orienteering.sk/competitions/"+id+"/entries"
        stage = int(sys.argv[3])
        competition_id = int(sys.argv[2])
        html = fetch_html(start_url)
        if html is None:
                return
        parse_applications(html, stage, competition_id)
        conn = sqlite3.connect('orienteering.db')
        update_runners_db(conn)
        fill_database_competitions_categories(conn, competition_id)
        conn.close()

if __name__ == "__main__":
        main()