from urllib.parse import urljoin, urlparse

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from main.models import Statistic

from selenium import webdriver
from bs4 import BeautifulSoup
import os


def download_page_with_selenium(url, folder_path, proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, "html.parser")

        os.makedirs(folder_path, exist_ok=True)

        process_css_scripts(soup, url)

        process_media_links(soup, url, folder_path, proxy)

        reformat_href(soup, proxy)

        reformat_static_img(soup, proxy)

        with open(os.path.join(folder_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(str(soup))

    finally:
        driver.quit()

    return soup


def process_css_scripts(soup, url):
    css_link = soup.find("link", {"rel": "stylesheet"})

    if css_link:
        css_url = urljoin(url, css_link["href"])
        css_content = requests.get(css_url).text
        style_tag = soup.new_tag("style")
        style_tag.string = css_content
        soup.head.append(style_tag)


def process_media_links(soup, url, folder_path, proxy):
    for element in soup.find_all(['img', 'link', 'script'], {'src': True}):
        src = element['src']
        if src.startswith(('http:', 'https:')):
            src_url = src
        else:
            src_url = urljoin(url, src)
        download_media(src_url, folder_path, proxy)


def download_media(url, base_folder, proxy):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        file_name = os.path.basename(urlparse(url).path)
        if "/static/" not in url:
            file_path = os.path.join(base_folder, file_name)
        else:
            file_path = f"static/{proxy.name}/" + url[url.find('/static/') + len("/static/"):]
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


def reformat_static_img(soup, proxy):
    for img_tag in soup.find_all("img", src=True):
        if "/static/" in img_tag["src"]:
            img_tag["src"] = img_tag["src"].replace("/static/", f"/static/{proxy.name}/")
        if "/media/" in img_tag["src"]:
            img_tag["src"] = f"/media/{proxy.name}/" + img_tag["src"].split("/")[-1]


def reformat_href(soup, proxy):
    for a_tag in soup.find_all("a", href=True):
        if not a_tag["href"].startswith(('http:', 'https:')):
            a_tag["href"] = f"/{proxy.name}/{proxy.url}/{a_tag['href']}"
    for form_tag in soup.find_all("form", action=True):
        if not form_tag["action"].startswith(('http:', 'https:')):
            form_tag["action"] = f"/{proxy.name}/{proxy.url}{form_tag['action']}"


def update_statistic(request, proxy, bytes_sent, bytes_received, page_views):
    user = request.user
    site = proxy

    statistic, created = Statistic.objects.get_or_create(user=user, site=site)

    statistic.page_views += page_views
    statistic.data_sent += bytes_sent
    statistic.data_received += bytes_received

    statistic.save()
