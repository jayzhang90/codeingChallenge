import json
import re
from collections import OrderedDict

products = {}  # key : manufacturer , value : [product]

# read products.txt file
with open('products.txt') as json_file:
    for line in json_file:
        product = json.loads(line)
        manufacturer = product["manufacturer"].lower()
        if manufacturer in products:
            products[manufacturer].append(product)
        else:
            products[manufacturer] = [product]

listings = []  # [listing]

# read listings.text file
with open('listings.txt') as json_file:
    for line in json_file:
        listings.append(json.loads(line))

result = {}  # key: product name, value : [listing]
for value in products.values():
    for value_product in value:
        product_name = value_product["product_name"]
        result[product_name] = []


def check_manufacturer(string_to_check, pattern_list):
    return_value = ""
    for pattern in pattern_list:
        if re.search("\\b"+pattern+"\\b", string_to_check, re.IGNORECASE):
            return_value = pattern  # match
            break
    return return_value  # not match

def check_model(string_to_check, pattern_list):  # string_to_check = title , pattern_list = [product]
    return_value = None
    for pattern in pattern_list:  # pattern = product
        model = pattern["model"]
        if re.search('\\b'+model+'\\b', string_to_check, re.IGNORECASE):    # check for exact match
            return_value = pattern  # match
            break

        # if model contain space, it's ok to remoce the space, eg: "T 100" matches "T100"
        elif ' ' in model and re.search('\\b'+model.replace(' ','')+'\\b', string_to_check, re.IGNORECASE):
            return_value = pattern  # match
            break

        # if model contain '-', it's ok to remoce the '-', eg: "T-100" matches "T100"
        elif '-' in model and re.search('\\b' + model.replace('-', '') + '\\b', string_to_check, re.IGNORECASE):
            return_value = pattern  # match
            break

        # if model contain '_', it's ok to remoce the '_', eg: "T_100" matches "T100"
        elif '_' in model and re.search('\\b' + model.replace('_', '') + '\\b', string_to_check, re.IGNORECASE):
            return_value = pattern  # match
            break

    return return_value


for listing in listings:  # key is manufacturer
    # check whether title contain manufacturer or not
    match_manu_in_title = check_manufacturer(listing["title"], list(products.keys()))
    if match_manu_in_title != "":  # if yes
        # check whether title contain  model or not
        product = check_model(listing["title"], (products[match_manu_in_title]))
        if product is not None:
            listing = OrderedDict([("title",listing["title"]),("price",listing["price"]),("manufacturer",listing["manufacturer"]),("currency",listing["currency"])])
            result[product["product_name"]].append(listing)

with open('data.txt', 'w') as outfile:
    for product in result.keys():
        outfile.write("{}\n".format(json.dumps(OrderedDict([("product_name",product), ("listings",result[product])]), ensure_ascii=False)))
