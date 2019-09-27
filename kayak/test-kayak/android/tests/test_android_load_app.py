# coding=utf-8
"""
    New Landing Test Module
"""

from common.globals import Globals
from android.pages.android_load_app import AndroidLoadApp


class TestAndroidLoadApp(object):

    """
    Load App
    """

    def test_check_origin_text(self, set_capabilities, setup_logging):

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
        global_contents = Globals(setup_logging)
        android_load_app = AndroidLoadApp(set_capabilities, setup_logging)

        assert android_load_app.on_screen() == global_contents.LAUNCH_ACTIVITY_NAME
        assert android_load_app.skip_login_screen() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.skip_alert_front_door() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.load_flights_round_trip_tab()
        assert (global_contents.FRONT_DOOR_ACTIVITY_NAME
                == android_load_app.flights_select_departure("NYC", "yes"))
        assert android_load_app.compare_text_departure("NYC")
        assert (android_load_app.flights_select_destination("LAX")
                == global_contents.FRONT_DOOR_ACTIVITY_NAME)
        assert android_load_app.compare_text_destination("LAX")
        assert (android_load_app.flights_search_button()
                == global_contents.SEARCH_FLIGHT_RESULT_ACTIVITY)

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

        global_contents = Globals(setup_logging)
        android_load_app = AndroidLoadApp(set_capabilities, setup_logging)
        android_load_app.reset_app()
        assert android_load_app.on_screen() == global_contents.LAUNCH_ACTIVITY_NAME
        assert android_load_app.skip_login_screen() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.skip_alert_front_door() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.load_flights_round_trip_tab()
        assert (android_load_app.flights_select_departure("BOS", "no")
                == global_contents.FRONT_DOOR_ACTIVITY_NAME)
        assert android_load_app.compare_text_departure("BOS")
        assert (android_load_app.flights_select_destination("SFO")
                == global_contents.FRONT_DOOR_ACTIVITY_NAME)
        assert android_load_app.compare_text_destination("SFO")
        assert android_load_app.flights_swap_button()
        assert android_load_app.compare_text_departure("SFO")
        assert android_load_app.compare_text_destination("BOS")

    def test_pass_value_of_traveller(self, set_capabilities, setup_logging):
        """
         set traveler
        """
        global_contents = Globals(setup_logging)
        android_load_app = AndroidLoadApp(set_capabilities, setup_logging)
        android_load_app.reset_app()
        assert android_load_app.on_screen() == global_contents.LAUNCH_ACTIVITY_NAME
        assert android_load_app.skip_login_screen() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.skip_alert_front_door() == global_contents.FRONT_DOOR_ACTIVITY_NAME
        assert android_load_app.load_flights_round_trip_tab()
        android_load_app.flights_select_traveler()
        android_load_app.flights_traveler_increment_decrement(adult=3, senior=0, youth=1)
