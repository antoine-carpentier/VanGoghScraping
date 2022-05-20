# VanGoghScraping

This python script's function is to download hundreds of paintings from different web sources and aggregate them into a labeled dataset that will be used by the [VanGoghMLModel repository](https://github.com/antoine-carpentier/VanGoghMLModel).

It makes use of Selenium to get the webpage source codes, BeautifulSoup to parse the page source html and get the image source URLs and finally requests to retrieve all the images from the URLs collected.
