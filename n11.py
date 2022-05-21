import requests
from bs4 import BeautifulSoup


class N11:
    all_review = {
        "comments": []
    }

    def __init__(self, url):
        print("n11")
        self.url = url
        self.scrap_reviews()

    def scrap_reviews(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/100.0.4896.127 Safari/537.36'}
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        product_id = soup.find("a", attrs={"id": "getWishList"}).get("data-productid")

        n11_review_url = f"https://www.n11.com/component/render/productReviews?page=1&productId={product_id}"

        response = requests.get(url=n11_review_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            page_count = int(soup.find("a", attrs={"class": "pageLink last"}).get_text())
        except Exception:
            page_count = 1

        for i in range(page_count):
            n11_review_url = f"https://www.n11.com/component/render/productReviews?page={i + 1}&productId={product_id}"

            response = requests.get(url=n11_review_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            in_page_comments = soup.find_all("li", attrs={"class": "comment"})

            for comment in in_page_comments:
                id = comment.get("data-reviewid")
                owner = comment.find("span", attrs={"class": "userName"}).get_text().strip()
                owner_comment = comment.find("p").get_text().strip()
                comment_date = comment.find("span", attrs={"class": "commentDate"}).get_text().strip()

                add_dict = {
                    "id": id,
                    "owner": owner,
                    "comment": owner_comment,
                    "date": comment_date
                }

                flag = 0
                for ids in self.all_review["comments"]:
                    if id == ids["id"]:
                        flag = 1
                        break
                if flag == 0:
                    self.all_review["comments"].append(add_dict)
