from price_parser import Price
from re import match
from urllib.parse import urlparse

class ExtractNull():
    def __call__(self, url, soup):
        netloc = urlparse(url).netloc
        raise NotImplementedError(f"domain {netloc} is not handled")

class BaseExtractor:
    def __init__(self, next):
        self._next = next

    def __call__(self, url, soup):
        netloc = urlparse(url).netloc
        return self.handle(url, soup) if match(self.domain(), netloc) \
          else self._next(url, soup)
    
    def handle(self, url, price):
        raise NotImplementedError()

class ExtractIsadore (BaseExtractor):
    def domain(self): return "(www.)?isadore.com"
    
    def handle(self, url, soup):
        price_p = soup.find_all('span', attrs={'class': 'price'})[0]
        price = Price.fromstring(price_p.get_text())
        return price

class ExtractLaPassione (BaseExtractor):
    def domain(self): return "(www.)?lapassione.cc"

    def handle(self, url, soup):
        price_p = soup.find("span", {"id": "ProductPrice"})
        price = Price.fromstring(price_p.get_text())            
        return price

class ExtractScienceInSport (BaseExtractor):
    def domain(self): return "(www.)?scienceinsport.com"

    def handle(self, url, soup):
        pip = soup.find_all(attrs={'class': 'product-info-price'})[0]
        price_p = pip.find_all('span', attrs={'data-price-type': 'finalPrice'})[0]
        price = Price.fromstring(price_p.get_text())
        return price

class ExtractWiggle (BaseExtractor):
    def domain(self): return "(www.)?wigglesport.it"
    
    def handle(self, url, soup):
        price_p = soup.find_all('p', attrs={'class': 'bem-pricing__product-price'})[0]
        price = Price.fromstring(price_p.get_text())
        return price

extractor = ExtractScienceInSport(
            ExtractWiggle(
            ExtractIsadore(
            ExtractLaPassione(
            ExtractNull()))))