# coding=utf-8
"""
    New Landing Page Module
"""
import time

from android.pages import android_elements
from android.pages.android_base_page import AndroidBasePage


class AndroidLoadApp(AndroidBasePage):
    """
    New Landing screen
    """

    def on_screen(self):
        """
        Load New Landing screen

        Returns:
            str: New Landing screen Activity Name
        """

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.LAUNCH_ACTIVITY_NAME
        )

    def reset_app(self):
        """
        reset application

        """
        self.driver.reset()

    def get_search_button(self):
        """Get edX logo
        Returns:
        web driver element: Logo element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.search_button
        )

    def get_skip_button(self):
        """
        Get edX logo
        Returns:
            webdriver element: Logo element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.login_skip_button
        )

    def skip_login_screen(self):
        """Get welcome message text
            Returns:
            web driver element: Welcome Message element
        """

        self.get_skip_button().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def get_skip_alert_front_door_screen(self):
        """
        Get edX logo
        Returns:
            web driver element: Logo element
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.login_skip_button
        )

    def skip_alert_front_door(self):
        """
        Get edX logo
        Returns:
            web driver element: Logo element
        """

        self.get_skip_alert_front_door_screen().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def get_text_from_origin_code(self):
        """
            Get text from origin code
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_code
        )

    def compare_text_departure(self, txt):
        """
            compare text
        """

        return self.get_text_from_origin_code().text == txt

    def get_text_to_destination(self):
        """
            Get text from origin code
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_destination_code
        )

    def compare_text_destination(self, txt):
        """
            compare text
        """

        return self.get_text_to_destination().text == txt

    def get_flights_swap_button(self):
        """
        click swap button

        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_swap_button
        )

    def flights_swap_button(self):
        """
        click swap button

        """
        self.get_flights_swap_button().click()

        return self.get_flights_swap_button().is_enabled()

    def flights_from_button_click(self):
        """
       get the field

        Returns:
            webdriver element: origin code
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_code
        )

    def flights_to_button_click(self):
        """
       get the field

        Returns:
            webdriver element: location from
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_destination_code
        )

    def date_button_click_open_calender(self):
        """
         click open calender
         Returns:
         webdriver element: calender
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_dates
        )

    def date_day_calender(self):
        """
         click open calender
         Returns:
         webdriver element: calender
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.date_25_september
        ).click()

    def apply_selected_date(self):
        """
         click open calender
         Returns:
         webdriver element: calender
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.date_25_september
        )

    def flights_from_text_write(self, txt):
        """
              text to  find

              Returns: search result
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_search_bar
        ).send_keys(txt)

    def flights_from_select_text_enter(self):
        """
            enter first result of search
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.first_result_againts_search
        )

    def get_flights_smarty_texts(self):
        """
        get all texts in

        """

        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.first_result_againts_search
        )

    def get_flights_departure_time(self):
        """

        get all departure times
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_departure_time
        )

    def get_flights_arrival_time(self):
        """

        get all arrival times
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_arrival_time
        )

    def get_flights_duration(self):
        """

        get all duration
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_container_duration_id
        )

    def get_flights_price(self):
        """

          get all prices
        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_price
        )

    def get_flights_departure_airport_code(self):
        """

         get all dep airport codes

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_origin_code
        )

    def get_flights_arrival_airport_code(self):
        """

        get all arrival airport codes

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_destination_code
        )

    def get_flights_traveler(self):
        """
        open traveler select activity

        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_travelers
        )

    def flights_select_traveler(self):
        """
        select traveler

        """
        self.get_flights_traveler().click()

    def get_flights_traveller_get_text_count(self):
        """
        get values of traveler

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_travelers_count_value
        )

    def get_flight_traveller_click_plus(self):
        """
        increment the traveler

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_search_traveller_limit
        )

    def get_flight_traveller_click_negative(self):
        """
        decrement the traveler

        """
        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.flights_traveller_count_negative
        )

    def get_flights_traveller_set_count_plus(self, count, index_of_count):
        """
        click count increment

        """
        for _ in range(count):
            self.get_flight_traveller_click_plus()[index_of_count].click()

    def get_flights_traveller_set_count_negative(self, count, index_of_count):
        """
        click count decrement

        """
        for _ in range(count):
            self.get_flight_traveller_click_negative()[index_of_count].click()

    def get_flights_traveller_who_is_greater(self, first, second, index_of_count):
        """
        compare  to do increment or decrement

        """
        if second > first:
            self.get_flights_traveller_set_count_negative(second - first, index_of_count)
        elif first > second:
            self.get_flights_traveller_set_count_plus(first, index_of_count)

    def flights_traveler_increment_decrement(self,
                                             adult=0, senior=0,
                                             youth=0, child=0,
                                             infant=0, lap_infant=0):
        """
        perform all increment and decrement

        """

        time.sleep(3)

        self.get_flights_traveller_who_is_greater(
            adult,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.first_existence].text),
            self.global_contents.first_existence
        )
        self.get_flights_traveller_who_is_greater(
            senior,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.second_existence].text),
            self.global_contents.second_existence
        )
        self.get_flights_traveller_who_is_greater(
            youth,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.third_existence].text),
            self.global_contents.third_existence
        )
        self.get_flights_traveller_who_is_greater(
            child,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.fourth_existence].text),
            self.global_contents.fourth_existence
        )
        self.get_flights_traveller_who_is_greater(
            infant,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.fifth_existence].text),
            self.global_contents.fifth_existence
        )
        self.get_flights_traveller_who_is_greater(
            lap_infant,
            int(self.get_flights_traveller_get_text_count()
                [self.global_contents.sixth_existence].text),
            self.global_contents.sixth_existence
        )

    def flights_smarty_texts(self):
        """
         all texts smarty text field
         Returns:

          check all

        """
        return self.get_flights_smarty_texts()

    def flights_select_departure(self, txt, text):
        """
             text

                Returns:
                    web driver  element: text
        """
        self.flights_from_button_click().click()
        self.flights_from_text_write(txt)

        if text == "yes":
            assert self.flights_smarty_texts()[1].text == "New York, NY - John F Kennedy Intl (JFK)"
            assert self.flights_smarty_texts()[2].text == "New York, NY - LaGuardia (LGA)"
            assert self.flights_smarty_texts()[3].text == "Newark, NJ - Newark (EWR)"

        time.sleep(3)

        self.flights_from_select_text_enter().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def flights_to_write_text_origin(self, txt):
        """


                Returns:
                     text
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_search_bar
        ).send_keys(txt)

    def get_flights_select_text_smarty_search(self):
        """


                Returns:
                    web driver element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.first_result_againts_search
        )

    def flights_select_destination(self, txt):
        """
             text

                Returns:
                   activity name
        """
        self.flights_to_button_click().click()
        self.flights_to_write_text_origin(txt)
        time.sleep(3)
        self.get_flights_select_text_smarty_search().click()
        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def get_main_tabs(self):
        """
        Get Search Courses icon

        Returns:
            web driver element: Search Courses icon element
        """

        return self.global_contents.get_all_views_on_screen_by_id(
            self.driver,
            android_elements.front_door_screen_title
        )

    def load_hotels_tab(self):
        """
        Get Search Courses edit field

        Returns:
            web driver element: Search Courses edit field element
        """
        self.get_main_tabs()[self.global_contents.first_existence].click()

    def load_flights_tab(self):
        """
        Get Search Courses edit field

        Returns:
            web driver element: Search Courses edit field element
        """
        self.get_main_tabs()[self.global_contents.second_existence].click()

    def load_cars_tab(self):
        """
        Get Search Courses edit field

        Returns:
            web driver element: Search Courses edit field element
        """
        self.get_main_tabs()[self.global_contents.third_existence].click()

    def get_flights_one_way_tab(self):
        """
        Get edX logo
        Returns:
            webdriver element: Logo element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_oneway_tab
        )

    def load_flights_one_way_tab(self):
        """
        Get edX logo
        Returns:
            webdriver element: Logo element
        """

        self.get_flights_one_way_tab().click()

    def get_flights_round_trip_tab(self):
        """
        Get edX logo
        Returns:
            web driver element: Logo element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_round_trip_tab
        )

    def load_flights_round_trip_tab(self):
        """
        Get edX logo
        Returns:
            web driver element: Logo element
        """

        self.get_flights_round_trip_tab().click()

        return self.get_flights_round_trip_tab().is_selected()

    def get_multi_city_tab(self):
        """
        Get edX logo
        Returns:
            web driver element: Logo element
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_multi_city_tab
        )

    def load_flights_multi_city_tab(self):
        """ Get edX logo
                Returns:
                  web driver element: Logo element
        """

        self.get_multi_city_tab().click()

    def get_origin_tab(self):
        """
       get origin tab

        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_code
        )

    def load_origin_tab(self):
        """
        Get origin tab
        """
        self.get_origin_tab().click()

    def get_destination_tab(self):
        """
        Get destination tab
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_destination_code
        )

    def load_destination_tab(self):
        """
           Get destination tab
        """

        self.get_destination_tab().click()

    def get_flights_travelers(self):
        """
        Get Flights travelers tab
        """

        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_travelers,
        )

    def get_cabin_type(self):
        """
        Get type of cabin
        Economy/Premium/etc
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.premium_economy
        )

    def get_no_of_travellers(self):
        """
        Get no of travellers
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.adult_increment_button
        )

    def get_apply_button(self):
        """
          get value
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.apply_selected_date
        )

    def load_flights_travelers(self):
        """
        get flights traveler cabin type
        """
        self.get_flights_travelers().click()
        self.get_cabin_type().click()
        self.get_no_of_travellers().click()
        self.get_apply_button().click()

    def get_origin_search_box(self):
        """
        Get origin tab
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_origin_search_bar
        )

    def get_first_result_against_search(self):
        """"
        Get first result
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.first_result_againts_search
        )

    def get_flight_date_tab(self):
        """
          get value
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.flights_dates
        )

    def get_search_image_button(self):

        """
        get value
        """
        return self.global_contents.wait_and_get_element(
            self.driver,
            android_elements.search_button
        )

    def flights_search_button(self):
        """
        click on search button than go to search flight screen

        """
        self.get_search_image_button().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.SEARCH_FLIGHT_RESULT_ACTIVITY
        )

    def load_flight_date_tab(self):
        """
        get value
        """

        self.get_flight_date_tab().click()
        self.apply_selected_date().click()
        self.get_apply_button().click()

        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            self.global_contents.FRONT_DOOR_ACTIVITY_NAME
        )

    def flights_search_result_complete(self):
        """
        complete search
        """
        return self.global_contents.wait_for_android_activity_to_load(
            self.driver,
            android_elements.flight_result_search_complete_text
        ).is_displayed()

    def back_and_forth_login(self):
        """
        Load login screen and get back to previous screen

        Returns:
             bool: Returns True if app is back on New Landing screen from Login screen
        """

        self.global_contents.flag = False
        if self.driver.current_activity == self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME:
            if self.load_login_screen() == self.global_contents.LOGIN_ACTIVITY_NAME:
                self.driver.back()
                if self.global_contents.wait_for_android_activity_to_load(
                        self.driver,
                        self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME
                ) == self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME:
                    self.global_contents.flag = True
                else:
                    self.log.error('New Landing screen is not loaded')
            else:
                self.log.error('Login screen is not loaded')
        else:
            self.log.error('Problem - Not on New Landing screen')

        return self.global_contents.flag

    def back_and_forth_register(self):
        """
        Load register screen and get back to previous screen

        Returns:
             bool: Returns True if app is back on New Landing screen from Register screen
        """

        self.global_contents.flag = False
        if self.driver.current_activity == self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME:
            if self.load_register_screen() == self.global_contents.REGISTER_ACTIVITY_NAME:
                self.driver.back()
                if self.global_contents.wait_for_android_activity_to_load(
                        self.driver,
                        self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME
                ) == self.global_contents.DISCOVERY_LAUNCH_ACTIVITY_NAME:
                    self.global_contents.flag = True
                else:
                    self.log.error('New Landing screen is not loaded')
            else:
                self.log.error('Register screen is not loaded')
        else:
            self.log.error('Problem - Not on New Landing screen')

        return self.global_contents.flag
