from datetime import datetime
from flask import Flask, render_template, g
import sqlite3
import pandas as pd
import re
import json
import numpy as np

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('orienteering.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    clubs = g.db.execute('SELECT shortcut, name FROM clubs').fetchall()
    city_coordinates=fetch_coordinates()
    club_ratios=count_ratios()
    club_activity = fetch_club_activity()
    gender_data = fetch_gender_distribution()
    competition_classification, total_comp =  fetch_competition_classification()
    favourite_competition = fetch_fav_comp()
    regress = regression()
    age_regress = age_regression()
    club_members = fetch_club_members()
    club_competitions = fetch_club_comp()
    average_age, violin_data = fetch_age_distribution()
    club_colors = fetch_club_colors()
    category = fetch_comp_categories()

    return render_template('main.html', club_colors=club_colors, data_category=category, average_age=average_age, violin_data=violin_data, clubs=clubs, age_regress=age_regress, data_regression=regress, favourite_competition=favourite_competition, competition_classification=competition_classification, gender_data=gender_data, club_activity=club_activity, club_ratios=club_ratios, club_competitions=club_competitions, club_members=club_members, city_coordinates=city_coordinates)

def fetch_club_colors():
    club_shortcuts = g.db.execute('SELECT shortcut FROM clubs').fetchall()
    #colors = ['#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5', '#ad494a']
    colors = ['#000075', '#17becf', '#4363d8', '#E72929',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', 
        '#aec7e8', '#ff7f0e', '#808000', '7077A1', '#3cb44b', '#ff9896', '#c5b0d5',
        '#42d4f4', '#f7b6d2','#ffe119' , '#9edae5' ,'#A67B5B',
        '#8A2BE2']
    
    club_colors = {}
    for i, shortcut in enumerate(club_shortcuts):
        club_colors[shortcut[0]] = colors[i % len(colors)] 
    return club_colors


def fetch_coordinates():
    club_info = g.db.execute("SELECT shortcut, city, members  FROM clubs").fetchall()
    pattern = r'\b\d{5}\b\s(.*)$'
    city_coordinates=[]
    for shortcut, city, members in club_info:
        if re.search(pattern, city)==None:
            city="Stupava"
        else:
            city = re.search(pattern, city).group(1)
        if '-' in city:
            city=city.split('-')[0].strip()
        city_info = g.db.execute("SELECT lat, lng FROM cities WHERE city = ?", (city,)).fetchone()
        if city_info:
            city_coordinates.append((city, city_info[0], city_info[1], members, shortcut))

    return city_coordinates

def count_ratios():
    club_info = g.db.execute('SELECT club, COUNT(*) FROM runners GROUP BY club').fetchall()
    competitions_per_club = g.db.execute("SELECT org, COUNT(*) FROM competitions WHERE strftime('%Y', date) > '2017' GROUP BY org").fetchall()
    club_competitions = dict(competitions_per_club)

    club_ratios = [['Club', 'Members per Competition']]
    for club, count in club_info:
        competitions = club_competitions.get(club, 0)
        ratio = round(count / (competitions/7), 1) if competitions > 0 else 0
        club_ratios.append([club, ratio])
    ratios_sorted = sorted(club_ratios[1:], key=lambda x: x[1], reverse=False)

    return [['Club', 'Members per Competition']] + ratios_sorted


def fetch_club_activity():
    cursor = g.db.execute("""
        SELECT club, COUNT(DISTINCT reg_number) AS num_runners,
               SUM(num_competitions) / 7.0 AS avg_competitions_per_year
        FROM runners
        GROUP BY club
    """)
    data = cursor.fetchall()
    club_activity = []
    for club, num_runners, avg_competitions_per_year in data:
        if num_runners > 0:
            avg_activity_per_runner = avg_competitions_per_year / num_runners
            club_activity.append([club, avg_activity_per_runner])
    club_activity_sorted = sorted(club_activity, key=lambda x: x[1])
    club_activity_sorted.insert(0, ['Club', 'Average Competitions per Runner'])

    return club_activity_sorted


def fetch_gender_distribution():
    result = g.db.execute("""
        SELECT club,
               SUM(CASE WHEN gender = 'Muž' THEN 1 ELSE 0 END) AS male_count,
               SUM(CASE WHEN gender = 'Žena' THEN 1 ELSE 0 END) AS female_count
        FROM runners
        GROUP BY club;
    """).fetchall()
    if not result:
        return [['Club', 'Female', 'Male', 'Overall Female', 'Overall Male']]

    df = pd.DataFrame(result, columns=['club', 'male_count', 'female_count'])

    df['total'] = df['male_count'] + df['female_count']
    df['male_percentage'] = (df['male_count'] / df['total']) * 100
    df['female_percentage'] = (df['female_count'] / df['total']) * 100
    df_sorted = df.sort_values(by='female_percentage', ascending=True)

    total_males = df['male_count'].sum()
    total_females = df['female_count'].sum()
    total_runners = total_males + total_females
    overall_male_percentage = (total_males / total_runners) * 100
    overall_female_percentage = (total_females / total_runners) * 100

    gender_data = [['Club', 'Female', 'Male', 'Overall Female', 'Overall Male']]
    for _, row in df_sorted.iterrows():
        gender_data.append([
            row['club'],
            row['female_percentage'],
            row['male_percentage'],
            overall_female_percentage,
            overall_male_percentage
        ])

    return gender_data


def fetch_fav_comp():
    classification_counts =g.db.execute( '''
    SELECT classification, AVG(runners) AS avg_runners
    FROM competitions
    WHERE strftime('%Y', date) > '2017'
    GROUP BY classification
    ORDER BY avg_runners DESC
    ''').fetchall()
    return classification_counts


def regression():
    club_colors = fetch_club_colors()
    competitions = g.db.execute("SELECT date, runners, org, name FROM competitions WHERE strftime('%Y', date) > '2017' ORDER BY date")

    df = pd.DataFrame(competitions, columns=['date', 'runners', 'org', 'name'])
    data = [['Date (Month-Day)', 'Number of Runners', 'Organizer', {'role': 'style'}]]
    organizer_colors = {} 

    for organizer in df['org'].unique():
        organizer_colors[organizer] = club_colors[organizer]

    for _, row in df.iterrows():
        color = organizer_colors[row['org']]
        data.append([row['date'], row['runners'], row['org'], color, row['name']])
    data_json = json.dumps(data)

    return data_json

def age_regression():
    age =g.db.execute("SELECT age, num_competitions, name, club FROM runners").fetchall()
    df = pd.DataFrame(age, columns=['Age', 'Number of Competitions', 'Name', 'Club'])
    data_json = df.to_json(orient='values')
    return data_json

def fetch_club_members():
    club_runners = g.db.execute('SELECT club, COUNT(*) FROM runners GROUP BY club ORDER BY COUNT(*) DESC').fetchall()
    club_members = [['Club', 'Count']] + [[club, count] for club, count in club_runners]
    return club_members

def fetch_club_comp():
    club_comp = g.db.execute("SELECT org, COUNT(*) FROM competitions WHERE strftime('%Y', date) > '2017' GROUP BY org ORDER BY COUNT(*) DESC").fetchall()
    club_competitions = [['Club', 'Count']] + [[org, count] for org, count in club_comp]
    return club_competitions

def fetch_comp_categories(comp_id=None):
    if comp_id is None:
        rows = g.db.execute("SELECT * FROM competitions_categories").fetchall()
    else:
        rows = g.db.execute("SELECT * FROM competitions_categories WHERE id = ?", (comp_id,)).fetchall()
    category_data = dict()
    columns = g.db.execute("PRAGMA table_info(competitions_categories)")
    categories = [row[1] for row in columns.fetchall()][1:]  
    category_data = {category: 0 for category in categories}
    for row in rows:
        for cat, count in zip(categories, row[1:]):
            if count is None:
                count = 0
            category_data[cat] += count
    total_rows = len(rows)
    category_data_normalized = {cat: count / total_rows for cat, count in category_data.items()}
    return category_data_normalized



####CLUB FUNCTIONS
@app.route('/club/<club_id>')
def club(club_id):
    club_data = g.db.execute('SELECT name, members, shortcut FROM clubs WHERE shortcut = ?', (club_id,)).fetchone()
    if club_data:
        competitions = g.db.execute("SELECT * FROM competitions WHERE strftime('%Y', date) > '2017' AND org = ? ORDER BY date DESC", (club_id,)).fetchall()
        average_age, violin_data = fetch_age_distribution(club_id)
        chart_data, total_competitions = fetch_competition_classification(club_id)
        gender_counts = g.db.execute('SELECT gender, COUNT(*) FROM runners WHERE club = ? GROUP BY gender', (club_id,)).fetchall()        
        return render_template('club.html', total_competitions = total_competitions, competitions=competitions, club_data=club_data, average_age=average_age, violin_data=violin_data, bar_data=chart_data, gender_counts=gender_counts)

    else:
        return "Club not found"


def fetch_age_distribution(club_id=None):
    if club_id==None:
        age_distribution = g.db.execute('SELECT age, gender FROM runners').fetchall()
    else:
        age_distribution = g.db.execute('SELECT age, gender FROM runners WHERE club = ?', (club_id,)).fetchall()
    male_ages = [row[0] for row in age_distribution if row[1] == 'Muž']
    female_ages = [row[0] for row in age_distribution if row[1] == 'Žena']

    age_groups = [(i, i + 5) for i in range(0, 86, 5)]
    male_age_counts = [sum(1 for age in male_ages if age_group[0] <= age < age_group[1]) for age_group in age_groups]
    female_age_counts = [sum(1 for age in female_ages if age_group[0] <= age < age_group[1]) for age_group in age_groups]

    violin_data = [['Age Group', 'Male', 'Female']]
    for i, age_group in enumerate(age_groups):
        age_range = f'{age_group[0]}-{age_group[1]-1}'
        violin_data.append([age_range, male_age_counts[i], female_age_counts[i]])

    average_male_age = round(sum(male_ages) / len(male_ages), 2) if male_ages else 0
    average_female_age = round(sum(female_ages) / len(female_ages), 2) if female_ages else 0

    average_age = [average_male_age, average_female_age]
    return average_age, violin_data


def fetch_competition_classification(club_id=None):
    if club_id==None:
        classification_counts =g.db.execute('''
                SELECT strftime('%Y', date) AS year, classification, COUNT(*) AS num_competitions
                FROM competitions
                GROUP BY year, classification
                ORDER BY year
            ''').fetchall()
    else:
        classification_counts =g.db.execute('''
            SELECT strftime('%Y', date) AS year, classification, COUNT(*) AS num_competitions
            FROM competitions
            WHERE org = ?
            GROUP BY year, classification
            ORDER BY year
        ''', (club_id,)).fetchall()
    chart_data = [['Year', 'Šprint', 'Stredná trať', 'Dlhá trať', 'Nočný OB','Skrátená trať','Iné', 'Knock-out']]
    years = [str(year) for year in range(1999, 2025)]
    total_competitions = 0
    for year in years:
        sprint_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Šprint'), 0)
        stredna_trat_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Stredná trať'), 0)
        dlha_trat_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Dlhá trať'), 0)
        nocny_ob_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Nočný OB'), 0)
        skratena_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Skrátená trať'), 0)
        other = next((row[2] for row in classification_counts if row[0] == year and row[1] == ''), 0)
        KO_count = next((row[2] for row in classification_counts if row[0] == year and row[1] == 'Knock-out šprint'), 0)
        
        chart_data.append([year, sprint_count, stredna_trat_count, dlha_trat_count, nocny_ob_count, skratena_count, other, KO_count])
        total_competitions += sprint_count + stredna_trat_count + dlha_trat_count + nocny_ob_count + skratena_count + other + KO_count
    return chart_data, total_competitions



@app.route('/club/competition/<competition_id>')
def competition(competition_id):
    comp_data = g.db.execute('SELECT * FROM competitions WHERE id = ?', (competition_id,)).fetchone()
    if comp_data:  
        categories = fetch_comp_categories (competition_id)    
        return render_template('competition.html', categories = categories, comp_data=comp_data)
    else:
        return "Club not found"