DOWNLOAD_DIRECTORY = 'output'
EXCEL_FILE = 'agencies.xlsx'
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


"""

SELECT COUNT(USERS.ID), DATE_PART('DAY', date_reg), COUNTRIES.group
FROM USERS 
JOIN COUNTRIES on USERS.id_country=COUNTRIES.id
GROUP BY DATE_PART('DAY', date_reg), COUNTRIES.group

DELETE FROM USERS
WHERE date_reg BETWEEN '2017-10-01 12:36:00' AND '2017-10-01 15:45:00'
AND (email LIKE '___\_test_\___' OR email LIKE 'test_\___' OR email LIKE '___\_test'

SELECT clicks.day, clicks.typez, clicks.amount/whole.amount as CTR
from 
(SELECT EMAILS_SENT.id_type as typez, DATE_PART('DAY', EMAILS_SENT.date_sent) as day, count(1) as amount
FROM EMAILS_SENT 
GROUP BY EMAILS_SENT.id_type, DATE_PART('DAY', EMAILS_SENT.date_sent)
) as whole
LEFT JOIN (
SELECT EMAILS_SENT.id_type as typez, DATE_PART('DAY', EMAILS_SENT.date_sent) as day, count(1) as amount
FROM EMAILS_SENT 
JOIN EMAILS_CLICKS ON EMAILS_SENT.id = EMAILS_CLICKS.id_email
GROUP BY EMAILS_SENT.id_type, DATE_PART('DAY', EMAILS_SENT.date_sent)
) as clicks on whole.typez=clicks.typez and whole.day=clicks.day
"""