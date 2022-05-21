import n11
import trendyol
import vatan
from cimri import Cimri

# Get url from user
url = 'https://www.cimri.com/cep-telefonlari/en-ucuz-apple-iphone-11-128gb-akilli-cep-telefonu-fiyatlari,a331840845'

# Scrap cimri site
scrap_main_cimri_site = Cimri(url)

print(len(trendyol.Trendyol.all_review["comments"]))
print(len(n11.N11.all_review["comments"]))
print(len(vatan.Vatan.all_review["comments"]))
