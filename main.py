import argparse
from bs4 import BeautifulSoup
from decimal import Decimal
from extractors import extractor
from functools import partial
import json
import requests
import smtplib
import sys

souper = partial(BeautifulSoup, features='html.parser')

def compute_price(url, target, price_extractor):
    soup = souper(requests.get(url).content)
    price = price_extractor(url, soup)
    return price

def main(argv):
    parser = argparse.ArgumentParser(description='Price tracker by laserpez.')
    parser.add_argument('-m', '--mail', action='store_true', help='send e-mail instead of print')
    parser.add_argument('-f', '--file', default='urls.json', help='URLs file path')
    args = parser.parse_args()

    with open(args.file, 'rt') as f:
        input = json.load(f)
        URLs = [(url, Decimal(price)) for url, price in input]

    results = [(url, compute_price(url, target, extractor), target) for url, target in URLs]
    send_report(results, send_mail=args.mail)
    return 0

def build_body(url, price, target):
    delta = price.amount - target
    body = f"Item at {url} price is still {price.amount}." if abs(delta) < 0.001 \
      else f"> Item at {url} price is now {price.amount} (difference: {delta:.2f})!"
    
    return body

def send_report(results, send_mail=False):
    with smtplib.SMTP_SSL('email-smtp.eu-central-1.amazonaws.com', 465) as server:
        server.ehlo()
        server.login("AKIAU2W3YTRDMFMDYIKC", "BOBzKJ5PyUMxT5mXCZd6m1OOg1oPCFJUTynSreWpD98R")
      
        subject = 'Pricewatch report'
        body    = "\n\n".join(build_body(url, price, target) for url, price, target in results) + "\n"
        msg     = f"Subject: {subject}\n\n{body}"

        server.sendmail("\"Pricewatch\" <psycho_78@libero.it>", 'laserpez+cash@gmail.com', msg) if send_mail else print(msg)

# entry point
sys.exit(main(sys.argv[1:]) if __name__ == "__main__" else 0)