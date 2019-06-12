This project is Created using [python](https://www.python.org/download/releases/3.0/).

# Weather Man App


A simple app that allows user to generate different report about the weather of Murree

* `Yearly Report` Generate Certain Year Weather Report
* `Monthly Report` Generate Certain Month Weather Report
* `Barchart` Populate Certain Month Weather Bar chart
* `Multiple Reports` Generate above three reports at once


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites

Need to have Python installed.

### Installing

First of all clone the project and change to that directory.

```
git clone https://github.com/arbisoft/the-lab.git
```

No external modules required 


### Starting

You've got project all setup, now all you need to do is start the development server, that will run on port 5000 by default.

```
 python driver.py /path/to/files-dir -e 2002 (for year report)
 python driver.py /path/to/files-dir -a 2002/1 (for month report)
 python driver.py /path/to/files-dir -c 2002/1 (for month barchart + bonus barchart)
 weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011 (Multiple reports) 
```