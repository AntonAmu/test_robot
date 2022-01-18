from PdfHandler import PdfHandler
from constants import (ANSWER_IF_NO_MATCH, ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH,
                       ANSWER_IF_UII_DOESNT_MATCH, ANSWER_IF_MATCH)


class CheckerPdfVsExcel:

    def __init__(self):
        self.pdf_handler = PdfHandler()

    def compare_pdf_with_excel(self, excel_handler):
        data_from_pdfs = self.pdf_handler.get_data_from_pdf_files()
        table = excel_handler.read_worksheet_as_table('Individual Investments')
        uii = table.get_column('A').values()
        name = table.get_column('C').values()
        dict_from_excel_uii_key = dict(zip(uii, name))
        dict_from_excel_name_key = dict(zip(name, uii))
        for data in data_from_pdfs:
            result = self.compare_values(data, dict_from_excel_uii_key, dict_from_excel_name_key)
            print(result)
        return result

    @staticmethod
    def compare_values(data, dict_from_excel_uii_key, dict_from_excel_name_key):
        if dict_from_excel_uii_key.get(data['uii']):
            if dict_from_excel_name_key.get(data['name']):
                return ANSWER_IF_MATCH.format(data['file'])
            else:
                return ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH.format(data['file'])

        if dict_from_excel_name_key.get(data['name']):
            return ANSWER_IF_UII_DOESNT_MATCH.format(data['file'])
        else:
            return ANSWER_IF_NO_MATCH.format(data['file'])
