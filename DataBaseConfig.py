import requests
from bs4 import BeautifulSoup
import sqlite3

#? Getting all the brands of jumia smart phones and storing them in brands list without duplication
brands=[]
url = 'https://www.jumia.com.tn/smartphones/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
product_links = soup.find_all('a', {'class': 'core'})

for link in product_links:
    data_brand = link.get('data-brand')
    brands.append(data_brand)

brands=list(dict.fromkeys(brands))



#? Creating a product info dictionary that has all of the infos then save the product infos in a list 

product_info_list = []

for link in product_links:
    data_brand = link.get('data-brand')
    data_name = link.get('data-name')
    data_price = link.get('data-price')
    data_image_url = link.find('img')['data-src']

    # create the product info dictionary and add it to the list
    product_info = {'brand': data_brand, 'name': data_name, 'price': data_price, 'image_url': data_image_url}
    product_info_list.append(product_info)

#? Creating a database and to save the data in it
conn=sqlite3.connect('jumiaSmartPhones.db')
c=conn.cursor()

#---------------------------------------------------------------------Table brand---------------------------------------------------------------------------------

#*The red comment is related to the database the first one is creating a new table brand the secound is inserting the brands to the table with an id i
# c.execute(''' CREATE TABLE brand(brandName TEXT,brandId INT) ''')
# for i in range(len(brands)):
#      val=brands[i]
#      c.execute(''' INSERT INTO brand VALUES(?,?) ''',(val,i))

# conn.commit()

#Fetching the inserted data
# c.execute(''' select * from brand ''')
# res=c.fetchall()
# print(res)

#---------------------------------------------------------------------Table Smart phone---------------------------------------------------------------------------------
#* Creating the table SmartPhone and inserting the data from the list of dictionary
# c.execute(''' CREATE TABLE SmartPhone(brand TEXT,nom TEXT,price INT,imgURL TEXT) ''')
# for info in product_info_list:
#      val_brand=info['brand']
#      val_name=info['name']
#      val_price=info['price']
#      val_img=info['image_url']
#      c.execute(''' INSERT INTO SmartPhone VALUES(?,?,?,?) ''',(val_brand,val_name,val_price,val_img))
# conn.commit()

#*Fetching the inserted data
# c.execute(''' select * from SmartPhone ''')
# res=c.fetchall()
# print(res)

#------------------------------------------------------
# query = 'SELECT brandName FROM brand'

# # Retrieve brand names from SQLite database
# cursor = conn.execute(query)
# brand_names = [row[0] for row in cursor.fetchall()]

# conn.close()


