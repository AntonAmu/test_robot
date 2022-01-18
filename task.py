from pathlib import Path
from DownloaderPdfFile import DownloaderPdfFile
from ExcelHandler import ExcelHandler
from RPA.Browser.Selenium import Selenium
from CheckerPdfVSExcel import CheckerPdfVsExcel
from constants import (DOWNLOAD_DIRECTORY, AGENCY_NAME, MAIN_PAGE_URL,
                       ELEMENT_FOR_CLICK_IN_MAIN_PAGE, PARSED_ELEMENT_ON_MAIN_PAGE, TIMEOUT, DETAIL_TABLE,
                       SELECT_ELEMENT, SELECT_OPTION, PAGINATOR, ELEMENT_IN_TABLE_WITH_URL, TABLE_CELL
                       )


def convert_ammount(amount):
    multi = {'B': 1e10, 'M': 1e6, 'T': 1e3, '': 1}
    amount = float(amount[1:-1])*multi.get(amount[-1])
    return amount


class Bot:

    def __init__(self):
        self.downloader_pdf_file = DownloaderPdfFile
        self.browser = Selenium()
        self.excel_handler = ExcelHandler(str(Path(DOWNLOAD_DIRECTORY, 'agencies.xlsx')))
        self.browser.set_download_directory(str(DOWNLOAD_DIRECTORY))
        self.agencies = None
        self.checker_pdf_vs_excel = CheckerPdfVsExcel()

    @staticmethod
    def get_agencies(elements):
        agencies = {}
        for element in elements:
            info = element.text.split('\n')
            agency = info[0]
            total = info[-1]
            agencies[agency] = {}
            agencies[agency]['total'] = convert_ammount(total)
            agencies[agency]['element'] = element
        return agencies

    def get_element_for_concrete_agency(self, agency_name):
        return self.agencies.get(agency_name).get('element')

    @staticmethod
    def get_agencies_with_totals(agencies):
        agencies_name = []
        totals = []
        for agency in agencies:
            agencies_name.append(agency)
            totals.append(agencies.get(agency).get('total'))
        return tuple(zip(agencies_name, totals))

    def get_totals_and_agencies_from_main_page(self):
        self.browser.open_headless_chrome_browser(MAIN_PAGE_URL)
        self.browser.click_element(ELEMENT_FOR_CLICK_IN_MAIN_PAGE)
        self.browser.wait_until_element_is_visible(PARSED_ELEMENT_ON_MAIN_PAGE)
        list_of_elements = self.browser.find_elements(PARSED_ELEMENT_ON_MAIN_PAGE)
        self.agencies = self.get_agencies(list_of_elements)
        totals_for_agencies = self.get_agencies_with_totals(self.agencies)
        return totals_for_agencies

    def elemts_from_table_for_agency(self):
        element_to_click = self.get_element_for_concrete_agency(AGENCY_NAME)
        self.browser.click_element(element_to_click)
        self.browser.wait_until_element_is_visible(DETAIL_TABLE, timeout=TIMEOUT)
        self.browser.select_from_list_by_value(SELECT_ELEMENT, SELECT_OPTION)
        self.browser.wait_until_page_contains_element(PAGINATOR, timeout=TIMEOUT)
        return self.browser.find_elements(TABLE_CELL)

    def get_data_from_table_elements(self):
        return [element.text for element in self.elemts_from_table_for_agency()]

    def get_url_for_downloading(self):
        return [element.get_attribute('href') for element in self.browser.find_elements(ELEMENT_IN_TABLE_WITH_URL)]

    @staticmethod
    def retrieve_data_from_table(data, step=7):
        rows = []
        for iteration in range(0, len(data)//step):
            row = data[iteration*step:step*(iteration + 1)]
            rows.append(row)
        return rows

    def open_windows(self, urls):
        for url in urls:
            self.browser.execute_javascript(f"window.open('{url}')")
        return self.browser.get_window_handles()

    def download_pdfs(self, window_handles):
        for index in range(1, len(window_handles)):
            window_handle = window_handles[index]
            self.downloader_pdf_file(window_handle).download_pdf(self.browser)

    def task(self):
        totals_for_agencies = self.get_totals_and_agencies_from_main_page()
        self.excel_handler.write_data_to_new_worksheet(totals_for_agencies, 'Agencies')
        detail_data_from_table = self.retrieve_data_from_table(self.get_data_from_table_elements())
        self.excel_handler.write_data_to_new_worksheet(detail_data_from_table, 'Individual Investments')
        urls_for_downloading = self.get_url_for_downloading()
        window_handles = self.open_windows(urls_for_downloading)
        self.download_pdfs(window_handles)
        self.checker_pdf_vs_excel.compare_pdf_with_excel(self.excel_handler)


def main():
    try:
        bot = Bot()
        bot.task()
    finally:
        bot.browser.close_all_browsers()
        bot.excel_handler.close_workbook()


if __name__ == '__main__':
    main()
