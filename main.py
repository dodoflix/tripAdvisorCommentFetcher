import time
import xlsxwriter

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def urlControl(tempUrl):
    if type(tempUrl) != str:
        return None
    tempUrl = str(tempUrl)
    list = tempUrl.split("/")
    if not list[2].lower().startswith("www.tripadvisor.com") and list[3].lower().startswith("hotel_review"):
        return False
    else:
        return True


class Review:
    def __init__(self):
        self.username = None
        self.point = None
        self.title = None
        self.text = None
        self.date = None


url = str(input("Lütfen URL'yi giriniz:"))
if not urlControl(url):
    print("Hatalı veya eksik URL girdiniz!")
else:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)
    driver.get(url)
    time.sleep(3)
    try:
        # Cookie Accept
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        pageNumbers = driver.find_element(By.CLASS_NAME, "pageNumbers")
        languageButton = driver.find_element(By.CLASS_NAME, "cvxmR")
        actions.move_to_element(languageButton).perform()
        languageButton.click()
        actions.move_to_element(pageNumbers).perform()
        time.sleep(3)
        title = driver.title
        reviewCount = driver.find_element(By.CLASS_NAME, "cdKMr.Mc._R.b").text
        reviewCount = int(reviewCount)
        reviewBox = driver.find_elements(By.CLASS_NAME, "cWwQK.MC.R2.Gi.z.Z.BB.dXjiy")
        pageCount = reviewCount // len(reviewBox)
        reviewList = []
        nextButton = driver.find_element(By.CLASS_NAME, "ui_button.nav.next.primary")
        print("Yorum çekme işlemi başlatıldı!")
        for page in range(pageCount):
            print((pageCount - 1) - page, "adet sayfa kaldı.")
            reviewBox = driver.find_elements(By.CLASS_NAME, "cWwQK.MC.R2.Gi.z.Z.BB.dXjiy")
            for review in reviewBox:
                tempReview = Review()
                tempReview.username = review.find_element(By.CLASS_NAME, "ui_header_link.bPvDb").text
                tempReview.point = int(
                    review.find_element(By.CLASS_NAME, "ui_bubble_rating").get_attribute("class").split("_")[-1]) // 10
                tempReview.title = review.find_element(By.CLASS_NAME, "fCitC").text
                tempReview.text = review.find_element(By.CLASS_NAME, "XllAv.H4._a").text
                tempReview.date = review.find_element(By.CLASS_NAME, "euPKI._R.Me.S4.H3").text.replace(
                    review.find_element(By.CLASS_NAME, "CrxzX").text, "")[1::]
                reviewList.append(tempReview)
            actions.move_to_element(nextButton).click()
            if page != pageCount - 1:
                nextButton.click()
                time.sleep(3)
        print("Yorum çekme işlemi başarıyla tamamlandı.")
        driver.close()
        print(len(reviewList), "adet yorum çekildi.")
        workbook = xlsxwriter.Workbook(title + ".xlsx")
        worksheet = workbook.add_worksheet()
        print(title, "adlı dosyaya yazılma işlemi başlatıldı.")
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
        print("Dosyaya yazılma işlemi başarıyla tamamlandı.")
        workbook.close()
    except NameError:
        print("Bir hata oldu!")
