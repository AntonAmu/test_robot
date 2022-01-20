from pathlib import Path
from DownloaderPdfFile import DownloaderPdfFile
from ExcelHandler import ExcelHandler
from bs4 import BeautifulSoup
from RPA.Tables import Table
from Parser import Parser
from CheckerPdfVSExcel import CheckerPdfVsExcel
from constants import DOWNLOAD_DIRECTORY, MAIN_PAGE_URL, INITIAL_COLUMN_FOR_MAIN_PAGE_TABLE
import logging


logging.basicConfig(filename=f'{DOWNLOAD_DIRECTORY}/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def convert_ammount(amount):
    """Parses amount to integer"""
    multi = {'B': 1e10, 'M': 1e6, 'T': 1e3, '': 1}
    amount = float(amount[1:-1])*multi.get(amount[-1])
    return amount


class Bot:

    def __init__(self):
        self.downloader_pdf_file = DownloaderPdfFile
        self.parser = Parser()
        self.excel_handler = ExcelHandler(str(Path(DOWNLOAD_DIRECTORY, 'agencies.xlsx')))
        self.elements_for_agencies = None
        self.checker_pdf_vs_excel = CheckerPdfVsExcel

    @staticmethod
    def form_data_from_main_page(elements):
        """
        Gets list of webelements
        Returns Dict with elements to click in order to get detail info
        and Table structure.
        """
        elements_for_agencies = {}
        rows = []
        header = INITIAL_COLUMN_FOR_MAIN_PAGE_TABLE
        for element in elements:
            row = []
            info = element.text.split('\n')
            agency = info[0]
            total = info[-2]
            elements_for_agencies[agency] = element
            row.append(agency)
            row.append(convert_ammount(total))
            rows.append(row)
        else:
            header.append(info[1])
        return elements_for_agencies, Table(rows, columns=header)

    @staticmethod
    def transform_table_webelement_to_beatifulsoup_object(element):
            """
            Get webelement retrieve inner html.
            Returns Beatifulsoup object.
            """
            html_table = element.get_attribute('innerHTML')
            return BeautifulSoup(html_table, "html.parser")

    def get_detail_table(self, html_table, head_table):
        """
        Parses and returns the given HTML table as a Table structure and list of urls.
        :param html_table: Table HTML markup, list.
        """
        table_rows = []
        urls_for_downloading = []
        soup_table = self.transform_table_webelement_to_beatifulsoup_object(html_table)
        soup_head = self.transform_table_webelement_to_beatifulsoup_object(head_table)
        for table_row in soup_table.select('tr'):
            link = table_row.find('a')
            if link:
                urls_for_downloading.append(MAIN_PAGE_URL + link.get('href'))
            cells = table_row.find_all('td')
            if len(cells) > 0:
                cell_values = []
                for cell in cells:
                    cell_values.append(cell.text.strip())
                table_rows.append(cell_values)
        return Table(table_rows, [th.text for th in soup_head.find_all('th')]), urls_for_downloading

    def download_pdfs(self, urls):
        """Gets list of urls and downloads pdf files for each url.
        """
        for url in urls:
            self.parser.browser.go_to(url)
            self.downloader_pdf_file.download_pdf(self.parser.browser)

    def task(self):
        self.elements_for_agencies, main_page_table = self.form_data_from_main_page(self.parser.parse_table_from_main_page())
        self.excel_handler.write_data_to_new_worksheet(main_page_table, 'Agencies')
        html_table, head_table = self.parser.parse_element_from_details_page(self.elements_for_agencies)
        detail_info, urls_for_downloading = self.get_detail_table(html_table, head_table)
        self.excel_handler.write_data_to_new_worksheet(detail_info, 'Individual Investments')
        self.download_pdfs(urls_for_downloading)
        self.checker_pdf_vs_excel(detail_info).compare_pdf_with_excel()


def main():
    try:
        bot = Bot()
        bot.task()
    finally:
        bot.parser.browser.close_all_browsers()
        bot.excel_handler.close_workbook()


if __name__ == '__main__':
    main()
