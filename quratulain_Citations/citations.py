from collections import defaultdict
import itertools
import codecs
import re


class Citations:
    citations = []

    def read_file(self, file_name):
        with codecs.open(file_name, encoding='iso-8859-1', mode='r') as open_file:
            file_text = open_file.read()
            records = self.arrange_records(file_text)

            for record in records:
                cite = self.process_record(record)
                self.citations.append(cite)

        print(self.citations)

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
        records = re.split('(#[\*|@|t|c]|#index)', record)
        pairs = zip(records[1::2], records[2::2])
        return {key: value for key, value in pairs}

    def count_published_paper(self, start_year, end_year):
        return sum(start_year <= cite['year'] <= end_year for cite in self.citations)

    def count_published_papers(self, duration):
        return [self.count_published_paper(start_year, end_year) for start_year, end_year in
                duration]

    def generate_records_per_year(self):
        """ :return: [(author, year)] """
        records = []
        for cite in self.citations:
            for author in cite.get('author'):
                records.append((author, cite.get('year')))
        return records

    def print_papers_published_percentage(self):
        records = self.generate_records_per_year()

        for author, year in records:
            publications, author_occurrence = 0, 0
            for author_compare, year_to_compare in records:
                if author == author_compare:
                    author_occurrence += 1
                    if year == year_to_compare:
                        publications += 1

            print("{}, {} -> {}%".format(author, year, int(publications / author_occurrence * 100)))

    def find_authors(self):
        coauthors = defaultdict(set)
        for cite in self.citations:
            for author, coauthor in itertools.permutations(cite['author'], 2):
                coauthors[author].add(coauthor)
        return coauthors

    def print_common_authors(self):
        authors_records = self.find_authors()
        pairs = itertools.combinations(authors_records.keys(), 2)
        for pair in pairs:
            common = set(authors_records[pair[0]]) & set(authors_records[pair[1]])
            if common:
                print("%s -> %s" % (', '.join(pair), ', '.join(common)))

    def print_published_papers_count(self, durations):
        for index, duration in enumerate(durations):
            start, end = duration[0], duration[1]
            print(" {}, {} -> {}".format(str(start), str(end),
                                         self.count_published_paper(start, end)))

    @staticmethod
    def print_authors(authors):
        for author, coauthor in authors.items():
            print("{} : {}".format(author, ', '.join(coauthor)))
