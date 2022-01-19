from RPA.Browser.Selenium import Selenium
from constants import (AGENCY_NAME, MAIN_PAGE_URL, ELEMENT_FOR_CLICK_IN_MAIN_PAGE, DOWNLOAD_DIRECTORY,
                       PARSED_ELEMENT_ON_MAIN_PAGE, TIMEOUT, DETAIL_TABLE, SELECT_ELEMENT,
                       SELECT_OPTION, PAGINATOR, ELEMENT_IN_TABLE_WITH_URL, TABLE
                       )


class Parser:
    def __init__(self):
        self.browser = Selenium()
        self.browser.set_download_directory(str(DOWNLOAD_DIRECTORY))

    def parse_table_from_main_page(self):
        """Opens headless browser, reveal information about agencies.
        Returns list of webelements.
        """
        self.browser.open_headless_chrome_browser(MAIN_PAGE_URL)
        self.browser.click_element(ELEMENT_FOR_CLICK_IN_MAIN_PAGE)
        self.browser.wait_until_element_is_visible(PARSED_ELEMENT_ON_MAIN_PAGE)
        list_of_elements = self.browser.find_elements(PARSED_ELEMENT_ON_MAIN_PAGE)
        return list_of_elements

    def parse_element_from_details_page(self, elements_for_agencies):
        """
        Goes to page for detail information about appropite agency.
        Returns webelement witch cointains detail information.
        """
        element_to_click = elements_for_agencies.get(AGENCY_NAME)
        self.browser.click_element(element_to_click)
        self.browser.wait_until_element_is_visible(DETAIL_TABLE, timeout=TIMEOUT)
        self.browser.select_from_list_by_value(SELECT_ELEMENT, SELECT_OPTION)
        self.browser.wait_until_page_does_not_contain_element(PAGINATOR, timeout=TIMEOUT)
        return self.browser.find_element(TABLE)

    @property
    def url_for_downloading(self):
        """Returns list of urls for downloading pdf.
        """
        return [element.get_attribute('href') for element in self.browser.find_elements(ELEMENT_IN_TABLE_WITH_URL)]