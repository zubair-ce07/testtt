import datetime

from sqlalchemy.orm import sessionmaker

from models import Jobs, db_connect, create_jobs_table


class JobsPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_jobs_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        item['crawl_id'] = datetime.datetime.now().strftime('%s%f')
        item['crawled_at'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
        job = Jobs(**item)

        try:
            session.add(job)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
