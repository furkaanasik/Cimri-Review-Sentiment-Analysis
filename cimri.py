import requests
import io
import n11
import trendyol
import vatan
import json

from bs4 import BeautifulSoup


class Cimri:
    url = ""

    # it obligation definition variable for beautiful soup and requests
    soup = None
    response = None
    session = None
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/100.0.4896.127 Safari/537.36'}

    brand_name_links = []
    redirect_links = []
    product_links = []

    saler_sites = None

    def __init__(self, url):
        Cimri.url = url
        Cimri.main_framework()

    @staticmethod
    def main_framework():
        # Send requests cimri site
        Cimri.request_cimri_site()

        # Scrap brand name and redirect links
        Cimri.scrap_brand_name_and_redirect_links()

        # Scrap product links
        Cimri.scrap_product_links()

        # Extriction product links
        Cimri.extriction_product_links_to_class()

        # Create csv for all sites.
        Cimri.create_json()

    # Request main cimri url
    @staticmethod
    def request_cimri_site():
        Cimri.session = requests.Session()
        Cimri.response = Cimri.session.get(url=Cimri.url, headers=Cimri.headers)
        Cimri.soup = BeautifulSoup(Cimri.response.content, "html.parser")
        Cimri.saler_sites = Cimri.soup.find_all("tr", attrs={"class": "s17f9cy4-3 bkOZxz"})

    # Scrap brand name links
    @staticmethod
    def scrap_brand_name_and_redirect_links():
        for sites in Cimri.saler_sites:
            try:
                redirect = sites.find("a", attrs={"class": "s17f9cy4-5 hhrBHG"})
                main_site = redirect.findChild().get("alt")
                Cimri.brand_name_links.append(main_site)
                Cimri.redirect_links.append(redirect.get("href"))
            except Exception:
                continue

    # Scrap product links
    @staticmethod
    def scrap_product_links():
        for i in range(len(Cimri.redirect_links)):
            Cimri.response = Cimri.session.get(url=Cimri.redirect_links[i], headers=Cimri.headers)
            Cimri.soup = BeautifulSoup(Cimri.response.content, "html.parser")
            print(Cimri.response)
            try:
                script = io.StringIO(Cimri.soup.find("script").get_text(strip=True)).readline()[11:-3]
                Cimri.product_links.append(script)
            except Exception:
                pass
        print(len(Cimri.product_links))

    # Extriction product links
    @staticmethod
    def extriction_product_links_to_class():
        for pl in Cimri.product_links:
            main_site_name = pl.split(".")[1]

            match main_site_name:
                # Create trendyol class
                case "trendyol":
                    trendyol.Trendyol(pl)

                # Create n11 class
                case "n11":
                    n11.N11(pl)

                # Create vatan class
                case "vatanbilgisayar":
                    vatan.Vatan(pl)

    @staticmethod
    def create_json():
        trendyol_data = trendyol.Trendyol.all_review
        with open("trendyol.json", "w+") as f:
            json.dump(trendyol_data, f)

        n11_data = n11.N11.all_review
        with open("n11.json", "w+") as f:
            json.dump(n11_data, f)

        vatan_data = vatan.Vatan.all_review
        with open("vatanbilgisayar.json", "w+") as f:
            json.dump(vatan_data, f)
