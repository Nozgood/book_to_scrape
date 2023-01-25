import requests
import csv
import os
from bs4 import BeautifulSoup

# init variables
links = []
books = []
dataDirPath = "/Users/nowfeel/Python/book_to_scrape/data/" # path to save img files
imgDirPath = "/Users/nowfeel/Python/book_to_scrape/data/images/"
bookImgIndex = 0

headers = ["product_page_url",
           "title",
           "upc",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "image_url",
           "description",
           "category",
           "review_rating",
           ]

poetryCat = 0
historicalFiction = 0
fiction = 0
mystery = 0
history = 0
youngAdult = 0
business = 0
default = 0
poetry = 0


# loop to get all the pages links (prepare pages links to Extract)
for i in range(1, 2, 1):
    parentUrl = "https://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    res = requests.get(parentUrl)
    if res.ok:
        page = BeautifulSoup(res.text, 'html.parser')
        divLink = page.findAll("div", class_="image_container")
        for singleDiv in divLink:
            aTag = singleDiv.find("a")
            link = "https://books.toscrape.com/catalogue/" + aTag["href"]
            links.append(link)
    else:
        print("bad res from fetching")

# loop to get all the books
# Extract and Transform
for i in range(0, len(links), 1):
    res = requests.get(links[i])
    if res.ok:
        upcValue = ""
        priceWithTax = ""
        priceWithoutTax = ""
        availableValue = ""
        imgUrl = ""
        bookPage = BeautifulSoup(res.content, "html.parser")

        # Get the title of the book and format it to string
        titleBook = bookPage.find("div", class_="col-sm-6 product_main").find("h1").string
        print("livre numéro " + str(i + 1) + " : " + titleBook)
        # Get the UPC, price (excl/incl tax), availability information from the table in the html page + format currency
        productInfoTable = bookPage.find("table")
        allTr = productInfoTable.findAll("tr")
        for tr in allTr:
            titleTr = tr.find("th").string
            if titleTr == "UPC":
                upcValue = tr.find("td").string
            elif titleTr == "Price (excl. tax)":
                priceWithTax = tr.find("td").string.replace("Â", "")
            elif titleTr == "Price (incl. tax)":
                priceWithoutTax = tr.find("td").string.replace("Â", "")
            elif titleTr == "Availability":
                availabilitySentence = tr.find("td").string.split("(")
                sentenceSplit = availabilitySentence[1].split()
                availableValue = sentenceSplit[0]

        # get the product description
        pTags = bookPage.findAll("p")
        description = pTags[3].text

        # get the category
        breadCrumb = bookPage.find("ul", class_="breadcrumb")
        liBreadCrumb = breadCrumb.findAll("li")
        category = liBreadCrumb[2].text.replace("\n", "").replace("ô", 'o')
        if category == "Poetry":
            poetry += 1
        i

        # get the review rating
        pTagStars = bookPage.find("p", class_="star-rating")
        classPtagStars = pTagStars["class"]
        reviewRating = classPtagStars[1]

        # get the image url
        imgTag = bookPage.find("div", class_="item active").find("img")
        imgTitle = imgTag["alt"]
        imgUrl = imgTag["src"].replace("../../", "https://books.toscrape.com/")

        book = [
            links[i],
            titleBook,
            upcValue,
            priceWithTax,
            priceWithoutTax,
            availableValue,
            imgUrl,
            description,
            category,
            reviewRating,
        ]
        books.append(book)
    else:
        print("bad res from fetching book url")

# Loading datas
with open('/Users/nowfeel/Python/book_to_scrape/data/scraps-books.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for book in books:
        writer.writerow(book)
    print("\n ------------ fichier csv crée ------------ \n")
    print("livres dans la catégorie poésie : " + str(poetry))

for book in books:
    bookImgIndex += 1
    print("image du livre " + book[1] + " téléchargée")
    test = os.path.join(imgDirPath + str(bookImgIndex) + "-" + book[1].replace(" ", "-").replace("/", "-") + ".jpg")
    with open(test, "wb") as file:
        imgScrap = requests.get(book[6])
        if res.ok:
            file.write(imgScrap.content)
        else:
            print("error during image's download")

