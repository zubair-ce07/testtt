"""Produce a list of co-authors of each author in the given input file. """

from dataparser import DataParser


def get_co_authors(author):
    global researchpapers

    co_authors = set({})

    for paper in researchpapers:
        if author in paper['author']:
            co_authors.update(paper['author'])

    co_authors.remove(author)
    return co_authors


researchpapers = DataParser.readandparsefile('citations.txt')

for paper in researchpapers:
    for author in paper['author']:
        co_authors = get_co_authors(author)
        if co_authors:
            string = ', '.join(co_authors)
            print(author + ' -> ' + string)
