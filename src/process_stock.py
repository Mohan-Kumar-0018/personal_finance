from nsetools import Nse
nse = Nse()
price = nse.get_index_list()
print("price",price)
# print(nse.get_quote('infy'))