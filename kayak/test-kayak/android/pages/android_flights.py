# coding=utf-8
"""
   Android flights Page
"""
import time

from android.pages import android_elements
from android.pages.android_base_page import AndroidBasePage


class AndroidFlights(AndroidBasePage):
    """
    Load android flight screen
    """

    def _get_launch_app(self):
        """
        Load  Landing screen
        Returns:
            Activity Name: LAUNCH ACTIVITY

        """

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.LAUNCH_ACTIVITY_NAME
        )

    def _reset_app(self):
        """
        Restart  application

        """
        self.driver.reset()

    def _get_skip_button(self):
        """
        get skip login screen button
        Returns:
            web driver element: login screen button
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.login_skip_button
        )

    def _load_skip_login_screen(self):
        """
        load skip button of login screen
        Returns:
            Activity Name: front door activity
        """

        self._get_skip_button().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        ) is not None

    def _get_skip_alert_front_door_screen(self):
        """
        get alert button of search screen
        Returns:
            web driver element: alert button of search screen
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.login_skip_button
        )

    def _load_skip_alert_front_door(self):
        """
        load alert button of search screen

        Returns:
            Activity Name: front door activity
        """

        self._get_skip_alert_front_door_screen().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        ) is not None

    def flights_launch_app(self):
        """
        launch Application
        Returns:
            Activity Name: front door activity
        """
        self._reset_app()
        self._get_launch_app()
        self._load_skip_login_screen()
        self._load_skip_alert_front_door()

        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def _get_main_tabs(self):
        """
        Get all main tabs
        Returns:
            web driver element:all main tabs
        """

        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.front_door_screen_title
        )

    def load_flights_tab(self):
        """
         load flights tab
         Returns:
            Activity Name: front door activity
        """
        self._get_main_tabs()[self.global_contents.second_existence].click()
        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def _get_flights_round_trip_tab(self):
        """
        get fights round trip tab
         Get all main tabs
        Returns:
            web driver element:fights round trip tab
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_round_trip_tab
        )

    def load_flights_round_trip_tab(self):
        """
        selected flight round trip tab
        Returns:
            True if round trip tab is selected
        """

        self._get_flights_round_trip_tab().click()

        return self._get_flights_round_trip_tab().is_selected()

    def _get_search__origin_code_button(self):
        """
        get the search origin code button
        Returns:
            web driver element: origin code button
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_code
        )

    def _get_flights_to_write_text_smarty(self):
        """
        get  the smarty text
         Returns:
            web driver element:  smarty text
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_search_bar
        )

    def _get_flights_first_text_smarty_search(self):
        """
        get the first text of smarty search
         Returns:
            web driver element: first text of smarty search
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.smarty_result_against_search
        )

    def load_origin_code(self, origin_text=None, smarty_list=None):
        """
        load origin code button
        check first three smarty texts if smarty list is available
        compare smarty texts
        load first smarty text
        Returns:
            Activity Name: front door activity
        """

        self._get_search__origin_code_button().click()
        self._get_flights_to_write_text_smarty().send_keys(origin_text)
        if smarty_list is not None:
            assert self._compare_smarty_text_list(smarty_list)
        self._get_flights_first_text_smarty_search().click()

        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def _get_flights_smarty_texts(self):
        """
        get all texts in smarty search
        Returns:
            web driver element: all texts in smarty search
        """

        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.smarty_result_against_search
        )

    def _compare_smarty_text_list(self, smarty_list):
        """
         compare first four  texts in smarty search
         Returns:
            True if all four texts are equal with each other
        """
        search_results = self._get_flights_smarty_texts()
        flag = True
        for i, val in enumerate(smarty_list):
            if search_results[i].text[-4:-1] != val:
                flag = False
        return flag

    def _get_text_from_origin_code(self):
        """
         Get text from origin code
         Returns:
            web driver element:  text from origin code

        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_code
        )

    def compare_text_origin_code(self, origin_text=None):
        """
        compare text with origin code text
         Returns:
            True if both texts are equal with each other
        """

        return self._get_text_from_origin_code().text == origin_text

    def _get_search_destination_code_button(self):
        """
        get the search destination code button
        Returns:
            web driver element: search destination code button
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_destination_code
        )

    def load_destination(self, destination_text=None):
        """
        load destination code button
        write destination text in smarty text
        load first smarty text

        Returns:
            Activity Name: front door activity
        """
        self._get_search_destination_code_button().click()
        self._get_flights_to_write_text_smarty().send_keys(destination_text)
        self._get_flights_first_text_smarty_search().click()

        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def _get_text_from_destination_code(self):
        """
        Get text from destination code
          Returns:
            web driver element: text from destination code


        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_destination_code
        )

    def compare_text_destination_code(self, destination_text=None):
        """
        compare text with destination code text
        Returns:
            True if both texts are equal with each other

        """

        return self._get_text_from_destination_code().text == destination_text

    def _get_swap_button(self):
        """
        get swap button

        Returns:
          Web driver element : swap button

        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_swap
        )

    def load_swap_button(self):
        """
        load swap button

        Returns:
            Activity Name: front door activity
        """
        self._get_swap_button().click()
        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def _get_traveler_button(self):
        """
        get traveler button
         Returns:
          Web driver element :  traveler button
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_travelers
        )

    def load_traveler_button(self):
        """
        load traveler button

        Returns:
            Activity Name: front door activity
        """
        self._get_traveler_button().click()
        return self.global_contents.FLIGHTS_TRAVELER_ACTIVITY == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FLIGHTS_TRAVELER_ACTIVITY
        )

    def _get_traveler_apply_button(self):
        """
        get traveler apply button
        Returns:
           web driver element:  traveler apply button
         """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.apply_button
        )

    def _get_traveller_text_counts(self):
        """
        get values of travelers
        Returns:
            web driver element:  values of travelers
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_travelers_count_value
        )

    def _get_flight_traveller_plus(self):
        """
        get increment button of  traveler
        Returns:
            web driver element:  increment button of  traveler
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_traveller_count_plus
        )

    def _get_flight_traveller_minus(self):
        """
        get decrement button of  traveler
        Returns:
            web driver element:  decrement button of  traveler

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_traveller_count_minus
        )

    def flights_traveler_increment_decrement(self,
                                             adult=0, senior=0,
                                             youth=0, child=0,
                                             infant=0, lap_infant=0):

        """
        perform all increment and decrement of traveler
         Returns:
            Activity Name: traveler activity

        """
        traveler_member_list = [adult, senior, youth, child, infant, lap_infant]
        for i in range(5):
            if traveler_member_list[i] != 0:
                already_traveler_value = int(self._get_traveller_text_counts()[i].text)
                new_traveler_value = traveler_member_list[i]
                if already_traveler_value > new_traveler_value:
                    for _ in range(already_traveler_value - new_traveler_value):
                        self._get_flight_traveller_minus()[i].click()
                elif new_traveler_value > already_traveler_value:
                    for _ in range(new_traveler_value - already_traveler_value):
                        self._get_flight_traveller_plus()[i].click()
                time.sleep(self.global_contents.medium_timeout)
        self._get_traveler_apply_button().click()
        return self.global_contents.FRONT_DOOR_ACTIVITY_NAME == self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

