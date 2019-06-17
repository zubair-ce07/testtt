class Utils:
    def convert_distance_into_km(self, ride_distance):
        return ride_distance / 1000

    def convert_time_into_minutes(self, ride_wait_time):
        return ride_wait_time / 1000

    def show_scalled_ride_time(self, identifier, ride_time):
        if ride_time < 60:
            print(f"{identifier}: {ride_time} Seconds")
        else:
            print(f"{identifier}: {ride_time//60} Minutes {ride_time % 60} "
                  f"Seconds")

    def show_scalled_ride_distance(self, ride_distance):
        if ride_distance < 1000:
            print(f"Distance: {ride_distance} Meters")
        else:
            print(f"Distance: {ride_distance//1000} KM"
                  f" {ride_distance % 1000} "
                  f"Meters")
