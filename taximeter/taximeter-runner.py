#! usr/bin/python3
import time

import keyboard

from config import Configurations as Config
from ride import Ride


def attatch_listeners_to_keystroke(ride):
    keyboard.add_hotkey('e', ride.end_ride)
    keyboard.add_hotkey('shift+e', ride.end_ride)
    keyboard.add_hotkey('p', ride.pause_ride)
    keyboard.add_hotkey('shift+p', ride.pause_ride)
    keyboard.add_hotkey('r', ride.resume_ride)
    keyboard.add_hotkey('shift+r', ride.resume_ride)
    keyboard.add_hotkey('up', ride.increase_speed)
    keyboard.add_hotkey('down', ride.decrease_speed)


def main():
    input('Press any key to start the ride.')
    take_ride = Ride()
    take_ride.resume_ride()
    attatch_listeners_to_keystroke(take_ride)

    while True:
        time.sleep(Config.SLEEPING_INTERVAL)
        take_ride.update_ride_time()

        if take_ride.ride_state == Config.RIDE_END_STATE:
            break

    take_ride.display_ride_stats()
    keyboard.wait('esc')


if __name__ == '__main__':
    main()
