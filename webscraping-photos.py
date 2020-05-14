import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from itertools import chain
from urllib.request import urlopen, Request
import os
import time

class PlazaVea():
  def __init__(self):
    self.driver = webdriver.Chrome(executable_path="D:/Aplicaciones/automation-browser/drivers/chromedriver.exe")      

  def entry(self):   
    pathS = './img/Supermercado/'
    pathE = './img/Electro/'
    base_url = 'https://www.plazavea.com.pe'
    self.driver.maximize_window()    
    self.driver.implicitly_wait(10)
    self.driver.get(base_url)

    #supermarket
    self.driver.find_element_by_xpath('//div[@id="event-food"]').click()
    time.sleep(10)    

    subMenusMarket = self.driver.find_element_by_xpath("/html[1]/body[1]/div[3]/header[1]/section[1]/div[3]/div[2]/div[1]/ul[1]/div[1]")    
    titleSubMenusMarket = subMenusMarket.find_elements_by_xpath('li[@class="MainMenu__category__item " or "MainMenu__category__item active"]/a')
    subMenus2Market = subMenusMarket.find_elements_by_xpath('div[contains(@class, "MainMenu__subcategory")]')
    time.sleep(10)       
    for i, subMenu2Market in enumerate(subMenus2Market):      
      titleSubMenusMarket[i].click() 
      titleFileSubMenu = titleSubMenusMarket[i].text   
      time.sleep(10) 
      os.makedirs(pathS + titleFileSubMenu)      
      if i == 0:        
        subMenu2Market = subMenu2Market.find_element_by_class_name('MainMenu__subcategory__content')        
        # titleSubMenu2Market = subMenu2Market.find_elements_by_xpath('div/h3/a')
        subMenus3Market = subMenu2Market.find_elements_by_class_name("MainMenu__subcategory__section")
        for i, subMenu3Market in enumerate(subMenus3Market):          
          titleSubMenus3Market = subMenu3Market.find_element_by_xpath('h3/a')
          titleFileSubMenu3 = titleSubMenus3Market.text
          os.makedirs(pathS + titleFileSubMenu + '/' + titleFileSubMenu3)
          subMenus4Market = subMenu3Market.find_elements_by_xpath('ul/li')
          for i, subMenu4Market in enumerate(subMenus4Market):            
              titleSubMenus4Market = subMenu4Market.find_element_by_xpath('a')
              titleFileSubMenu4 = titleSubMenus4Market.text
              os.makedirs(pathS + titleFileSubMenu + '/' + titleFileSubMenu3 + '/' + titleFileSubMenu4)
              urlMenu4 = subMenu4Market.find_element_by_xpath('a').get_attribute("href")                    
              self.driver.execute_script("window.open('');")
              self.driver.switch_to.window(self.driver.window_handles[1])          
              self.driver.get(urlMenu4)  
              time.sleep(10)
              self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              SCROLL_PAUSE_TIME = 0.5
              # Get scroll height
              last_height = self.driver.execute_script("return document.body.scrollHeight")
              while True:
              # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)              
              # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height                          

              allProducts = self.driver.find_element_by_xpath('/html/body/div[3]/main/div/div[4]/div/section[2]/div[2]/div[2]/div[2]/div[2]/div')
              for iprod, allProduct in enumerate(allProducts.find_elements(By.CLASS_NAME, 'Showcase__name')):
                titleFileProduct = allProduct.text
                os.makedirs(pathS + titleFileSubMenu + '/' + titleFileSubMenu3 + '/' + titleFileSubMenu4 + '/' + titleFileProduct)
                urlProducto = allProduct.get_attribute("href")        
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[2])          
                self.driver.get(urlProducto)  
                time.sleep(10)      
                imageObjects = self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div[3]/div[1]/div[2]/ul/div[1]/div')
    
                for i, imageObject in enumerate(imageObjects.find_elements(By.TAG_NAME, 'a')):
                  urlImageNormal = imageObject.get_attribute('rel')
                  urlImageZoom = imageObject.get_attribute('zoom')
                  urllib.request.urlretrieve(urlImageNormal, pathS + titleFileSubMenu + '/' + titleFileSubMenu3 + '/' + titleFileSubMenu4 + '/' + titleFileProduct + '/' + str(i) +" - Normal.webp")
                  urllib.request.urlretrieve(urlImageZoom, pathS + titleFileSubMenu + '/' + titleFileSubMenu3 + '/' + titleFileSubMenu4 + '/' + titleFileProduct + '/' +str(i) + " - zoom.webp")

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[1])
              #endproducts
              self.driver.close()
              self.driver.switch_to.window(self.driver.window_handles[0])
    self.driver.quit()
PlazaVea = PlazaVea()
PlazaVea.entry()

