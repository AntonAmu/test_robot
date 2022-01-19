from RPA.PDF import PDF
from glob import glob
from constants import DOWNLOAD_DIRECTORY


class PdfHandler(PDF):

    @staticmethod
    def get_name_of_this_investment(text):
        """Find name of investment in pdf file.
        Returns string
        """
        start = text.find('1. Name of this Investment:') + len('1. Name of this Investment:')
        end = text.find('2. Unique Investment Identifier (UII):')
        return text[start:end].strip()

    @staticmethod
    def get_unique_investment_identifier(text):
        """Find UII in pdf file.
        Returns string
        """
        start = text.find('2. Unique Investment Identifier (UII):') + len('2. Unique Investment Identifier (UII):')
        end = text.find('Section B: Investment Detail')
        return text[start:end].strip()

    def get_values_from_pdf(self, file):
        """Parses pdf file.
        Returns dict with parsed information
        """
        text = self.get_text_from_pdf(file, trim=True)[1]
        unique_investment_identifier = self.get_unique_investment_identifier(text)
        name_of_this_investment = self.get_name_of_this_investment(text)
        self.close_pdf(file)
        return {'name': name_of_this_investment, 'uii': unique_investment_identifier, 'file': file}

    def get_data_from_pdf_files(self):
        """Parses each pdf file in outcome.
        Returns list of dicts
        """
        data = []
        for file in glob(f"{DOWNLOAD_DIRECTORY}/*.pdf"):
            values = self.get_values_from_pdf(file)
            data.append(values)
        return data
