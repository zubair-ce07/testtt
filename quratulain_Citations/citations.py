from collections import Counter
import itertools
import codecs
import re


class Citations:
    def __init__(self):
        self.citations = []
        self.regex = re.compile('(#[@tc\*]|#index)')

    def read_file(self, file_name):
        with codecs.open(file_name, encoding='iso-8859-1', mode='r') as open_file:
            file_text = open_file.read()
            records = self.arrange_records(file_text)

            for record in records:
                cite = self.process_record(record)
                self.citations.append(cite)

    def arrange_records(self, file_text):
        return list(map(lambda x: '#*' + x, file_text.split('#*')[1:]))

    def process_record(self, record):
        values = self.extract_value(record)
        return {

            'title': values.get('#*'), 'year': int(values.get('#t')), 'venu': values.get('#c'),
            'index': int(values.get('#index')),
            'author': [element.strip() for element in values.get('#@').split(',') if
                       element.strip() != '']}

    def extract_value(self, record):
        records = self.regex.split(record)
        return dict(zip(records[1::2], records[2::2]))

    def count_published_paper(self, start_year, end_year):
        return sum(start_year <= cite['year'] <= end_year for cite in self.citations)

    def count_published_paper_per_year_author(self, year, author):
        return sum(year == cite['year'] and author in cite['author'] for cite in self.citations)

    def generate_records_per_year(self):
        """ :return: {{author: {year:<2006>,year:<2007>}} """
        records = {}
        for cite in self.citations:
            for author in cite.get('author'):
                year = cite.get('year')
                records.setdefault(author, dict()).update(
                    {year: self.count_published_paper_per_year_author(year, author)})
        return records

    def print_papers_published_percentage(self):
        records = self.generate_records_per_year()
        for author, years in records.items():
            for year, publications in years.items():
                percentage = int(publications / len(years) * 100)
                print("{}, {} -> {}%".format(author, year, percentage))

    def find_co_authors(self):
        coauthors = {}
        for cite in self.citations:
            for author, coauthor in itertools.permutations(cite['author'], 2):
                coauthors.setdefault(author, set()).add(coauthor)
        return coauthors

    def print_common_authors(self):
        authors_records = self.find_co_authors()
        pairs = itertools.combinations(authors_records.keys(), 2)
        for pair in pairs:
            common = set(authors_records[pair[0]]) & set(authors_records[pair[1]])
            if common:
                print("%s -> %s" % (', '.join(pair), ', '.join(common)))

    def print_published_papers_count(self, durations):
        for start, end in durations:
            print(" {}, {} -> {}".format(str(start), str(end),
                                         self.count_published_paper(start, end)))

    @staticmethod
    def print_co_authors(authors):
        for author, coauthor in authors.items():
            print("{} : {}".format(author, ', '.join(coauthor)))

