from collections import defaultdict
from datetime import datetime
import itertools
import codecs
import re


class Citations:
    citations = []

    def read_file(self, file_name):
        cite = {}
        with codecs.open(file_name, encoding='iso-8859-1', mode='r') as open_file:
            rough_records = open_file.readlines()
            records = ''.join(rough_records).replace("\r\n", "").split("*")

            for record in records[1:]:
                record_list = record.split('#')[:-1]

                for index, element in enumerate(record_list):
                    if index == 0:
                        cite['title'] = element
                    elif element[0] == 't':
                        cite['year'] = int(element[1:])
                    elif element == 'c':
                        cite['publication'] = element
                    elif element[0] == 'index':
                        cite['index'] = re.split('(\D+)', element)[-1]
                    elif element[0] == '@':
                        cite['author'] = [element.strip() for element in element[1:].split(',') if
                                          element.strip() != '']

                self.citations.append(cite)
                cite = {}

    def count_published_paper(self, start_year, end_year):
        years = [cite['year'] for cite in self.citations if start_year <= cite['year'] <= end_year]
        return len(years)

    def count_published_papers(self, duration):
        total_counts = [self.count_published_paper(start_year, end_year) for start_year, end_year in
                        duration]
        return sum(total_counts)

    def papers_published_per_year(self):
        records, publications = [], []
        for cite in self.citations:
            for author in cite.get('author'):
                records.append((author, cite.get('year'), cite.get('publication')))

        for index, record in enumerate(records):
            publications = [record[2] for r in records[index:] if
                            record[0] == r[0] and record[1] == r[1]]
            percentage = len(list(filter(None, publications))) / 100 * 100
            print("{}, {} -> {}%".format(record[0], record[1], int(percentage)))

    def find_authors(self):
        coauthors = defaultdict(set)
        for citation in self.citations:
            for author, coauthor in itertools.permutations(citation['author'], 2):
                coauthors[author].add(coauthor)
        return coauthors

    def print_common_authors(self):
        authors_records = self.find_authors()
        pairs = itertools.combinations(authors_records.keys(), 2)
        for pair in pairs:
            coauthor1 = authors_records[pair[0]]
            coauthor2 = authors_records[pair[1]]
            common = set(coauthor1) & set((coauthor2))
            if common:
                print("%s -> %s" % (','.join(pair), ','.join(common)))


if __name__ == '__main__':
    citation = Citations()
    citation.read_file("citation.txt")

    # Task 1
    now = datetime.now()
    duration_list = [(1980, 1990), (1991, 2000), (2001, 2010), (2011, now.year)]
    count = citation.count_published_papers(duration_list)
    output_duration = ', '.join('{}-{}'.format(*el) for el in duration_list)
    print('Count of published papers for %s is %d' % (output_duration, count))

    # Task 2
    print("\n Authors: \n")
    authors = citation.find_authors()
    print(authors)

    # Task 3
    print("\n Common Co-Authors \n")
    citation.print_common_authors()

    # Task 4
    print("\n Papers Published \n")
    citation.papers_published_per_year()
