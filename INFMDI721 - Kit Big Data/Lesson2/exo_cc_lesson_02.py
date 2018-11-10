# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

'''
This program gives the average discount offered for a certain laptop selled at www.darty.com

!!! IMPORTANT : This code was run under Python 2 !!!

Requirements :
beautifulsoup4==4.6.3
bs4==0.0.1
certifi==2018.8.24
chardet==3.0.4
idna==2.7
requests==2.19.1
urllib3==1.23

'''


def average_discount(search_words):
    idems_limit = 600
    url_search_word = ""
    words = search_words.split(" ")
    if len(words) == 1:
        url_search_word = search_words
    else:
        for word in words:
            url_search_word = word + "+" + url_search_word

    url = "https://www.darty.com/nav/recherche?p=%s&s=relevence&text=%s&fa=756" % (idems_limit, url_search_word)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    discounts = soup.find_all(class_="darty_prix_barre_remise")
    discounts_list = [float(x.text.replace('%', '').replace(' ', '')) / 100 for x in discounts]

    average = 0 if len(discounts_list) == 0 else sum(discounts_list) / len(discounts_list)
    return average


if __name__ == "__main__":
    print("Dell average discount is {:.2%}".format(average_discount("dell")))
    print("Acer average dicout is {:.2%}".format(average_discount("acer")))
