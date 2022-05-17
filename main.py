import os
import xlsxwriter

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class Review:
    def __init__(self):
        self.username = None
        self.point = None
        self.title = None
        self.text = None
        self.date = None


path = "{}/storage".format(os.getcwd())
if not os.path.exists(path):
    os.makedirs(path)

url = str(input("TripAdvisor URL:"))
url = url.replace("-Reviews", "-Reviews%s")
url = "{}#REVIEWS".format(url)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url % "")
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
driver.find_element(By.CLASS_NAME, "bahwx.Vm._S").click()
title = driver.title
print("Comment fetching on", title, "has started.")

reviewList = []

content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
count = 0
reviewCount = int(soup.find('span', attrs={'class': 'cdKMr Mc _R b'}).text)
nextButton = driver.find_element(By.CLASS_NAME, "ui_button.nav.next.primary")
while count < reviewCount - 10:
    print((reviewCount - count) / 10, "page(s) left.")
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    for reviewBox in soup.find_all('div', attrs={'class': 'cWwQK MC R2 Gi z Z BB dXjiy'}):
        review = Review()
        review.username = reviewBox.findNext('a', attrs={'class': 'ui_header_link bPvDb'}).text
        review.point = reviewBox.findNext('span', attrs={'class': 'ui_bubble_rating'})['class'][-1][-2]
        review.title = reviewBox.findNext('a', attrs={'class': 'fCitC'}).text
        review.text = reviewBox.findNext('q', attrs={'class': 'XllAv H4 _a'}).text
        review.date = reviewBox.findNext('span', attrs={'class': 'euPKI _R Me S4 H3'}).text.split(':')[-1][1::]
        reviewList.append(review)
    count += 10
    nextButton.click()
    x = driver.find_element(By.CLASS_NAME, "cWwQK.MC.R2.Gi.z.Z.BB.dXjiy")
    y = driver.find_element(By.CLASS_NAME, "cWwQK.MC.R2.Gi.z.Z.BB.dXjiy")
    while x == y:
        y = driver.find_element(By.CLASS_NAME, "cWwQK.MC.R2.Gi.z.Z.BB.dXjiy")
workbook = xlsxwriter.Workbook(path + "/" + title + ".xlsx")
worksheet = workbook.add_worksheet()
print("Writing to", title + ".xlsx")
row = 0
for review in reviewList:
    column = 0
    worksheet.write(row, column, review.username)
    column += 1
    worksheet.write(row, column, review.date)
    column += 1
    worksheet.write(row, column, review.point)
    column += 1
    worksheet.write(row, column, review.title)
    column += 1
    worksheet.write(row, column, review.text)
    row += 1
print("Writing finished successfully.")
workbook.close()
driver.close()
