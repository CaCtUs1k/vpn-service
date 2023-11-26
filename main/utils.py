from urllib.parse import urljoin

import requests

from main.models import Statistic


def get_css(soup, url):
    css_link = soup.find("link", {"rel": "stylesheet"})

    if css_link:
        css_url = urljoin(url, css_link["href"])
        css_response = requests.get(css_url)

        if css_response.status_code == 200:
            css_content = css_response.text

            style_tag = soup.new_tag("style")
            style_tag.string = css_content
            soup.head.append(style_tag)
        else:
            print(
                f"Failed to fetch CSS. Status code: {css_response.status_code}"
            )


def get_scripts(soup, url):
    script_tags = soup.find_all("script", {"src": True})

    for script_tag in script_tags:
        script_src = script_tag["src"]
        script_url = urljoin(url, script_src)

        script_response = requests.get(script_url)

        if script_response.status_code == 200:
            script_content = script_response.text
            new_script_tag = soup.new_tag("script")
            new_script_tag.string = script_content
            script_tag.replace_with(new_script_tag)
        else:
            print(
                f"Failed to fetch script. Status code: {script_response.status_code}"
            )


def reformat_href(soup, proxy):
    for a_tag in soup.find_all("a", href=True):
        if "https://" not in a_tag["href"]:
            a_tag["href"] = f"/{proxy.name}/{proxy.url}/{a_tag['href']}"
    for form_tag in soup.find_all("form", action=True):
        if "https://" not in form_tag["action"]:
            form_tag[
                "action"
            ] = f"/{proxy.name}/{proxy.url}/{form_tag['action']}"


def update_statistic(request, proxy, bytes_sent, bytes_received, page_views):
    user = request.user
    site = proxy

    statistic, created = Statistic.objects.get_or_create(user=user, site=site)

    statistic.page_views += page_views
    statistic.data_sent += bytes_sent
    statistic.data_received += bytes_received

    statistic.save()
