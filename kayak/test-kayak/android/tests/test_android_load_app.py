# coding=utf-8
"""
    New Landing Test Module
"""
from android.pages.android_flights import AndroidFlights
from common.globals import Globals


class TestAndroidLoadApp(object):
    """
    Load App
    """

    def test_flights_check_text(self, set_capabilities, setup_logging):
        """
               Go to FFD
               Tap Round-trip tab
               Tap Origin Picker
               Type "NYC"
                   Smarty shows "NYC" metro code
                   Smarty shows below: "JFK", "LGA" and "EWR"
               Tap "NYC"
                   Origin field shows "NYC"
               Tap Destination Picker
               Type LAX
                   Smarty shows "LAX" specific airport
               Tap "LAX"
                   Destination field shows "LAX"
               """
        smarty_text_list = ["NYC", "JFK", "LGA", "EWR"]
        origin_code_text = 'NYC'
        destination_code_text = 'LAX'
        Globals(setup_logging)
        android_flights_app = AndroidFlights(set_capabilities, setup_logging)
        assert android_flights_app.flights_launch_app()

        assert android_flights_app.load_flights_tab()
        assert android_flights_app.load_flights_round_trip_tab()

        assert android_flights_app.load_origin_code(origin_text=origin_code_text, smarty_list=smarty_text_list)
        assert android_flights_app.compare_text_origin_code(origin_text=origin_code_text)
        assert android_flights_app.load_destination(destination_text=destination_code_text)
        assert android_flights_app.compare_text_destination_code(destination_text=destination_code_text)

    def test_first_check_text_than_swap(self, set_capabilities, setup_logging):
        """
               Go to FFD
               Tap Round-trip tab
               Set Origin with BOS
                   Origin field shows BOS
               Set Destination SFO
                   Destination field shows SFO
               Tap O/D Swap
                   Origin field shows SFO
                   Destination field shows BOS
        """

        origin_code_text = 'BOS'
        destination_code_text = 'SFO'
        Globals(setup_logging)
        android_flights_app = AndroidFlights(set_capabilities, setup_logging)
        assert android_flights_app.flights_launch_app()

        assert android_flights_app.load_flights_tab()
        assert android_flights_app.load_flights_round_trip_tab()

        assert android_flights_app.load_origin_code(origin_text=origin_code_text)
        assert android_flights_app.compare_text_origin_code(origin_text=origin_code_text)
        assert android_flights_app.load_destination(destination_text=destination_code_text)
        assert android_flights_app.compare_text_destination_code(destination_text=destination_code_text)

        assert android_flights_app.load_swap_button()
        assert android_flights_app.compare_text_origin_code(origin_text=destination_code_text)
        assert android_flights_app.compare_text_destination_code(destination_text=origin_code_text)

    def test_pass_the_value_of_travellers(self, set_capabilities, setup_logging):
        """
        Go to FFD
        Tap Round-trip tab
        Set traveler
        """
        Globals(setup_logging)
        android_flights_app = AndroidFlights(set_capabilities, setup_logging)

        assert android_flights_app.flights_launch_app()

        assert android_flights_app.load_flights_tab()
        assert android_flights_app.load_flights_round_trip_tab()
        android_flights_app.load_traveler_button()
        android_flights_app.flights_traveler_increment_decrement(adult=2, senior=3, youth=3, child=2, infant=2)

