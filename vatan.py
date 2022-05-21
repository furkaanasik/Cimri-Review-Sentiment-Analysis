import requests
from bs4 import BeautifulSoup


class Vatan:
    all_review = {
        "comments": []
    }

    def __init__(self, url):
        print("vatan")
        self.url = url
        self.scrap_reviews()

    def scrap_reviews(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/100.0.4896.127 Safari/537.36'}

        product_id = self.url.split(".html")[0].split("-")[-1]
        product_review_url = f"https://www.vatanbilgisayar.com/ProductDetail/Comments/?productId={product_id}"

        response = requests.get(url=product_review_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        all_comments = soup.find_all("div", attrs={"class": "col-md-12 ds-table comment-items"})

        for elements in all_comments:
            id = elements.find("div", attrs={"class": "comment-likebtn"}).find("a").get("data-commentid")
            owner = elements.find("div", attrs={"class": "comment-name"}).find("span").get_text()
            comment = elements.find("div", attrs={"class": "comment"}).get_text(strip=True)
            date = elements.find("span", attrs={"class": "replaced-date"}).get_text()

            add_dict = {
                "id": id,
                "owner": owner,
                "comment": comment,
                "date": date
            }

            flag = 0
            for ids in self.all_review["comments"]:
                if id == ids["id"]:
                    flag = 1
                    break

            if flag == 0:
                self.all_review["comments"].append(add_dict)
