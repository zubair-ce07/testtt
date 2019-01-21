import argparse
import re
from datetime import datetime


def read_citations(file_name):
    with open(file_name, errors='ignore') as citations:
        incomplete_row = ''
        rows = []
        for row in citations:
            if row.strip() and is_row_complete(incomplete_row + row):
                rows.append(parse_citation(incomplete_row + row))
                incomplete_row = ''
            elif not is_row_complete(incomplete_row + row):
                incomplete_row = row
        return rows


def is_row_complete(row):
    return '#*' in row and '#@' in row and '#t' in row and '#index' in row


def parse_citation(row):
    columns = re.split(r'(#\*|#@|#c|#t|#index)', row)
    title = authors = year = ''
    for index in range(1, len(columns), 2):
        if not columns[index+1]:
            continue

        if '#*' in columns[index]:
            title = columns[index + 1].strip()
        elif '#@' in columns[index]:
            authors = columns[index + 1].split(',')
        elif '#t' in columns[index]:
            year = int(columns[index + 1].strip())
    authors = [author.strip() for author in authors]
    row = {'title': title, 'authors': authors, 'year': year}
    return row


def count_citations(citations, time_period):
    if len(time_period) == 1:
        research_papers = [cite for cite in citations if cite.get('year') == time_period[0]]
        print('{} research paper is published in {}'.format(len(research_papers), time_period[0]))
    elif len(time_period) == 2:
        research_papers = [cite for cite in citations if
                           time_period[0] <= cite.get('year') <= time_period[1]]
        print('{} research paper is published between {}-{}'.format(
            len(research_papers), time_period[0], time_period[1]))


def find_co_authors(research_wise_author, authors):
    research_wise_co_authors = [research_authors for research_authors in research_wise_author
                                if authors_in_research(research_authors, authors)]
    if research_wise_co_authors:
        all_co_authors = set(sum(research_wise_co_authors, []))
        [all_co_authors.remove(author) for author in authors]
        return authors, all_co_authors


def authors_in_research(research_authors, authors):
    is_auth_in_research = True
    for author in authors:
        if author not in research_authors:
            is_auth_in_research = False
    return is_auth_in_research


def show_co_authors(co_authors):
    if co_authors:
        author_separator_symbol = {0: '- ', 1: ', '}
        for index, co_author in enumerate(co_authors):
            [print(author, end=author_separator_symbol.get(index)) for author in co_author
             if author]
            if index == 0 and co_author[index]:
                print('\b> ', end='')
        print('\b\b')
    else:
        print('{} and {} are not common authors'.format(args.authors[0], args.authors[1]))


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', default='citation.txt', help='Enter file name')
    parser.add_argument('-r', '--range', type=validate_range, default=1999,
                        help='To count the research paper published in specific time period,'
                             'enter range in format  in yyyy-yyyy')
    parser.add_argument('-a', '--authors', type=validate_authors,
                        default='Arthur Greef,Michael Fruergaard Pontoppidan',
                        help='Enter any two authors to find common co-authors author1,author2')
    return parser.parse_args()


def validate_range(range_text):
    boundaries = range_text.split('-')
    try:
        boundaries = [datetime.now().year if 'today' == bound else int(bound)
                      for bound in boundaries]
        return boundaries
    except:
        raise argparse.ArgumentTypeError('Please enter a valid range like 1989-2000')


def validate_authors(authors):
    authors = authors.split(',')
    if len(authors) == 2:
        if not authors[0] in authors[1]:
            return authors
        else:
            raise argparse.ArgumentTypeError('Please enter two different authors')
    else:
        raise argparse.ArgumentTypeError('Please enter two authors in format author1,author2')


if __name__ == "__main__":
    args = get_arguments()
    citation = read_citations(args.file_name)
    research_wise_authors = [reading.get('authors') for reading in citation]
    if args.range:
        count_citations(citation, args.range)
    if args.authors:
        print('\n\n\t\tCo_authors between two authors')
        common_co_authors = find_co_authors(research_wise_authors, args.authors)
        show_co_authors(common_co_authors)
    print('\n\n\t\tCo_authors of all authors')
    authrs = set(sum(research_wise_authors, []))
    co_authors_of_all = [find_co_authors(research_wise_authors, [author]) for author in authrs]
    [show_co_authors(co_authors) for co_authors in co_authors_of_all]
