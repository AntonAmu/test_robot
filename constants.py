from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIRECTORY = Path(BASE_DIR, 'output')
AGENCY_NAME = 'National Archives and Records Administration'
MAIN_PAGE_URL = "https://itdashboard.gov/"
ELEMENT_FOR_CLICK_IN_MAIN_PAGE = '#home-dive-in'
PARSED_ELEMENT_ON_MAIN_PAGE = '//div[@class="col-sm-4 text-center noUnderline"]'
TIMEOUT = 300
INITIAL_COLUMN_FOR_MAIN_PAGE_TABLE = ['Agency name']
DETAIL_TABLE = '//*[@id="investments-table-object_wrapper"]'
HEAD_TABLE = '//*[@class="datasource-table usa-table-borderless dataTable no-footer"]'
SELECT_ELEMENT = '//*[@id="investments-table-object_length"]/label/select'
SELECT_OPTION = '-1'
PAGINATOR = '//*[@id="investments-table-object_paginate"]/span/a[2]'
TABLE = '//*[@id="investments-table-object"]/tbody'
ELEMENT_IN_TABLE_WITH_URL = '//*[@id="investments-table-object"]/tbody/tr/td/a'
WAITING_ELEMENT = '//*[@id="business-case-pdf"]'
ELEMENT_TO_DOWNLOAD = '//*[@id="business-case-pdf"]/a'
ANSWER_IF_MATCH = 'Data in file: {0} math with data in the excel file'
ANSWER_IF_UII_DOESNT_MATCH = 'UII in file: {0} differs from the excel file'
ANSWER_IF_NAME_OF_INVESTMENT_DOESNT_MATCH = 'Name of Investment in file: {0} differs from the excel file'
ANSWER_IF_NO_MATCH = 'Name of Investment and UII in file: {0} differs from the excel file'
