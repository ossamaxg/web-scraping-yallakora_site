
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
    champs = soup.find_all('div', {'class': 'matchCard'})
    for i in range(len(champs)):
        champ_title = champs[i].h2.text.strip()
        all_matches = champs[i].find_all('div', {'class': 'teamsData'})

        def get_matches_details(all_matches):
            for j in range(len(all_matches)):
                team_A = all_matches[j].find('div', {'class': 'teams teamA'}).p.text.strip()
                team_B = all_matches[j].find('div', {'class': 'teams teamB'}).p.text.strip()
                score_1 = all_matches[j].find_all('span', {'class': 'score'})[0].text.strip()
                score_2 = all_matches[j].find_all('span', {'class': 'score'})[1].text.strip()
                match_result = f'{score_1} - {score_2}'
                teams = f'{team_A} - {team_B}'
                match_time = all_matches[j].find_all('span', {'class': 'time'})[0].text.strip()
                matches_details.append({'نوع البطولة': champ_title, 'ميعاد المباراة': match_time, 'الفرق': teams, 'النتيجة': match_result})
        get_matches_details(all_matches)
        keys = matches_details[0].keys()
        with open(f'matches_details_{date.replace("/", "")}.csv', 'w') as op_file:
            dict_writer = csv.DictWriter(op_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)

    print('\n', 'done', '\n', time.time() - start, 'seconds')
main(page)


