from PdfHandler import PdfHandler
import time
import logging
from constants import (ANSWER_IF_NO_MATCH, ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH,
                       ANSWER_IF_UII_DOESNT_MATCH, ANSWER_IF_MATCH)


class CheckerPdfVsExcel:

    def __init__(self, table):
        self.pdf_handler = PdfHandler()
        self.table = table

    def compare_pdf_with_excel(self):
        """
        Compares datas from pdf files with excel file.
        Return string.
        """
        start = time.perf_counter()
        data_from_pdfs = self.pdf_handler.get_data_from_pdf_files()
        period = time.perf_counter() - start
        print(f"parse pdf takes {period}")
        uii = self.table.get_column(0).values()
        name = self.table.get_column(2).values()
        dict_from_excel_uii_key = dict(zip(uii, name))
        dict_from_excel_name_key = dict(zip(name, uii))
        for data_from_pdf in data_from_pdfs:
            result = self.compare_values(data_from_pdf, dict_from_excel_uii_key, dict_from_excel_name_key)
            logging.info(result)
        return result

    @staticmethod
    def compare_values(data_from_pdf, dict_from_excel_uii_key, dict_from_excel_name_key):
        """
        Gets data from pdf file as dict and data from excel file as two dicts.
        Compares uii and name of investment in pdf file with excel file.
        Return string.
        """
        if dict_from_excel_uii_key.get(data_from_pdf['uii']):
            if dict_from_excel_name_key.get(data_from_pdf['name']):
                return ANSWER_IF_MATCH.format(data_from_pdf['file'])
            else:
                return ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH.format(data_from_pdf['file'])

        if dict_from_excel_name_key.get(data_from_pdf['name']):
            return ANSWER_IF_UII_DOESNT_MATCH.format(data_from_pdf['file'])
        else:
            return ANSWER_IF_NO_MATCH.format(data_from_pdf['file'])
