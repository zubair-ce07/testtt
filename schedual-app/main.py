from schedualar import candidate, candidates, interviewer, interviewers
from datetime import datetime
import sys

class schedualApplication:
    
    
    def __init__(self):
        self.interviewers_list = interviewers()
        self.candidates_list = candidates()
    
    def show_menu(self):
        print("Press 1 to create/Get interviewer")
        print("Press 2 to create/Get candidate")
        print("press e to exit Application")

    def show_next_menu(self):
        print("Press 1 to set Reservation")
        print("Press 2 to get Reservations")
        print("Press b to go back.")

    def create_interviewer(self):
        name = input("Enter Name :").strip()
        inter_viewer = self.interviewers_list.add_interviewer(name)
        return inter_viewer
    
    def create_candidate(self):
        name = input("Enter name: ").strip()
        one_candidate = self.candidates_list.add_candidate(name)
        return one_candidate

    def input_date(self, prompt_msg, dt_format):
        dt = None
        while dt is None:
            try:
                dt = datetime.strptime(input(prompt_msg), dt_format).date()
            except:
                print("Date is not according to the described formate.")
                dt = None
        return dt

    def input_int(self, prompt_msg):
        value = None
        while value is None:
            try:
                value = int(input(prompt_msg))
                if value < 0 or value > 23:
                    value = None
            except:
                print("Please Enter Valid 24-hour time")
                value = None
        return value

    def set_reservation(self, inter_viewer):
        dt_format = "%d/%m/%Y"
        from_dt = self.input_date("Enter start date formated(d/m/yyyy) : ", dt_format)
        to_dt = self.input_date("Enter end date formated(d/m/yyyy) : ", dt_format)
        from_hour = self.input_int("Enter Start hour 24-formatted : ")
        to_hour = self.input_int("Enter end hour 24-formatted : ")
        days = input("Enter available days monday=1, sunday=7 [comma seperated] :").split(',')
        inter_viewer.set_reservation(from_dt, to_dt, from_hour, to_hour, days)

    def set_availability(self, one_candidate):
        dt_format = "%d/%m/%Y"
        from_dt = self.input_date("Enter start date formated(d/m/yyyy) : ", dt_format)
        to_dt = self.input_date("Enter end date formated(d/m/yyyy) : ", dt_format)
        from_hour = self.input_int("Enter Start hour 24-formatted : ")
        to_hour = self.input_int("Enter end hour 24-formatted : ")
        days = input("Enter available days monday=1, sunday=7 [comma seperated] :").split(',')
        one_candidate.set_availability(from_dt, to_dt, from_hour, to_hour, days)

    def get_reservations(self, inter_viewer):
        reservaton = inter_viewer.get_reservations()
        print(reservaton)

    def get_interviewers(self, names):
        interviewers_list = []
        for name in names:
            inter_viewer = self.interviewers_list.get_interviewer(name)
            if inter_viewer is not None:
                interviewers_list.append(inter_viewer)
        return interviewers_list

    def get_overlapped_days_hours(self, interviewers_list, one_candidate):
        accepted_days = {}
        cand_avail = one_candidate.get_availability()
        days = list(cand_avail.keys())
        for day in days:
            accepted_days[day] = 0
            for inter_viewer in interviewers_list:
                candidate_timing = cand_avail[day]
                inter_viewer_reservation = inter_viewer.get_reservations()
                interviewer_timing = inter_viewer_reservation[day] if day in inter_viewer_reservation else None
                if interviewer_timing is not None:
                    if candidate_timing[0] >= interviewer_timing[0] and candidate_timing[0] < interviewer_timing[1]:
                        accepted_days[day] = accepted_days[day] + 1
                    elif candidate_timing[1] > interviewer_timing[0] and candidate_timing[1] < interviewer_timing[1]:
                        accepted_days[day] = accepted_days[day] + 1
        return accepted_days

    def get_days(self, accepted_days, milestone):

        max_value = max(accepted_days.values())
        days = []
        if max_value == 0 or max_value < milestone or milestone == 0:
            return days
        elif max_value == milestone:
            for key in accepted_days.keys():
                if accepted_days[key] == max_value:
                    days.append(key)
            return days

    def get_overlapped_timing(self, timing1, timing2):

        timing1, timing2 = (timing2.copy(), timing1.copy()) if timing1[0] > timing2[0] else (timing1.copy(), timing2.copy())
        overlap_timing = []
        while timing1[0] < timing1[1] and timing2[0] < timing2[1]:
            if timing1[0] - timing2[0] == 0 : 
                overlap_timing.append(timing1[0])
                overlap_timing.append(timing1[0]+1)
                timing2[0] += 1
            timing1[0] += 1
        return overlap_timing

    def get_availability(self, one_candidate):
        names = input("Enter interviewer name(s) [comma seperaqted] :").split(',')
        interviewers_list = self.get_interviewers(names)
        accepted_days = self.get_overlapped_days_hours(interviewers_list,one_candidate)
        days = self.get_days(accepted_days,len(interviewers_list))
        days_timing = {}
        for day in days:
            cand_timing = one_candidate.get_availability()[day]
            overlapping_time = [cand_timing[0], cand_timing[1]]
            for inter_viewer in interviewers_list:
                overlapping_time = [overlapping_time[0], overlapping_time[len(overlapping_time)-1]]
                interviewer_timing = inter_viewer.get_reservations()[day]
                overlapping_time = self.get_overlapped_timing(overlapping_time, interviewer_timing)

            days_timing[day] = [(overlapping_time[i],overlapping_time[i+1]) for i in range(0,len(overlapping_time),2)]
        return days_timing

    def interviewer_menu(self, inter_viewer):
        
        flag = True
        while flag:
            self.show_next_menu()

            option = input("Enter your Choice ? ")

            if option == "1" :
                self.set_reservation(inter_viewer)
            elif option == "2" :
                self.get_reservations(inter_viewer)
            elif option == "b" :
                flag = False 

    def candidate_menu(self, one_candidate):
        
        flag = True
        while flag:
            self.show_next_menu()

            option = input("Enter your Choice ? ")

            if option == "1" :
                self.set_availability(one_candidate)
            elif option == "2" :
                day_time = self.get_availability(one_candidate)
                print(day_time)
            elif option == "b":
                flag = False

    def start_application(self):
        
        while(True):
            self.show_menu()
            option = input("Enter your Choice ? ")
            if option == "1" :
                inter_viewer = self.create_interviewer()
                self.interviewer_menu(inter_viewer)
            elif option == "2" :
                one_candidate = self.create_candidate()
                self.candidate_menu(one_candidate)
            elif option == "e" : 
                sys.exit(0)

def main():
    schedualApplication().start_application()

if __name__ == "__main__":
    main()
