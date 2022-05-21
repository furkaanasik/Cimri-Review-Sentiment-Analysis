import requests


class Trendyol:
    all_review = {
        "comments": []
    }

    def __init__(self, url):
        print("trendyol")
        self.url = url
        self.scrap_reviews()

    def scrap_reviews(self):
        # Get product id and merchant id from url
        merchant_id = int(self.url.split("&")[1].replace("merchantId=", ""))
        product_id = int(self.url.split("?")[0].split("-")[-1])

        product_review_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}" \
                             f"?merchantId={merchant_id}" \
                             f"&storefrontId=1&culture=tr-TR&order=5&searchValue=&onlySellerReviews=false&page=0 "

        # Get Trendyol data.
        response = requests.get(url=product_review_url)
        json_response = (response.json())

        # Get productReviews json.
        product_reviews = json_response["result"]["productReviews"]

        # Get total page count.
        total_page = int(product_reviews["totalPages"]) + 1

        for i in range(0, total_page):
            product_review_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}" \
                                 f"?merchantId={merchant_id}" \
                                 f"&storefrontId=1&culture=tr-TR&order=5&searchValue=&onlySellerReviews=false&page={i} "

            # Get Trendyol data.
            response = requests.get(url=product_review_url)
            json_response = (response.json())

            # Get productReviews json.
            product_reviews = json_response["result"]["productReviews"]

            # Get content array in json.
            content = product_reviews["content"]

            # Get id, owner, comment, rate, date, isElite, isInfluencer information from json file.
            # Add these information data all_review json file.
            for review in content:
                id = review["id"]
                owner = review["userFullName"]
                comment = review["comment"]
                rate = review["rate"]
                date = review["lastModifiedDate"]
                is_elite = review["isElite"]
                is_influencer = review["isInfluencer"]

                add_dict = {
                    "id": id,
                    "owner": owner,
                    "comment": comment,
                    "rate": rate,
                    "date": date,
                    "is_elite": is_elite,
                    "is_influencer": is_influencer
                }

                flag = 0
                for ids in self.all_review["comments"]:
                    if id == ids["id"]:
                        flag = 1
                        break

                if flag == 0:
                    self.all_review["comments"].append(add_dict)

