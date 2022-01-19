from pathlib import Path
from constants import TIMEOUT, ELEMENT_TO_DOWNLOAD, WAITING_ELEMENT, DOWNLOAD_DIRECTORY


class DownloaderPdfFile:

    @classmethod
    def download_pdf(cls, browser):
        """
        Initializes dowloading and makes sure that file is downloaded.
        """
        location = browser.get_location()
        browser.wait_until_element_is_visible(WAITING_ELEMENT, timeout=TIMEOUT)
        browser.click_element(ELEMENT_TO_DOWNLOAD)
        file_name = location.split('/')[-1] + '.pdf'
        while not Path(f"{DOWNLOAD_DIRECTORY}/{file_name}").exists():
            continue
        return
