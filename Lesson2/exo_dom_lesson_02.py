# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


'''
Written by Amine Lemaizi - MSGBD2019

!!! IMPORTANT : This program is run under Pyhton 3 !!!

What to do ?
------------
Simply run this program using the following command (at the same .py folder):

python exo_dom_lesson_02.py

The results will be printed respecting a certain canevas

Requirements :
--------------
beautifulsoup4==4.6.3
requests==2.19.1

'''

# List of entries
companies = {
	'Airbus': "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
	'LVMH' : "https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
	'Danone' : "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"
}

# List collecting the results
results = []

# Text canevas for printing results
text_canevas = '''================================
{} - Status and Summary
================================

Sales Q4 Dec 2018 (In millions of EUR):
---------------------------------------
High : {:,.2f}
Mean : {:,.2f}
Low : {:,.2f}

Stock Value and Percentage Change:
----------------------------------
Value : {:,.2f} EUR
Change : {:.2%}

Percentage of Institutional holders:
------------------------------------
Percentage : {:.2%}

Dividends Yield:
----------------
Company : {:,.2f} EUR
Industry : {:,.2f} EUR
Sector : {:,.2f} EUR
'''

for key, value in companies.items():
	# Initialization
	data = {'company_name': key}
	page = requests.get(value)
	soup = BeautifulSoup(page.text, 'html.parser')

	# Extract Quarter Sales Dec 2018
	data_table = soup.find(class_='dataTable')

	sales = data_table.find_all('tr')[2].find_all('td')
	data['sales_high'] = float((sales[3].text).replace(',', ''))
	data['sales_mean'] = float((sales[2].text).replace(',', ''))
	data['sales_low'] = float((sales[4].text).replace(',', ''))

	# Stock price and evo

	stock_info = soup.find(class_="sectionQuoteDetail")
	data['stock_value'] = float((stock_info.find_all('span')[1].text).strip())
	stock_evo_text = soup.find(class_="valueContentPercent").text.replace("(", "").replace(")", "").strip()
	data['stock_evo'] = float(stock_evo_text.replace("%", ""))/100

	# Percentage of INSTITUTIONAL HOLDERS
	per_institutional_holders_text = soup.find_all(class_='dataSmall')[-1].find(class_="data").text
	data['per_institutional_holders'] = float(per_institutional_holders_text.replace("%", ''))/100

	# Dividend Yield
	dividend_table = soup.find_all(class_='dataTable')[2]
	dividends = dividend_table.find_all('tr')[1].find_all('td')
	data['dividend_sector'] = float((dividends[3].text))
	data['dividend_industry'] = float((dividends[2].text))
	data['dividend_company'] = float((dividends[1].text))

	# Collecting data scrapped
	results.append(data)

# Printing the results using text canevas
for result in results:
	print(
		text_canevas.format(
			result['company_name'], 
			result['sales_high'], 
			result['sales_mean'],
			result['sales_low'],
			result['stock_value'],
			result['stock_evo'],
			result['per_institutional_holders'],
			result['dividend_company'],
			result['dividend_industry'],
			result['dividend_sector']
			)
		)
