from citations import Citations
from datetime import datetime

if __name__ == '__main__':
    citation = Citations()
    citation.read_file("citation.txt")

    # Task 1
    print("\n Published Papers Count: \n")
    now = datetime.now()
    duration_list = [(1980, 1990), (1991, 2000), (2001, 2010), (2011, now.year)]
    citation.print_published_papers_count(duration_list)

    # Task 2
    print("\n Authors List: \n")
    authors_list = citation.find_co_authors()
    citation.print_co_authors(authors_list)

    # Task 3
    print("\n Common Co-Authors \n")
    citation.print_common_authors()

    # Task 4
    print("\n Papers Published \n")
    citation.print_papers_published_percentage()
