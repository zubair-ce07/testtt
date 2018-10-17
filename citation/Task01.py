"""
Count the number of papers published during four time-periods: 1980-1990, 1991-2000, 2001-2010 and 2011-today.
"""

from dataparser import DataParser

researchpapers = DataParser.readandparsefile('citations.txt')

# For papers in time periods
n1980 = 0
n1991 = 0
n2001 = 0
n2011 = 0

for paper in researchpapers:
    if 1980 <= int(paper['date']) <= 1990:
        n1980 += 1
    elif 1991 <= int(paper['date']) <= 2000:
        n1991 += 1
    elif 2001 <= int(paper['date']) <= 2010:
        n2001 += 1
    elif 2011 <= int(paper['date']) <= 2018:
        n2011 += 1

print("1980-1990 -> ", n1980)
print("1991-2000 -> ", n1991)
print("2001-2010 -> ", n2001)
print("2011-today -> ", n2011)
