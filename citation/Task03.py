"""Develop a program to find common co-author between any two researchers."""

from dataparser import DataParser


def common_authors(author1, author2):
    global researchpapers

    author1_co = set({})
    author2_co = set({})

    for paper in researchpapers:
        if author1 in paper['author']:
            author1_co.update(paper['author'])
        if author2 in paper['author']:
            author2_co.update(paper['author'])

    author1_co.remove(author1)
    author2_co.remove(author2)

    co_authors = author1_co & author2_co

    return co_authors


researchpapers = DataParser.readandparsefile('citations.txt')

authors_list = set({})
for paper in researchpapers:
    authors_list.update(paper['author'])

authors_list.remove('')
authors_list.remove(' ')

for author1 in authors_list:
    for author2 in authors_list:
        if author2 != author1:
            authors = common_authors(author1, author2)
            if authors:
                result = ', '.join(authors)
                print(author1 + ' - ' + author2 + ' -> ' + result)
