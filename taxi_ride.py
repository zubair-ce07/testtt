import keyboard


class TaxiRide:
    def __init__(self):
        self.total_speed = 0

    def speed_state(self):
        if keyboard.is_pressed('up'):
<<<<<<< HEAD:taxi_ride.py
            self.total_speed = self.total_speed + 0.1
=======

            self.total_speed = self.total_speed + 0.1

>>>>>>> 16854b26792236e47ae79093d3eb042db47d769d:taxi_ride.py
        elif keyboard.is_pressed('down'):
            self.total_speed -= 0.1
            if self.total_speed < 0:
                self.total_speed = 0
<<<<<<< HEAD:taxi_ride.py
=======

>>>>>>> 16854b26792236e47ae79093d3eb042db47d769d:taxi_ride.py
        return self.total_speed
