# python -m pip install requests
# => get data from web (html,json, xml)
# python -m pip install beautifulsoup4
# => parse html

# Git ma rakhne tarika
# git config --global user.name "Jiban Chaudhary"
# git config --global user.email "rajbanshijiban288@gmail.com"
# git add .
# git commit -m "Finish Project"
# git status -- modified project

import requests 
from bs4 import BeautifulSoup
import json
import csv
from tabulate import tabulate  # for table display
import pandas as pd

url = "https://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code!=200:
        print("Failed to fetch the page..")
        return []
    # Set encoding explicitly to handle special character correctly
    response.encoding = response.apparent_encoding
    
    #print(response.text)


    # object banako 
    soup = BeautifulSoup(response.text,"html.parser") 
    books = soup.find_all("article", class_="product_pod")
    all_books = []
    for book in books:
        title = book.h3.a['title']
      #  print(title)
        
        price_text =book.find("p", class_="price_color").text
        
        currency = price_text[0]
        price = float(price_text[1:])
        all_books.append(
            {
                "title":title,
                "currency":currency,
                "price":price,
            }
        )
       # print(title,currency,price)
       # print(all_books)
    return all_books
        


books = scrape_books(url)

with open("books.json","w", encoding="utf-8") as f:
    
    
    json.dump(books,f, indent=4, ensure_ascii=False)
    


# Save books data to CSV file
with open("books.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["title", "currency", "price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write column names
    writer.writerows(books)  # Write all book data

print("✅ Data saved to books.csv successfully!")




if not books:
    print("No books found.")
else:
    #  Step 2: Display in table format
    print(tabulate(books, headers="keys", tablefmt="grid"))
df = pd.DataFrame(books)
df.to_csv("books.csv", index=False, encoding="utf-8")
print("✅ Saved data to books.csv")