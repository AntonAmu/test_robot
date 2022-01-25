from PdfHandler import PdfHandler
import logging
from constants import (
                       ANSWER_IF_NO_MATCH, ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH,
                       ANSWER_IF_UII_DOESNT_MATCH, ANSWER_IF_MATCH
                       )


class CheckerPdfVsExcel:

    def __init__(self):
        self.pdf_handler = PdfHandler()

    def compare_pdf_with_excel(self, table_row, file):
        """
        Compares datas from pdf file with excel file.
        Return string.
        """
        data_from_pdf = self.pdf_handler.get_values_from_pdf(file)
        uii = table_row[0]
        name = table_row[2]
        dict_from_excel_uii_key = {uii: name}
        dict_from_excel_name_key = {name: uii}
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
