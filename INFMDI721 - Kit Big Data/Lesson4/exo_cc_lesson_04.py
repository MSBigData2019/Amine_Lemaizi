import requests
import pandas as pd


def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')


if __name__ == '__main__':
	medicament = "paracetamol"
	limit = 100
	url = "https://www.open-medicaments.fr/api/v1/medicaments?limit={}&query={}".format(limit, medicament)
	med_url = "https://www.open-medicaments.fr/api/v1/medicaments/{}"

	response = requests.get(url)

	medi_dic = response.json()
	total = len(medi_dic)

	i = 1
	lst = []

	for med in medi_dic:
		code = med['codeCIS']
		denomination = med['denomination']
		response_2 = requests.get(med_url.format(code))
		med_info = response_2.json()

		dosage = med_info['substancesActives'][0]['dosageSubstance']
		forme_pharmaceutique = med_info['formePharmaceutique']
		prix = med_info['presentations'][0]['prix']

		lst.append([code, denomination, dosage, prix, forme_pharmaceutique])

		progbar(i, total, 10)
		i += 1

	print()
	df = pd.DataFrame(lst, columns=['code', 'dénomination', 'dosage', 'prix', 'forme galénique'])
	df[['dosage numérique', 'unité']] = df.pop('dosage').str.split(r'\s', expand=True)
	df['dosage numérique'] = pd.to_numeric(df['dosage numérique'].str.extract(r'(\d{1,3})'))
	df['multiplicateur'] = df['unité'].apply(lambda x : 1 if x == 'mg' else 1000 )
	print(df)