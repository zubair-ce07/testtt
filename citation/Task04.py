"""Produce a list of co-authors of each author in the given input file. """

from dataparser import DataParser

researchpapers = DataParser.readandparsefile('citations.txt')

authors_list = set({})
for paper in researchpapers:
    authors_list.update(paper['author'])

authors_list.remove('')
authors_list.remove(' ')

years = []
for author in authors_list:
    for paper in researchpapers:
        if author in paper['author']:
            years.append(paper['date'])

    temp = []
    for year in years:
        if year not in temp:
            percentage = (years.count(year) / len(years)) * 100
            print(author + ', ' + str(year) + ' -> ' + str(int(percentage)) + '%')
            temp.append(year)

    years = []
    print()
