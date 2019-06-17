""" This file contains the ReportContainer class
    with a member list variable, and helper member
    functions that add, print and clear reports from
    the list

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""


def date_translation(date):
    if date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
    else:
        return None
    if date_object:
        return datetime.strftime(date_object, '%B %d')
    else:
        return None


class ReportContainer:
    report_list = []

    def add_report(self, result_type, value, date):
        self.report_list.append({'type': result_type,
                                 'value': value,
                                 'date': date})

    def clear_reports(self):
        self.report_list.clear()

    def print_reports(self):
        for result in self.report_list:
            character = 'C'
            if 'Humidity' in result['type']:
                character = '%'

            if result['date']:
                print(result['type'], ': ',
                      result['value'], character, ' on ',
                      date_translation(result['date']),
                      sep='')
            else:
                print(result['type'], ': ',
                      result['value'], character,
                      sep='')
