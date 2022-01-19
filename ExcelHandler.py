from RPA.Excel.Files import Files


class ExcelHandler(Files):

    def __init__(self, workbook):
        super().__init__()
        self.create_workbook(workbook)

    def write_data_to_new_worksheet(self, data_to_excel, worksheet):
        """
        Create a new sheet in excel file and writes data to this sheet.
        """
        self.create_worksheet(worksheet)
        self.append_rows_to_worksheet(data_to_excel)
        self.save_workbook()
