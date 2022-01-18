from pathlib import Path
from constants import TIMEOUT, ELEMENT_TO_DOWNLOAD, WAITING_ELEMENT, DOWNLOAD_DIRECTORY


class DownloaderPdfFile:

    def __init__(self, window_handle):
        self.window_handle = window_handle

    def download_pdf(self, browser):
        browser.switch_window(self.window_handle)
        location = browser.get_location()
        browser.wait_until_element_is_visible(WAITING_ELEMENT, timeout=TIMEOUT)
        browser.click_element(ELEMENT_TO_DOWNLOAD)
        file_name = location.split('/')[-1] + '.pdf'
        while not Path(f"{DOWNLOAD_DIRECTORY}/{file_name}").exists():
            continue
        browser.close_window()
        return
