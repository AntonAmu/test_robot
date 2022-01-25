from constants import TIMEOUT, ELEMENT_TO_DOWNLOAD, WAITING_ELEMENT, DOWNLOAD_DIRECTORY


class DownloaderPdfFile:

    @staticmethod
    def download_pdf(browser, file_system):
        """
        Initializes dowloading and makes sure that file is downloaded.
        """
        location = browser.get_location()
        browser.wait_until_element_is_visible(WAITING_ELEMENT, timeout=TIMEOUT)
        browser.click_element(ELEMENT_TO_DOWNLOAD)
        file_name = location.split('/')[-1] + '.pdf'
        path = file_system.join_path(DOWNLOAD_DIRECTORY, file_name)
        file = file_system.wait_until_created(path, timeout=TIMEOUT)
        return file
