import requests
import yaml
from pyquery import PyQuery as pq
from collections import defaultdict
import os
import re
from time import sleep

def link_conv(url):
    return url.replace("/", "__")


def fix_href(url, domain):
    if url.startswith("http"):
        return url
    elif url.startswith("/"):
        domain = re.match(r"https?://[^/]+(?=/|$)", domain).group(0)
        return domain + url
    return domain.rsplit("/", 1)[0] + "/" + url


def write_file(folder, url, html):
    try:
        os.makedirs(folder)
    except:
        pass
    filename = folder + "/" + link_conv(url)
    f = open(filename, "w")
    f.write(html)
    print filename


def get_page(url, try_again=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Cookie": "cookie1=1; cookie2=2",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.exemplo.org.br/",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    try:
        res = requests.get(url, timeout=60, headers=headers)
        if res.status_code == 200:
            return (200, res.content)
        else:
            return (res.status_code, "")
    except:
        if try_again < 5:
            sleep(try_again * 0.3 + 0.3)
            return get_page(url, try_again+1)
        return (500, "")


def get_links(html, selector):
    if ":parent" in selector:
        selector = selector[:-len(":parent")]
        anchors = pq(html)(selector).map(lambda i, elem: elem.getparent().attrib.get("href"))
    else:
        anchors = pq(html)(selector).map(lambda i, elem: elem.attrib.get("href"))
    return anchors


def page_iterator(urls):
    url_with_index = filter(lambda u: "{index}" in u, urls)
    url_without_index = filter(lambda u: "{index}" not in u, urls)
    for url in url_without_index:
        yield url
    i = 1
    while True:
        for url in url_with_index:
            yield url.format(index=i)
        i += 1

def site_iterator(config):
    abrev = config['abrev']
    try:
        site_files = os.listdir(abrev)
    except:
        site_files = []
    if "noticias" in config:
        for url in page_iterator(config["noticias"]):
            url_conv = link_conv(url)
            if url_conv not in site_files:
                yield (url, config)
                site_files.append(url_conv)
    elif "lista_noticias" in config:
        for url in page_iterator(config["lista_noticias"]):
            status, html = get_page(url)
            if status == 200:
                links = get_links(html, config['lista_noticias_link'])
                for link in links:
                    link = fix_href(link, url)
                    url_conv = link_conv(link)
                    if url_conv not in site_files:
                        yield (link, config)
                        site_files.append(url_conv)
            yield None


def build_iterator(configs):
    iterators = []
    for config in configs:
        iterator = site_iterator(config)
        consecutive_fail = 0
        iterators.append([iterator, consecutive_fail])
    while len(iterators) > 0:
        for item in iterators:
            iterator = item[0]
            try:
                ret = iterator.next()
                if ret is None:
                    item[1] += 1
                    if item[1] >= 20:
                        print "removing iterator"
                        iterators.remove(item)
                else:
                    item[1] = 0
                    yield ret
            except StopIteration:
                iterators.remove(item)


if __name__ == "__main__":
    configs = yaml.load(open("config.yaml").read())
    url_iterator = build_iterator(configs)
    for url, config in url_iterator:
        status, html = get_page(url)
        abrev = config['abrev']
        if status == 200:
            write_file(abrev, url, html)

