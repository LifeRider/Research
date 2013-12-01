######################## import statements
from bs4 import BeautifulSoup

####################### data sources, like the wiki addresses
local_wikis = {'2010':'List_of_MPs_elected_in_the_United_Kingdom_general_election,_2010.html',
			   '2005':'List_of_MPs_elected_in_the_United_Kingdom_general_election,_2005.html',
			   '2001':'MPs_elected_in_the_United_Kingdom_general_election,_2001.html',
			   '1997':'List_of_MPs_elected_in_the_United_Kingdom_general_election,_1997.html',
			   '1992':'MPs_elected_in_the_United_Kingdom_general_election,_1992.html',
			   '1987':'MPs_elected_in_the_UK_general_election,_1987.html',
			   '1983':'MPs_elected_in_the_United_Kingdom_general_election,_1983.html',
			   '1979':'MPs_elected_in_the_United_Kingdom_general_election,_1979.html'}

years = local_wikis.keys()

################## create soups - use the html5lib parser to avoid errors and missing data
def Soup(year):
	return BeautifulSoup(open(local_wikis[year],'r'), "html5lib")

################### wiki table rows 
def tableRows(year):
	soup = Soup(year)
	if year == '2010':
		all_tables = soup.find_all('table')
		mp_table = all_tables[2]
	else:
		all_tables = soup.find_all('table', class_="wikitable")
		mp_table = all_tables[1]
	return mp_table('tr')

# filtering empty rows out
def rowFilter(row):
	return row.find_all('td', attrs={"bgcolor":"#CCCCFF"}) or row.find_all('th') or len(row.find_all('td'))==1 or row.find_all('a') == []

################### title analysis - take all names that have three words or more and sift through the firsts
# create a dict - {'parliament_size':<x>, 'title1':<title1>, etc.}
title_dict = {}
def getTitle(row, year):
	if year == '2010':
		return None
	second_row = row.contents[3]
	all_text = second_row.get_text().split()
	if len(all_text) > 2:
		if all_text[0] == 'The':
			return ' '.join(all_text[:2])
		else:
			return all_text[0]

################### extract names and wiki pages for all MPs
# use a dictionary with the link as key and a list of names as values to get rid of multiple entries.
all_mps_1979_2010 = {}

def getData(year):
	i = 0
	if year == '2010':
		i = 2
	else:
		i = 1
	names_and_links = {}
	title_dict_local = {}
	for row in tableRows(year):
		# avoiding the lettered sections of the table and repeated headers
		if rowFilter(row):
			continue
		else:
			all_a = row.find_all('a')
			mp_wiki = all_a[i].get('href')
			mp_name = all_a[i].get_text()
			if getTitle(row, year) :
				title = getTitle(row, year)
				if title not in title_dict:
					title_dict[title] = 1
				else:
					title_dict[title] += 1
				if title not in title_dict_local:
					title_dict_local[title] = 1
				else:
					title_dict_local[title] += 1
			if mp_wiki not in names_and_links:
				names_and_links[mp_wiki] = [mp_name]
			if mp_wiki not in all_mps_1979_2010:
				mp_wiki_list = [mp_name, 1]
				all_mps_1979_2010[mp_wiki] = mp_wiki_list
			else:
				all_mps_1979_2010[mp_wiki][1] += 1
	return names_and_links, len(names_and_links), title_dict_local

def returnData(years):
	all_dicts = [all_mps_1979_2010]
	total_number_of_seats = 0
	for year in years:
		dicts, totals, titles = getData(year)
		total_number_of_seats += totals
		all_dicts.append(dicts)
		titles['year'] = year
		print titles
	frequency_of_reelection = {}
	for politician in all_mps_1979_2010:
		if all_mps_1979_2010[politician][1] not in frequency_of_reelection:
			frequency_of_reelection[all_mps_1979_2010[politician][1]] = 1
		else:
			frequency_of_reelection[all_mps_1979_2010[politician][1]] += 1
		#if all_mps_1979_2010[politician][1] == 8:
		#	print all_mps_1979_2010[politician][0]
	#hdoehd = 0
	#for entry in frequency_of_reelection:
	#	hdoehd += frequency_of_reelection[entry]
	print all_mps_1979_2010
	print frequency_of_reelection
	#print hdoehd
	print len(all_mps_1979_2010)
	print total_number_of_seats
	print len(all_dicts)
	#print title_dict

returnData(years)

################### constituency analysis - how often do the MPs change it?