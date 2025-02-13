# Orienteering-in-Slovakia

# Správa projektu: Analýza orientačného behu na Slovensku

## Autor: Zuzana Kováčová  
**Odbor:** DAV  

## Úvod

### Pozadie
Orientačný beh je športová disciplína, ktorá kombinuje fyzickú kondíciu s navigačnými schopnosťami. Bežci sa pohybujú po rôznorodom a zvyčajne neznámom teréne, pričom úlohou je prebehnúť podľa mapy a buzoly trať za čo najkratší čas. Trate nie sú vopred známe a ani vyznačené v teréne. Sú tam umiestnené iba kontrolné stanovišťa, označené oranžovo-bielym lampiónom, ktoré musí bežec pomocou mapy v stanovenom poradí nájsť. 

Mapy používané v orientačnom behu sú špeciálne navrhnuté tak, aby poskytovali podrobné informácie potrebné pre rýchle a presné navigovanie v teréne. Tento šport vznikol v Škandinávii na konci 19. storočia, kde sa v počiatkoch využíval ako súčasť vojenského výcviku. Odvtedy sa rozšíril do celého sveta. V súčasnosti sa organizujú súťaže na všetkých úrovniach, od miestnych pretekov až po svetové šampionáty.

Okrem fyzickej zdatnosti je významným aspektom orientačného behu aj jeho prínos k mentálnej odolnosti. Trasa totiž nie je medzi kontrolnými bodmi vopred určená a pretekári si musia vybrať vlastnú cestu. Tento fakt núti bežcov neustále robiť rozhodnutia na základe terénnych podmienok a navigačných výziev, čo podporuje rýchle myslenie a schopnosť sústrediť sa pod tlakom. Výsledok pretekára teda nezávisí len od rýchlosti behu, ale aj od optimálneho výberu postupov medzi kontrolami či rýchlosti a správnosti rozhodovania.

Navyše, orientačný beh sa často koná v zaujímavých prírodných lokalitách či členitých historických mestách, čo dodáva tomuto športu ďalší špecifický aspekt.

Motiváciou pre tento projekt bolo zhromaždiť, spracovať, analyzovať a vizualizovať dáta, čo by umožnilo nielen mne, ale aj ostatným ľuďom lepšie pochopiť fungovanie tohto športu, ktorému sa aktívne venujem.

---

### Ciele projektu
Na Slovensku je orientačný beh organizovaný a regulovaný športovými klubmi a Slovenským zväzom orientačných športov. Informácie o rozložení bežcov, účastiach na súťažiach, dlhodobých trendoch či angažovaní jednotlivých klubov môžu poskytnúť cenné informácie pre organizátorov, účastníkov a nadšencov tohto športu v budúcom rozvoji. Jednoduchá webová aplikácia s interaktívnymi grafmi môže zároveň pomôcť pri popularizácii orientačného behu medzi verejnosťou.

---

### Zdroje údajov
Dáta pre tento projekt boli získané z nasledujúcich zdrojov:
- Oficiálna webová stránka Informačného systému Slovenského zväzu orientačných športov ([IS SZOŠ](https://is.orienteering.sk))
- GPS koordináty slovenských miest z Excel súboru dostupného na stránke [SimpleMaps](https://simplemaps.com/data/sk-cities)

---

## Postup

### Zhromažďovanie údajov
Na získanie údajov som použila rôzne techniky Web Scrapingu a spracovania dát z externých zdrojov. Pracovala som s pythonovskými knižnicami ako napríklad BeautifulSoup, Requst, Pandas či NumPy. Tento proces zahŕňal viaceré kroky a rozdelenie do viacerých skriptov, čím sa mala zabezpečiť úplnosť a presnosť získaných informácií.

#### a) Získavanie údajov o kluboch a pretekároch
Prvým krokom bolo získanie dát o kluboch z Informačného systému orientačných športov. Tento krok bol kľúčový, pretože klubové ID bolo potrebné na prepojenie jednotlivých databáz. Pomocou skriptu `read_clubs.py` som extrahovala linky na jednotlivé kluby. Tieto linky som spracovala pomocou skriptu `write_club.py`, ktorý získal detailné informácie o každom klube a jeho členoch. Spracované údaje boli zapisované do tabuliek `runners` a `clubs`.

#### b) Získavanie údajov o súťažiach
Informačný systém obsahuje údaje o súťažiach od roku 2018. Súťaže z obdobia 1999-2018 sú síce v systéme registrované, avšak nie s kompletnými údajmi, pretože v tom čase tento online systém ešte nefungoval. Z tohto dôvodu som na spracovanie súťaží použila dva rôzne prístupy. V oboch prípadoch som získavala údaje len z národných podujatí, keďže oblastné súťaže môžu využívať upravené pravidlá pre kategórie a klasifikáciu. 
V prvom prípade som prešla cez všetky súťaže, extrahovala prihlásených pretekárov a tieto informácie zapísala do tabuliek `competitions` a `competition_categories`. V druhom prípade som pri starších súťažiach nespracovávala prihlášky. Z tohto dôvodu sú niektoré analýzy robené až od roku 2018, kedy sú údaje kompletné a presné.


#### c) Získavanie údajov o mestách
Dáta GPS súradníc slovenských miest boli extrahované z Excel súboru dostupného na [SimpleMaps](https://simplemaps.com/data/sk-cities). Tieto údaje boli importované do tabuľky `cities`.

---

### Spracovanie údajov
Na uloženie údajov som použila SQL databázu `orienteering.db`. Samotné spracovávanie, čistenie údajov či správne formátovanie bolo vykonávané už priamo pri vkladaní dát do tabuliek. Jej schéma zahŕňala tabuľky:  
- `Runners` (informácie o bežcoch)  
- `Clubs` (detaily o kluboch)  
- `Competitions` (údaje o súťažiach)  
- `Competition_categories` (kategórie pre súťaže)  
- `Cities` (údaje o mestách)  

---

### Vizualizácia a analýza údajov
Na vizualizáciu dát som vytvorila webovú aplikáciu vo frameworku Flask s tromi HTML šablónami:
- `main.html`: Hlavná stránka obsahuje kľúčové metriky ako vizualizácia aktivity klubov, rodového a vekového rozloženia bežcov či klasifikácie súťaží. Hneď na začiatku sa nachádza zoznam jednotlivých klubov, odkiaľ sa dá prekliknúť na stránku každého klubu.
- `club.html`: Na stránke každého klubu sú jeho detailné informácie a tiež grafy vizualizujúce distribúciu členov podľa pohlavia, veku a organizovanie súťaží od roku 2018. Tieto súťaže sú hneď vedľa aj vypísané a na každú sa dá prekliknúť.
- `competition.html`: Tu sa nachádzajú informácie o súťaži a graf vizualizujúci pretekárov v jednotlivých kategóriách.

Na vizualizáciu dát a mapy som použila nástroje a grafy z knižnice Google Charts a Leaflet. Tým som docielila interaktívny prístup k dátam a možnosť aktualizácie údajov.
V analýze som sa zamerala najmä na grafy na úvodnej stránke, nakoľko práve tieto poskytujú komplexný pohľad na orientačný beh na Slovensku a umožňujú identifikovať kľúčové trendy a vzťahy medzi klubmi, súťažami a bežcami.

---

## Výsledky analýzy

### Bežci
V súčasnosti je na Slovensku registrovaných 861 orientačných bežcov, pričom vekové rozloženie ja naozaj veľmi široké (Graf 1). Často sa orientačný beh označuje aj ako rodinný šport, pretože umožňuje účasť všetkých členov rodiny v rôznych vekových kategóriách. Takže na preteky môže prísť celá rodina a každý beží vo svojej kategórií. Väčšinou sú zaraďované aj kategórie ako OPEN a N, určené pre verejnosť a začiatočníkov, kde sa môžu na jednoduchých tratiach naučiť základy.

Kategórie sú rozdelené podľa veku a pohlavia, pričom mladšie kategórie majú dvojročné intervaly a veteránske kategórie päťročné intervaly. Hlavnou kategóriou je W21/M21, ktorej najlepší pretekári tvoria jadro národnej reprezentácie a majú možnosť reprezentovať Slovensko na európskych či svetových podujatiach.
Orientačný beh sa taktiež zaraďuje medzi športy, ktoré sa vyznačujú vyváženým zastúpením oboch pohlaví. Zastúpenie pohlaví v orientačnom behu na Slovensku ukazuje, že približne 60 % účastníkov sú muži a 40 % ženy (Graf 2). Orientačný beh je teda šport, ktorý aktívne podporuje rodovú rovnosť a poskytuje príležitosti pre rôzne vekové kategórie. 

### Kluby
SZOŠ má momentálne 21 registrovaných členských klubov. Predstavujú lokálnu úroveň a všetky sú spolu pridružené k národnej úrovni riadiaceho orgánu SZOŠ. Kluby sú väčšinou otvorené pre všetkých záujemcov a v prípade záujmu je tak možné kontaktovať priamo klub v blízkosti. Kluby sú zväčša situované v krajských mestách pričom Bratislavský kraj má väčšinové zastúpenie nielen vo výrazne väčšom počte klubov, ale aj celkovom počte pretekárov (Graf 3). Zaujímavosťou je, že viac než polovica pretekárov pochádza len z 5 najväčších klubov (Graf 4). Zvyšné kluby tvoria len menšinové zastúpenie, pričom ich počet členov nepresahuje hranicu 50.

Kluby sú taktiež zodpovedné za organizovanie pretekov, pričom táto úloha by sa mala počas roka a jednotlivých sezón striedať, aby sa rovnomerne zapojil každý klub. Celkový počet organizovaných pretekov, však môže byť skresľujúci nakoľko kluby sú rôzne veľké (Graf 5). Je rozdiel, či národnú súťaž organizuje klub s 10 členmi alebo vyše 100, kde sa práca prerozdelí. Z tohto dôvodu Graf 6 vyobrazuje počet členov na jednu organizovanú súťaž (čím vyššie číslo, tým horšia vizitka pre klub). Z grafu môžeme vidieť veľký nepomer, pričom až 7 klubov neorganizovalo za posledných 6 rokov žiadnu súťaž. V tomto prípade ide o malé kluby, ale aj toto môže byť predmetom diskusie a zefektívnenia spolupráce do budúcna.

Zaujímavým meradlom môže byť aj opačný pohľad, keď sa zameriame na aktivitu členov vzhľadom na absolvované preteky. Aj pri tomto porovnaní je možné vidieť, že 3 kluby sú takmer neaktívne (Graf 7). Rozdiely medzi klubmi sú o niečo menšie, avšak celkovo sa dá povedať, že priemerná účasť na pretekoch je pomerne nízka, na to, že každoročne býva v priemere 18 celoslovenských pretekov. Aj toto odzrkadľuje situáciu v kluboch, kde je registrovaných veľa neaktívnych alebo skôr hobby bežcov, ktorí sa zúčastňujú pretekov len príležitostne a tým znižujú celkový priemer.

### Súťaže
Slovensko má ideálne podmienky na orientačný beh, vrátane krásnej prírody s rozmanitým terénom a kvalitných kartografov, ktorí vytvárajú mapy na svetovej úrovni. Už v minulosti sa tu úspešne zorganizovalo niekoľko významných medzinárodných či svetových podujatí. Naposledy sa tak stalo v roku 2023, kedy Košice hostili Veteránske majstrovstvá sveta.
Orientačný beh sa odohráva v rôznych prostrediach – od lesov po mestské centrá, v každom ročnom období. Ponúka rôzne formy a disciplíny, vrátane klasických pretekov na dlhé a stredné trate, šprintu, nočných pretekov či pretekov s rôznymi formami prepojenia iných športov, ako napríklad orientácia na horských bicykloch alebo lyžiach. Najnovšou disciplínou je knock-out šprint, ktorý sa skladá z viacerých vyraďovacích kôl a je tak atraktívnejší najmä pre divákov. Všetky disciplíny však spája spoločný cieľ, a to nájsť všetky kontrolné body v určenom poradí a byť najrýchlejší.
Obľúbenosť disciplín závisí najmä od preferencií jednotlivých bežcov (Graf 8). V minulosti sa pretekalo len na dlhých a stredných tratiach, no dnes sa tešia obľúbenosti aj šprinty, ktoré sú typické svojou dynamickosťou a mestským terénom.

Každoročne sa organizuje veľa rôznych súťaží. V rámci Slovenska sú rozdelené na oblastné, školské a celoslovenské. V analýze som sa venovala práve celoslovenským pretekom, nakoľko na školských sa zúčastňujú aj neregistrovaní bežci a pri oblastných sa pravidlá klasifikácie a rozdelenia kategórií mierne líšia.

Celoslovenské preteky zahŕňajú Slovenské rebríčky a majstrovstvá Slovenska. Majstrovstvá Slovenska sa pre každú disciplínu konajú raz za sezónu, zatiaľ čo Slovenské rebríčky tvoria zvyšok. V oboch prípadoch sa získavajú body, ktoré sa počítajú do celoslovenského rankingu.

Počas sezóny, ktorá trvá približne od marca do konca novembra, sú preteky rozdelené zväčša rovnomerne. Výnimkou sú letné prázdniny kedy ich je menej, pretože pretekári často cestujú na medzinárodné preteky a sústredenia do zahraničných terénov. Organizačnú štruktúru pretekov na Slovensku tvoria samotné kluby, a preto by si túto povinnosť mali rovnomerne prerozdeliť, aby každý prispel svojím podielom. Aj napriek tomu sú niektoré kluby aktívnejšie ako iné a majú tradíciu organizovať rovnaké preteky každý rok v podobnom termíne. Medzi takéto kluby patrí napríklad TKE (Karst) alebo BBA (Cesom). Práve tieto preteky s tradičným charakterom patria medzi najnavštevovanejšie (Graf 9). Pretekári si ich obľúbili a vždy vedia, čo môžu očakávať. Spôsobené je to najmä vďaka vybudovaniu si dlhoročnej tradície a kvality. Z grafu je tiež možné vidieť mierne klesajúcu tendenciu, čo sa týka počtu účastníkov na priebeh sezóny. Ku koncu sezóny býva menšia účasť na pretekoch, čo odzrkadľuje najmä nastavenie pretekárov. Po zimnej pauze sa všetci tešia na preteky, zatiaľ čo po lete sa účasť znižuje. Výnimku tvoria spomínané tradičné letné preteky.

Každá sezóna je plánovaná tak, aby bol počet pretekov pomerne stabilný. Výrazný pokles nastal v rokoch 2020-2021, keď bol šport obmedzený kvôli pandémii COVID-19 (Graf 10). Dôsledky tohto poklesu sú viditeľné aj v prítomnosti, keď sa počet účastníkov stále nedostal na úroveň pred pandémiou. Dôvodov je viacero, pričom medzi najvýraznejšie patrí prerušená práca s mládežou, čo spôsobilo výrazné oslabenie mládežníckej základne najmä v aktuálnom veku 16-20 rokov (Graf 11). Taktiež niektoré kluby čelili finančným problémom či ľudia zmenili návyky a sociálne interakcie.

Napriek všetkým týmto nepriaznivým faktorom sa zväz aj kluby snažia obnoviť pôvodne počty rôznymi iniciatívami ako sú rôzne promo akcie, školské preteky či náborové krúžky, ktoré majú za cieľ predstaviť tento šport verejnosti a získať väčšiu podporu.
Okrem spomínaného faktu, že orientačný beh je často rodinným športom, je zaujímavý aj vzťah veku a počtu absolvovaných pretekov (Graf 12). Okrem mládežníckych kategórií sa najmä v tých starších nachádzajú stále aktívni pretekári, ktorí majú absolvovaných najviac pretekov. Môže sa to zdať samozrejmé, keďže mali viac času, ale v porovnaní s inými športami ide skôr o raritu. Aj to dokazuje, že je to skutočne šport pre všetky vekové kategórie a v budúcnosti má veľký potenciál.

---

## Záver
Orientačný beh má na Slovensku dlhú históriu, no aj tak sa dá povedať, že stále sa len rozvíja. Napríklad, susedné Česko má päťkrát viac bežcov a vyššiu úroveň systematickej práce s mládežou aj dospelými. Česi patria k svetovej špičke, zatiaľ čo úspechy slovenských bežcov na svetových podujatiach sú zatiaľ ojedinelé. Verím, že aj tento projekt pomôže nahliadnuť do fungovania orientačného behu na Slovensku a s prípadným rozšírením prispeje k jeho budúcemu rozvoju.
Celkovo tento projekt zhromaždil, spracoval a analyzoval údaje o orientačnom behu na Slovensku. Vytvorená webová aplikácia poskytuje zaujímavý pohľad na tento šport, pomáha pochopiť dlhoročné trendy, účasti pretekárov či aktivity klubov.
Skúsenosti získané z tohto projektu mi zdôraznili dôležitosť práce s dátami, keďže práve oni môžu byť kľúčovým nástrojom na riešenie problematiky v danej sfére. Osobne ma spracovanie dát a ich následná analýza veľmi bavila a poskytla mi nový pohľad na šport, ktorému sa venujem.

---

## Zdroje
- [IS SZOŠ](https://is.orienteering.sk)  
- [SimpleMaps](https://simplemaps.com/data/sk-cities)  
