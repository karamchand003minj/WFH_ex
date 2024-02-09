# import requests

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 Edg/88.0.705.74",
#     "Accept-Language": "en-US,en;q=0.5"
# }

# url = "your_target_url_here"
# response = requests.get(url, headers=headers)

import csv
from lxml import html
import requests

def verify_response(response):
    """
    Verify if we received valid response or not
    """
    return True if response.status_code == 200 else False

def send_request(url):
    """
    Send request and handle retries.
    :param url:
    :return: Response we received after sending request to the URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 Edg/88.0.705.74",
        "Accept-Language": "en-US,en;q=0.5"
    }
    max_retry = 3
    while max_retry >= 1:
        response = requests.get(url, headers=headers)
        if verify_response(response):
            return response
        else:
            max_retry -= max_retry
    print("Invalid response received even after retrying. URL with the issue is:", url)
    raise Exception("Stopping the code execution as invalid response received.")

def get_next_page_url(response):
    """
    Collect pagination URL.
    :param response:
    :return: next listing page url
    """
    parser = html.fromstring(response.text)
    next_page_url = parser.xpath('(//a[@class="next page-numbers"])[1]/@href')[0]
    return next_page_url

def get_product_urls(response):
    """
    Collects all product URL from a listing page response.
    :param response:
    :return: list of urls. List of product page urls returned.
    """
    parser = html.fromstring(response.text)
    product_urls = parser.xpath('//li/a[contains(@class, "product__link")]/@href')
    return product_urls

def clean_stock(stock):
    """
    Clean the data stock by removing unwanted text present in it.
    :param stock:
    :return: Stock data. Stock number will be returned by removing extra string.
    """
    stock = clean_string(stock)
    if stock:
        stock = stock.replace(' in stock', '')
        return stock
    else:
        return None

def clean_string(list_or_txt, connector=' '):
    """
    Clean and fix list of objects received. We are also removing unwanted white spaces.
    :param list_or_txt:
    :param connector:
    :return: Cleaned string.
    """
    if not list_or_txt:
        return None
    return ' '.join(connector.join(list_or_txt).split())

def get_product_data(url):
    """
    Collect all details of a product.
    :param url:
    :return: All data of a product.
    """
    response = send_request(url)
    parser = html.fromstring(response.text)
    title = parser.xpath('//h1[contains(@class, "product_title")]/text()')
    price = parser.xpath('//p[@class="price"]//text()')
    stock = parser.xpath('//p[contains(@class, "in-stock")]/text()')
    description = parser.xpath('//div[contains(@class,"product-details__short-description")]//text()')
    image_url = parser.xpath('//div[contains(@class, "woocommerce-product-gallery__image")]/a/@href')
    product_data = {
        'Title': clean_string(title), 'Price': clean_string(price), 'Stock': clean_stock(stock),
        'Description': clean_string(description), 'Image_URL': clean_string(list_or_txt=image_url, connector=' | '),
        'Product_URL': url}
    return product_data

def save_data_to_csv(data, filename):
    """
    save list of dict to csv.
    :param data: Data to be saved to csv
    :param filename: Filename of csv
    """
    keys = data[0].keys()
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def start_scraping():
    """
    Starting function.
    """
    listing_page_url = 'https://scrapeme.live/shop/'
    product_urls = list()
    for listing_page_number in range(1, 6):
        response = send_request(listing_page_url)
        listing_page_url = get_next_page_url(response)
        products_from_current_page = get_product_urls(response)
        product_urls.extend(products_from_current_page)
        results = []
    for url in product_urls:
        results.append(get_product_data(url))
    save_data_to_csv(data=results, filename='scrapeme_live_Python_data.csv')
    print('Data saved as csv')

if __name__ == "__main__":
    start_scraping()
