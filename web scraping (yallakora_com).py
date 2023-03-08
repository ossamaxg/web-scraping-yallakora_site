
import requests
from bs4 import BeautifulSoup
import csv
import time

start = time.time()
date = input('Would you enter date please (like 21/mar/23 or 21mar23): ')
page = requests.get(f'https://www.yallakora.com/match-center/مركز-المباريات?date={date}#days')
def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    matches_details = []
    champs = soup.find_all('div', {'class': 'matchesList'})
    for champ in champs:
        champ_title = champ.h2.text.strip()
        champ_date = champ.find('div', {'class': 'date'}).text.strip()
        matches = champ.find_all('li', {'class': 'item finish'})
        def get_matches_details(matches):
            for match in matches:
                match_status = match.span.text.strip()
                team_A = match.p.text.strip()
                team_B = match.find('div', {'class': 'teams teamB'}).p.text.strip()
                score_1 = match.find('span', {'class': 'score'}).text.strip()
                score_2 = match.find_all('span', {'class': 'score'})[1].text.strip()
                match_result = f'{score_2} - {score_1}'
                teams = f'{team_A} - {team_B}'
                match_time = match.find('span', {'class': 'time'}).text.strip()
                matches_details.append({'عنوان البطولة': champ_title, 'مرحلة البطولة': champ_date, 'حالة المباراة': match_status, 'الفرق': teams, 'النتيجة': match_result, 'وقت المباراة': match_time})
        get_matches_details(matches)
        keys = matches_details[0].keys()
        with open(f'yallakora/matches_details_{date.replace("/", "")}.csv', 'w') as op_file:
            dict_writer = csv.DictWriter(op_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)
    print('\n done \n', time.time() - start, 'seconds')
main(page)


