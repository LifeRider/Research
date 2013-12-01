########################import statements
import urllib2

#######################data sources, like the wiki addresses
wikis = {'2010':'http://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_2010',
         '2005':'http://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_2005',
         '2001':'http://en.wikipedia.org/wiki/MPs_elected_in_the_United_Kingdom_general_election,_2001',
         '1997':'http://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_1997',
         '1992':'http://en.wikipedia.org/wiki/MPs_elected_in_the_United_Kingdom_general_election,_1992',
         '1987':'http://en.wikipedia.org/wiki/MPs_elected_in_the_UK_general_election,_1987',
         '1983':'http://en.wikipedia.org/wiki/MPs_elected_in_the_United_Kingdom_general_election,_1983',
         '1979':'http://en.wikipedia.org/wiki/MPs_elected_in_the_United_Kingdom_general_election,_1979'}

for wiki in wikis:
	file1 = wikis[wiki][29:]+'.html'
	fh = open(file1, "w")
	webpage = urllib2.urlopen(wikis[wiki]).read()
	fh.write(webpage)
	fh.close()