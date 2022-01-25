from RPA.FileSystem import FileSystem
from DownloaderPdfFile import DownloaderPdfFile
from ExcelHandler import ExcelHandler
from RPA.Tables import Table
from Parser import Parser
from CheckerPdfVSExcel import CheckerPdfVsExcel
from constants import DOWNLOAD_DIRECTORY, MAIN_PAGE_URL, INITIAL_COLUMN_FOR_MAIN_PAGE_TABLE, EXCEL_FILE
import logging


logging.basicConfig(filename=f'{DOWNLOAD_DIRECTORY}/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def convert_ammount(amount):
    """Parses amount to integer"""
    multi = {'B': 1e10, 'M': 1e6, 'T': 1e3, '': 1}
    amount = float(amount[1:-1])*multi.get(amount[-1])
    return amount


class Bot:

    def __init__(self):
        self.file_system = FileSystem()
        self.downloader_pdf_file = DownloaderPdfFile()
        self.parser = Parser(self.file_system.absolute_path(DOWNLOAD_DIRECTORY))
        self.elements_for_agencies = None
        self.checker_pdf_vs_excel = CheckerPdfVsExcel()
        self.excel_handler = ExcelHandler(self.file_system.join_path(DOWNLOAD_DIRECTORY,EXCEL_FILE))

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


    def handle_with_detail_table(self, html_table, head_table):
        """
        Parses and returns the given HTML table as a Table structure.
        For each row in table parses reference to pdf file is exist.
        If reference exists then downloads pdf file and compare uii and 
        investment title in pdf with appropriate values in table.
        Result of comparison logs to file app.log in directory output. 
        :param html_table: Table HTML markup.
        """
        table_rows = []
        head_table = head_table.find_elements_by_tag_name('th')
        
        for table_row in html_table.find_elements_by_tag_name('tr'):
                        
            cells = table_row.find_elements_by_tag_name('td')

            if len(cells) > 0:
                row = []
                for cell in cells:
                    row.append(cell.text.strip())
            
            link = table_row.find_elements_by_tag_name('a')
            
            if link:
                url_for_downloading = link[0].get_attribute('href')
                file = self.download_pdf(url_for_downloading)
                result = self.checker_pdf_vs_excel.compare_pdf_with_excel(row, file)
                logging.info(result)
            table_rows.append(row)
        
        return Table(table_rows, [th.text for th in head_table])

    def download_pdf(self, url):
        """
        Gets url and downloads pdf file.
        """
        self.parser.open_window(url)
        file = self.downloader_pdf_file.download_pdf(self.parser.browser, self.file_system)
        self.parser.close_window()
        return file

    def task(self):
        self.elements_for_agencies, main_page_table = self.form_data_from_main_page(self.parser.parse_table_from_main_page())
        self.excel_handler.write_data_to_new_worksheet(main_page_table, 'Agencies')
        html_table, head_table = self.parser.parse_element_from_details_page(self.elements_for_agencies)
        detail_info = self.handle_with_detail_table(html_table, head_table)
        self.excel_handler.write_data_to_new_worksheet(detail_info, 'Individual Investments')



def main():
    try:
        bot = Bot()
        bot.task()
    finally:
        bot.parser.browser.close_all_browsers()
        bot.excel_handler.close_workbook()


if __name__ == '__main__':
    main()
