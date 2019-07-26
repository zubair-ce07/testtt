import keyboard


class TaxiRide:
    def __init__(self):
        self.total_speed = 0

    def speed_state(self):
        if keyboard.is_pressed('up'):
            self.total_speed = self.total_speed + 0.1
        elif keyboard.is_pressed('down'):
            self.total_speed -= 0.1
            if self.total_speed < 0:
                self.total_speed = 0
        return self.total_speed
