import json
from re import findall
from datetime import datetime, date, time

from asiangames.models import *


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def month_to_number(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month)+1


if __name__ == '__main__':
    db.create_all()

    with open('json/medals.json') as medals_file:

        for medal_data in json.load(medals_file):
            for sport_medal in medal_data['sport_medals']:
                country_record = get_or_create(db.session, Country, name=medal_data['name'])

                sport_country_medal_record = SportCountryMedals(
                    gold=sport_medal['gold'], silver=sport_medal['silver'],
                    bronze=sport_medal['bronze']
                )

                sport_country_medal_record.sport = get_or_create(db.session, Sport, name=sport_medal['name'])
                country_record.medals.append(sport_country_medal_record)
                db.session.add(country_record)
                print('Completed {}\'s {}'.format(medal_data['name'], sport_medal['name']))
        db.session.commit()

    with open('json/athletes.json') as athletes_file:

        for athlete_data in json.load(athletes_file):
            sport_record = get_or_create(db.session, Sport, name=athlete_data['sport'])
            country_id = get_or_create(db.session, Country, name=athlete_data['country'])._id

            athlete_record = Athlete(_id=athlete_data['id'], name=athlete_data['name'], img_url=athlete_data['img_url'],
                                     height=athlete_data['height'], weight=athlete_data['weight'],
                                     age=athlete_data['age'], born_date=athlete_data['born_date'],
                                     born_city=athlete_data['born_city'], country_id=country_id)

            athlete_record.sports.append(sport_record)
            db.session.add(athlete_record)
            print('Completed adding Athlete {}'.format(athlete_data['name']))
        db.session.commit()

    with open('json/sports.json') as sports_file:

        numeric_regex = r'(\d+)'

        for sport_data in json.load(sports_file):

            sport_record = get_or_create(db.session, Sport, name=sport_data['name'])

            for schedule in sport_data['schedules']:
                schedule_date = list(schedule.keys())[0]
                sch_day, sch_date, sch_month = schedule_date.split(' ')
                final_date = date(2018, month_to_number(sch_month[0:3]), int(findall(numeric_regex, sch_date)[0]))

                for scheduled_event in schedule[schedule_date]:
                    if scheduled_event['time']:
                        sch_hours, sch_minutes = findall(numeric_regex, scheduled_event['time'])
                        final_date = datetime.combine(final_date, time(int(sch_hours), int(sch_minutes)))

                    schedule_record = Schedule(daytime=final_date, phase=scheduled_event['phase'],
                                               event=scheduled_event['event'], sport=sport_record)

                    db.session.add(schedule_record)
                    print('Completed Schedule {} for {}'.format(scheduled_event['event'], sport_record.name))
        db.session.commit()
