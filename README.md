### What is weatherman?
**weatherman** generates the weather reports as specified by:

1. command line argument describing the directory name for the data files
2. command line argument specifying the time frame for reports.

Given these, **weatherman**  can generate following reports:

- [-e] For a given year display the highest temperature and day, lowest temperature and day, most humid day and humidity.

- [-a] For a given month display the average highest temperature, average lowest temperature, average mean humidity.

- [-c] For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue.

- Multiple Reports as given above, in one run.

### How to call weatherman?
You can invoke the main "weatherman.py" file using `python3` with the following arguments:


> `> python3 weatherman.py weatherfiles -a 2004/3 ...`

### Known limitations

- If empty strings are passed as arguments, or wrong string (e.g. 13 as month, or 20001 as year), the program may work in unexpected ways. Mostly, that just results in a indexing error at some point during execution.
  
### What do different files do?
  - **weatherman.py**: File to be executed with arguments. Imports multiple classes from **weatherReader.py** to be used in generating reports.
  - **weatherReader.py**: This file contains the weatherReader, calculator and result classes, which are used to store data, calculate results, and store those results respectively
