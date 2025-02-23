import requests
from bs4 import BeautifulSoup
import zipfile
import os

MAIN_URL = "https://www.ecomschool.co.il"
MAIN_URL1 = 'https://docs.google.com/forms/d/e/1FAIpQLSf2l8S3NUSse0zMu1Hz1S6k2Ep2QNA8Ju8MlK7cUSw7A0VJwA/viewform'
SITE = requests.get(MAIN_URL)
save_path = r'C:\Users\chana\OneDrive\Documents\Homwork Cyber defence course\python test.zip'
Num = 0
TotalLinksFound = 0
PATH_LIST = []
EXISTING_URI = []
USED_PATH_LIST = []
PAGE_LINKS = []
USED_LINKS = []
DOWNLOADED_DOCS = []
File_extensions_list = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",  # Image Files
    ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".html", ".htm", ".md",  # Document Files
    ".xls", ".xlsx", ".ods", ".csv",  # Spreadsheet Files
    ".ppt", ".pptx", ".odp",  # Presentation Files
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",  # Audio Files
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",  # Video Files
    ".zip", ".rar", ".tar", ".gz", ".7z", ".bz2",  # Compressed Files
    ".exe", ".msi", ".bat", ".sh",  # Executable Files
    ".sql", ".db", ".mdb", ".accdb",  # Database Files
    ".dll", ".sys", ".ini", ".log"  # System Files
]


def get_paths():
    global PATH_LIST
    path = requests.get('https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt')
    # print(userNames.text.split())
    PATH_LIST = path.text.split()
    return PATH_LIST


# find the uri on current path
def find_paths_in_main_link():
    global PATH_LIST, USED_PATH_LIST, EXISTING_URI
    for uri in PATH_LIST:
        if uri not in USED_PATH_LIST:
            url = MAIN_URL
            print(f'searching if /{uri} exists ...')

            url = f'{url}/{uri}'
            print(url)
            USED_PATH_LIST.append(uri)
            response = requests.get(url)
            if response.status_code == 200:
                EXISTING_URI.append(url)

            print('all existing paths are: ', EXISTING_URI)

            print('used uri :', USED_PATH_LIST)
    check_in_path_uri()


# find the uri on  all  found uri recursively
def check_in_path_uri():
    global PATH_LIST, USED_PATH_LIST, EXISTING_URI

    for url in EXISTING_URI:
        for uri in PATH_LIST:

            url = url
            print(f'searching if /{uri} exists in url {url} ...')
            url1 = f'{url}/{uri}'
            print(url)
            if url1 not in USED_LINKS:
                USED_PATH_LIST.append(url1)
                response = requests.get(url)
                if response.status_code == 200:
                    EXISTING_URI.append(url1)

            print('all existing paths are: ', EXISTING_URI)

            print('used uri :', USED_PATH_LIST)


# find the links on current page
def find_links():
    global TotalLinksFound,EXISTING_URI,PAGE_LINKS
    soup = BeautifulSoup(SITE.text, 'html.parser')
    links = soup.findAll('a', href=True)
    num = 0
    for link in links:
        href = str(link['href'])
        if 'http' in href:
            num += 1
            if link not in USED_LINKS:
                TotalLinksFound += 1
                find_files_doc_or_images(link)
            PAGE_LINKS.append(href)
            print(f'{num} links found\n{href}')
            print('================')

    print('Total Links Found: ', TotalLinksFound)


def find_links_in_paths():
    global TotalLinksFound, EXISTING_URI, PAGE_LINKS
    # after finishing finding all paths now it checks for links in the existing paths
    if EXISTING_URI: # if the list has Items then:
        for url in EXISTING_URI:
            soup = BeautifulSoup(url.text, 'html.parser')
            links = soup.findAll('a', href=True)
            num = 0
            for link in links:
                href = str(link['href'])
                if 'http' in href:
                    num += 1
                    if link not in USED_LINKS:
                        TotalLinksFound += 1
                        find_files_doc_or_images(link)
                    PAGE_LINKS.append(href)
                    print(f'{num} links found\n{href}')
                    print('================')
            print('Total Links Found: ', TotalLinksFound)

    print("These are the links I found main page and in the uri paths:",PAGE_LINKS)


def crawl_trough_links():
    global SITE,PAGE_LINKS,USED_LINKS,MAIN_URL
    url = ''
    for link in PAGE_LINKS:
        if link not in USED_LINKS and MAIN_URL in link:
            print(f'searching {link} for links ...')
            pos = link.find('http')
            if pos != -1:
                url = link[pos:]
            url = url
            USED_LINKS.append(link)
            SITE = requests.get(url)
            find_links()

            print('used links :', USED_LINKS)
    print("These are the total links  found:",PAGE_LINKS)


def find_files_doc_or_images(link):
    for extension in File_extensions_list:
        if link not in DOWNLOADED_DOCS:
            if extension in link['href']:
                print('found file to download: ', link['href'])
                print(extension)
                DOWNLOADED_DOCS.append(link)
                download_and_compress_file(link['href'], extension)


def download_and_compress_file(url, extension):
    global Num, save_path
    Num += 1
    # Temporary file path for the downloaded document
    temp_file_path = fr"C:\Users\chana\Documents\Downloads\testPythonDoc{Num}{extension}"
    # Download the document
    response = requests.get(f'{url}')

    if response.status_code == 200:
        with open(temp_file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved to {temp_file_path}")

        # Compress the document into a zip file
        with zipfile.ZipFile(save_path, 'a') as zipf:
            zipf.write(temp_file_path, os.path.basename(temp_file_path))
        print(f"File compressed successfully and saved to {save_path}")

        # Remove the temporary file
        os.remove(temp_file_path)

    else:
        print(f"Failed to download file. Status code: {response.status_code}")


if __name__ == '__main__':
    get_paths()
    find_paths_in_main_link()
    find_links()
    find_links_in_paths()
    crawl_trough_links()

    print('finished ========================')
