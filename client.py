import requests

# data = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement",
#     json={
#           "title": "ad_1", "description": "Buy_car",
#           "price": 1000000, "author": "AutoClass-A"
#           },
# )
# print(data.status_code)
# print(data.json())

# data = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement",
#     json={
#           "title": "ad_1", "description": "Sell_car",
#           "price": 1500000, "author": "AutoClass"
#           },
# )
# print(data.status_code)
# print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/advertisement?title=ad_1")
# print(data.status_code)
# print(data.text)

# data = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/1",
#     json={
#           "title": "ad_1", "description": "Buy_car",
# #          "price": 900000, "author": "AutoClass-A"
#            },
# )
# print(data.status_code)
# print(data.json())

# data = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(data.status_code)
# print(data.json())