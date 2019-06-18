class Utils:
    @staticmethod
    def convert_meters_into_km(ride_distance):
        return ride_distance / 1000

    @staticmethod
    def convert_seconds_into_minutes(ride_wait_time):
        return ride_wait_time / 1000

    @staticmethod
    def show_scaled_ride_time(time_type_identifier, ride_time):
        if ride_time < 60:
            print(f"{time_type_identifier}: {ride_time} Seconds")
        else:
            print(f"{time_type_identifier}: {ride_time//60} Minutes {ride_time % 60} Seconds")

    @staticmethod
    def show_scaled_ride_distance(ride_distance):
        if ride_distance < 1000:
            print(f"Distance: {ride_distance} Meters")
        else:
            print(f"Distance: {ride_distance//1000} KM {ride_distance % 1000} Meters")
