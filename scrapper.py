import sys
from urllib.parse import urlparse
from urllib.request import urlopen


class Scrapper(object):
    url = ''

    def __init__(self, url):
        self.url = url

    def _check_validity(self):
        try:
            urlopen(self.url)
            print('Valid URL')
            return True
        except IOError:
            print('Invalid URL')
            return False

    def read_page(self):
        is_valid = self._check_validity()

        if not is_valid:
            sys.exit()

        # Todo: Pending install BeautifulSoup
        html = urlopen(self.url).read()
        html_page = bs(html, features="lxml")
        og_url = html_page.find('meta', attrs={'name': 'og:url'})['content']
        base = urlparse(self.url)
        self.get_parquet_files(html_page, og_url, base)

    def get_parquet_files(self, html_page, og_url, base):
        links = []
        for link in html_page.find_all('a'):
            current_link = link.get('href')
            if not current_link.endswith('.parquet'):
                continue

            if og_url:
                print('current link', current_link)
                links.append(og_url['content'] + current_link)
            else:
                links.append(base.scheme + '://' + base.netloc + current_link)


        for link in links:
            try:
                wget.download(link)
            except:
                print('Download failed')