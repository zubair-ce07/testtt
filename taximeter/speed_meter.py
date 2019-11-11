from config import Configurations as Config


class SpeedMeter(object):
    def __init__(self, *args, **kwargs):
        super(SpeedMeter, self).__init__()
        self.current_speed = 0

    def increase_speed(self):
        self.current_speed += Config.CHANGE_IN_SPEED
        print(f'\rSpeed increased to {self.current_speed}m/sec')

    def decrease_speed(self):
        if self.current_speed <= 0:
            print('Speed can not be less then 0m/sec')
            return

        self.current_speed -= Config.CHANGE_IN_SPEED
        print(f'\rSpeed decreased to {self.current_speed}m/sec')
