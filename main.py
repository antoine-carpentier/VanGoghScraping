# used for parsing the page html
from bs4 import BeautifulSoup

# used to download the images
import requests

# selenium required as the website is dynamically populated
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# function to download 211 Van Gogh paintings
def vangogh():
    # initializing Selenium with Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # website where the Van Gogh paintings are going to be downloaded from
    driver.get("https://www.vangoghmuseum.nl/en/collection?q=&Artist=Vincent%20van%20Gogh&Type=painting")

    # make the website wait 30s or for the last element to be loaded
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/main/section/section/div/div/div/div[211]"))
    )

    # get the page html and parse it
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    # each painting on the page is individually contained in a div of class "collection-art-object-list-item"
    divs = soup.find_all('div', class_="collection-art-object-list-item")

    # a lot of Van Gogh's painting have the same name, so we need to make sure we are not overwriting files
    img_name_list = []

    # within each div of divs, there's an img with an alt attribute
    # and a data-srcset containing the link to the painting that we want to grab
    for div in divs:
        img = div.findChild("img")
        try:
            img_name = img['alt']
            # check if a similarly named image was downloaded already
            img_name = check_img_name_unicity(img_name, img_name_list)

            img_url = img['data-srcset']
            img_url = img_url.split(' ')[-2][6:]
            # download the image to the chosen folder
            urlretrieve('C:\\Users\\elver\\Documents\\Art\\VanGoghML\\Van Gogh\\' + img_name + '.jpg', img_url)
        except:
            print(f"issue encountered with painting {img}")


# function to download the 500 most famous paintings
def not_vangogh():
    # initializing Selenium with Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # website where the paintings are going to be downloaded from
    driver.get("https://en.most-famous-paintings.com/MostFamousPaintings.nsf/ListOfTop500MostPopularPainting")

    # get the page html and parse it
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    # each painting on the page is individually contained in a div of class "mosaicflow__item"
    divs = soup.find_all('div', class_="mosaicflow__item")

    # within each div of divs, there's an img with a data original that we want to grab
    for div in divs:
        img = div.findChildren("img")
        img_name = img[0]['data-original']
        img_url = "https://en.most-famous-paintings.com" + img_name
        # remove the paintings by Van Gogh
        if "Gogh" not in img_url:
            # download the image
            img_name = img_name.split('/')[-1]
            urlretrieve('C:\\Users\\elver\\Documents\\Art\\VanGoghML\\Not Van Gogh\\' + img_name, img_url)


# function to download the images
def urlretrieve(path, url):
    with open(path, 'wb') as f:
        r = requests.get(url, stream=True)
        r.raise_for_status()  # Replace this with better error handling.

        for chunk in r.iter_content(1024):
            f.write(chunk)


# function that checks if the image name is already in use
# to avoid overwriting already downloaded images
def check_img_name_unicity(img_name, img_name_list):
    if img_name not in img_name_list:
        img_name_list.append(img_name)
        return img_name
    else:
        i = 2
        new_img_name = img_name
        while new_img_name in img_name_list:
            new_img_name = img_name + ' ' + str(i)
            i += 1
        img_name_list.append(new_img_name)
        print(f'{img_name} replaced by {new_img_name}.')
        return new_img_name


if __name__ == '__main__':
    vangogh()
    not_vangogh()
