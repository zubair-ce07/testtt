from datetime import datetime
from datetime import timedelta


class reservation:

    def __init__(self):
        self.available = {}

    def set_reservations(self, from_dt, to_dt,from_hour, to_hour, days):
        fr_date = from_dt
        to_date = to_dt
        while fr_date <= to_date:
            if str(fr_date.isoweekday()) in days:
                if fr_date in self.available:
                    prev = self.available[fr_date]
                    if from_hour < prev[0]:
                        prev[0] = from_hour
                    if to_hour > prev[1]:
                        prev[1] = to_hour
                    self.available[fr_date] = prev
                else:
                    self.available[fr_date] = [from_hour, to_hour]
            fr_date = fr_date + timedelta(days=1)

class candidate:
    
    def __init__(self):
        self.availability = reservation()

    def set_availability(self, from_dt, to_dt, from_hour, to_hour, days):
        self.availability.set_reservations(from_dt, to_dt, from_hour, to_hour, days)
    
    def get_availability(self):
        return self.availability.available


class candidates:
    
    candidates = {}

    def __init(self):
        pass
    
    def add_candidate(self, name):
        if name in self.candidates:
            print("Returning existing candidate")
            return self.candidates[name]
        else:
            self.candidates[name] = candidate()
            return self.candidates[name]

    def get_candidate(self, name):
        if name in self.candidates:
            return self.candidates[name]
        else:
            return None

class interviewer:
    
    def __init__(self):
        self.availability = reservation()

    def set_reservation(self, from_dt, to_dt, from_hour, to_hour, days):
        self.availability.set_reservations(from_dt, to_dt, from_hour, to_hour, days)
    
    def get_reservations(self):
        return self.availability.available

class interviewers:

    interviewers = {}

    def __init__(self):
        pass

    def add_interviewer(self, name):
        if name in self.interviewers:
            print("Returning existing interviewer")
            return self.interviewers[name]
        else:
            self.interviewers[name] = interviewer()
            return self.interviewers[name]

    def get_interviewer(self, name):
        if name in self.interviewers:
            return self.interviewers[name]
        else:
            return None
