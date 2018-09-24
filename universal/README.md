Universal scraper
=======

The project includes `universal` scraper to scrap complete www.universal.at products.

## Getting Started

1. Clone this repo on your local machine.
1. Assuming you are having Python 3.5 already in your machine.
1. Setup environment:
    1. cd whistles
    1. virtualenv -p python3.5 ~/.virtualenvs/universal_scraper
    1. source ~/.virtualenvs/universal_scraper/bin/activate
    1. pip install -r requirements.txt
1. Run scraper:
    1. scrapy crawl whistles -o whistles.json
1. To clean environment following commands can be used:
    1. deactivate
    1. rm -rf ~/.virtualenvs/universal_scraper
    1. find . -name "*.pyc" -exec rm -f {} \;