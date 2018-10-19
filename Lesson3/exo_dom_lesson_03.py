# -*- coding: utf-8 -*-
import requests
import pandas as pd
from bs4 import BeautifulSoup


'''
Written by Amine Lemaizi - MSGBD2019

!!! IMPORTANT : This program is run under Pyhton 3 !!!
!!! IMPORTANT : Please put your access token before running this script (update ACCESS_TOKEN variable value) !!!

What to do ?
------------
Simply run this program using the following command (at the same .py folder):

python exo_dom_lesson_03.py

The results will be printed respecting a certain canevas

Requirements :
--------------
beautifulsoup4==4.6.3
requests==2.19.1
pandas==0.23.0
'''

ACCESS_TOKEN = ''


def average_stargazers(username):
    average = 0
    repo_counter = 0
    api = "https://api.github.com/users/{}/repos?access_token={}&page={}"
    r = requests.get(api.format(username, ACCESS_TOKEN, 1))
    if(r.status_code == requests.codes.ok):
        link_header = r.headers.get('link', None)
        
        repos = r.json()
        repo_counter = len(repos)
        for repo in repos:
        	average += repo['stargazers_count']

        if link_header is not None:
            last_page = int(link_header.split(';')[1].replace("<", "").replace(">", "").strip().split('=')[-1])
            for page in range(2, last_page + 1):
                r = requests.get(api.format(username, ACCESS_TOKEN, page))
                repos = r.json()
                repo_counter += len(repos)

                for repo in repos:
                    average += repo['stargazers_count']

        if average != 0 : average = average / repo_counter
    
    return average, repo_counter


def main():
    user_url_list = []
    username_list = []
    df = pd.DataFrame(columns=['username', 'user_url', 'number_of_repos', 'average_stargazers'])
    starting_url = "https://gist.github.com/paulmillr/2657075"
    page = requests.get(starting_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table_lines = soup.find('article', class_='markdown-body').find_all("tr")

    for table_line in table_lines:
        user_cell = table_line.find('td')

        if user_cell is not None:
            link = user_cell.find('a')['href']
            username = link.split('/')[-1]
            user_url_list.append(link)
            username_list.append(username)

    df.username = username_list
    df.user_url = user_url_list

    for user in df.username:
        average, repo_count = average_stargazers(user)
        print("User %s has %s  repos with an average stars rate of %.2f" %(user, repo_count, average))
        df.loc[df.username == user, ['number_of_repos', 'average_stargazers']] = repo_count, average

    print(df.sort_values('average_stargazers', ascending=False).to_string())


if __name__ == "__main__":
    main()
