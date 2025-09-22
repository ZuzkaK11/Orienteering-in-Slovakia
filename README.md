# Orienteering in Slovakia

# Project Report: Analysis of Orienteering in Slovakia

## Introduction

### Background
Orienteering is a sport that combines physical fitness with navigation skills. Runners move through varied and often unfamiliar terrain, with the goal of completing a course using a map and compass in the shortest possible time. Courses are neither marked in advance nor visible in the terrain. Only control points, marked with orange-and-white flags, are placed along the route, which runners must locate in a specified order using their map.

Orienteering maps are specially designed to provide detailed information necessary for fast and accurate navigation in the terrain. The sport originated in Scandinavia at the end of the 19th century, initially used as part of military training. Since then, it has spread worldwide. Today, competitions are organized at all levels, from local races to world championships.

Beyond physical fitness, a key aspect of orienteering is its contribution to mental resilience. The route between control points is not predetermined, and competitors must choose their own path. This forces runners to make continuous decisions based on terrain conditions and navigational challenges, promoting quick thinking and the ability to focus under pressure. A competitor's result thus depends not only on running speed but also on the optimal choice of routes between controls and the speed and accuracy of decision-making.

Additionally, orienteering often takes place in interesting natural landscapes or historic urban areas, adding another unique aspect to the sport.

The motivation for this project was to collect, process, analyze, and visualize data, allowing both myself and others to better understand the functioning of a sport I actively participate in.

---

### Project Goals
In Slovakia, orienteering is organized and regulated by sports clubs and the Slovak Orienteering Federation. Information about the distribution of runners, competition participation, long-term trends, and club engagement can provide valuable insights for organizers, participants, and enthusiasts for future development. A simple web application with interactive charts can also help promote orienteering to the public.

---

### Data Sources
Data for this project were obtained from the following sources:
- The official website of the Slovak Orienteering Federation Information System ([IS SZOŠ](https://is.orienteering.sk))
- GPS coordinates of Slovak cities from an Excel file available on [SimpleMaps](https://simplemaps.com/data/sk-cities)

---

## Procedure

### Data Collection
Data were collected using web scraping and processing techniques from external sources. I used Python libraries such as BeautifulSoup, Requests, Pandas, and NumPy. This process involved multiple steps and scripts to ensure the completeness and accuracy of the data.

#### a) Collecting Club and Runner Data
The first step was to obtain data about clubs from the Orienteering Information System. This step was crucial, as club IDs were needed to link different databases. Using the script `read_clubs.py`, I extracted links to individual clubs. These links were processed with the `write_club.py` script, which retrieved detailed information about each club and its members. The processed data were stored in the `runners` and `clubs` tables.

#### b) Collecting Competition Data
The information system contains competition data from 2018 onwards. Competitions from 1999–2018 are registered but not fully detailed because the online system was not fully operational at that time. Therefore, two different approaches were used for processing competitions. In both cases, data were collected only from national events, as regional competitions may use modified rules for categories and classification.

In the first case, all competitions were processed, registered runners were extracted, and this information was stored in the `competitions` and `competition_categories` tables. For older competitions, participant registrations were not processed. For this reason, some analyses are only performed from 2018, when the data are complete and accurate.

#### c) Collecting City Data
GPS coordinates of Slovak cities were extracted from the Excel file available on [SimpleMaps](https://simplemaps.com/data/sk-cities) and imported into the `cities` table.

---

### Data Processing
Data were stored in an SQL database called `orienteering.db`. Data cleaning and proper formatting were performed during insertion into the tables. The database schema included the following tables:  
- `Runners` (information about runners)  
- `Clubs` (club details)  
- `Competitions` (competition data)  
- `Competition_categories` (competition categories)  
- `Cities` (city data)  

---

### Data Visualization and Analysis
For data visualization, I created a web application using the Flask framework with three HTML templates:
- `main.html`: The main page displays key metrics such as club activity, age and gender distribution of runners, and competition classifications. A list of all clubs is provided for easy navigation to individual club pages.
- `club.html`: Displays detailed information about each club, including charts showing the distribution of members by gender, age, and competitions organized since 2018. Competitions are listed and clickable for detailed views.
- `competition.html`: Displays information about a competition and a chart visualizing participants in each category.

Charts and maps were created using Google Charts and Leaflet, providing an interactive approach to the data with the possibility of updates. The analysis focused mainly on the main page charts, as they offer a comprehensive overview of orienteering in Slovakia and help identify key trends and relationships between clubs, competitions, and runners.

---

## Analysis Results

### Runners
Currently, there are 861 registered orienteering runners in Slovakia, with a very wide age distribution (Chart 1). Orienteering is often considered a family sport, as it allows participation across all age categories. Families can attend competitions, with each member competing in their own category. Categories such as OPEN and N are available for the public and beginners, allowing them to learn the basics on simpler courses.

Categories are divided by age and gender, with younger categories in two-year intervals and veteran categories in five-year intervals. The main category is W21/M21, whose top runners form the national team and may represent Slovakia at European or World events.  
Orienteering is also a sport with balanced gender representation. In Slovakia, approximately 60% of participants are male and 40% female (Chart 2). It actively supports gender equality and provides opportunities for all age groups.

<img src="/images/graf1.png" alt="Chart 1" height="300"> <img src="/images/graf2.png" alt="Chart 2" height="300">

*Chart 1: Age distribution of runners, showing demographic composition and identifying the largest groups. The average age of men and women is indicated in the title, with men averaging 3 years older.*  
*Chart 2: Gender distribution in clubs. The proportion of men and women is shown as bars, with horizontal lines representing overall averages.*

---

### Clubs

<img src="/images/graf3.png" alt="Chart 3" height="300">  
*Chart 3: Interactive map showing the location of clubs. Circle size represents the number of members per club.*

The SZOŠ currently has 21 registered clubs. They represent the local level, all linked to the national federation. Clubs are generally open to all interested individuals. Most clubs are located in regional cities, with the Bratislava region having the largest share of both clubs and runners (Chart 3). More than half of runners come from the five largest clubs (Chart 4), while smaller clubs have fewer than 50 members.

<img src="/images/graf4.png" alt="Chart 4" height="300"> <img src="/images/graf5.png" alt="Chart 5" height="300">

*Chart 4: Number of members per club. Each color segment represents a club’s members.*  
*Chart 5: Number of competitions organized by each club from 2018–2024. Highlights the most active clubs.*

Clubs are also responsible for organizing competitions, ideally rotating responsibilities to ensure equal participation. The total number of competitions can be misleading, as clubs vary in size (Chart 5). Chart 6 shows the number of members per organized competition, revealing a significant disparity; seven clubs have not organized any events in the last six years.

Member activity relative to completed competitions can also be informative. Chart 7 shows that three clubs are nearly inactive. Differences between clubs are smaller, but overall average participation is low, despite approximately 18 national competitions per year.

<img src="/images/graf6.png" alt="Chart 6" height="300"> <img src="/images/graf7.png" alt="Chart 7" height="300">

*Chart 6: Member-to-competition ratio for clubs (2018–2024).*  
*Chart 7: Average competition participation per member per year (2018–2024).*

---

### Competitions
Slovakia offers ideal conditions for orienteering, including varied terrain, beautiful nature, and high-quality cartography. Several major international and world competitions have been successfully organized here. In 2023, Košice hosted the Veteran World Championships.

Orienteering takes place in forests, urban areas, and different seasons. It includes multiple formats: long and middle-distance courses, sprints, night events, and hybrid competitions like mountain biking or ski orienteering. The newest discipline is the knock-out sprint, featuring multiple elimination rounds and providing spectator appeal. All disciplines share the goal of finding all control points in the correct order as quickly as possible. Discipline popularity depends on runner preferences (Chart 8).

<img src="/images/graf8.png" alt="Chart 8" height="300">

*Chart 8: Popularity of different disciplines. Y-axis: discipline names; X-axis: average participants per competition.*

Competitions are divided into regional, school, and national events. This analysis focuses on national competitions, as school competitions may include unregistered participants and regional competitions may have differing classification rules.

National competitions include the Slovak rankings and national championships. Championships are held once per season for each discipline, while rankings account for other events. Points contribute to the national ranking.

The season lasts from March to late November, with competitions evenly spread, except during summer holidays when participation may decrease due to travel. Clubs organize the competitions, ideally rotating responsibility. Some clubs, such as TKE (Karst) and BBA (Cesom), consistently organize traditional events that remain popular (Chart 9). Participation trends slightly decline over the season (Chart 9), with fewer participants later in the season.  

<img src="/images/graf9.png" alt="Chart 9" height="300"> <img src="/images/graf10.png" alt="Chart 10" height="300">

*Chart 9: Scatter plot of participant numbers by competition date, showing a slight decreasing trend.*  
*Chart 10: Total number of competitions per year since 1999, color-coded by classification. Data inconsistencies pre-2018 are noted.*

Competition numbers fell sharply in 2020–2021 due to the COVID-19 pandemic (Chart 10). This affected youth participation, especially ages 16–20 (Chart 11), and some clubs faced financial difficulties or altered participation patterns.

<img src="/images/graf11.png" alt="Chart 11" height="300">

*Chart 11: Histogram of average runner representation in competition categories.*

Despite challenges, the federation and clubs attempt to restore participation through promotions, school competitions, and recruitment programs. Orienteering remains a family sport, and a positive correlation exists between age and number of completed competitions (Chart 12), highlighting long-term activity and multi-age participation.

<img src="/images/graf12.png" alt="Chart 12" height="300">

*Chart 12: Scatter plot of age vs. number of competitions completed. Older participants show high activity.*

---

## Conclusion
Orienteering has a long history in Slovakia but continues to develop. Neighboring Czechia has five times more runners and stronger youth programs. Czech runners are world-class, while Slovak successes are rare. This project provides insights into orienteering in Slovakia and, with expansion, may contribute to its growth.  
The project collected, processed, and analyzed data, and the web application provides an engaging overview of the sport, long-term trends, runner participation, and club activities. It highlighted the importance of working with data, which can be a key tool for solving challenges in this field. Data analysis offered a new perspective on a sport I actively enjoy.

---

## References
- [IS SZOŠ](https://is.orienteering.sk)  
- [SimpleMaps](https://simplemaps.com/data/sk-cities)  
