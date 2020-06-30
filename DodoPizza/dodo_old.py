import requests
from bs4 import BeautifulSoup
import csv
import time
class Scraping_information:
	path = "output.csv"

	def __init__(self):
		pass

	#get data about object of search
	#link is link where we search
	#point is class or tag. Our information is inside point
	def data_about_site(self, link, point):
		self.page_link = link
		self.point = point

	#get code from page
	def get_page(self):
		self.page_response = requests.get(self.page_link, timeout=15)
		time.sleep(1)

	#find information about place
	def get_data(self): 
		self.page_content = BeautifulSoup(self.page_response.content, "html.parser")
		self.search_data = self.page_content.find_all(class_=self.point)
		self.city = self.page_content.find_all(class_='header__about-slogan-text_link')

	
	

	

