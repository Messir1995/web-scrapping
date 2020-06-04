import requests
from bs4 import BeautifulSoup
import csv
class Scraping_information:
	path = "output.csv"

	def __init__(self):
		pass

	#get data about object of search
	def data_about_site(self):
		self.page_link = 'https://dodopizza.ru/moscow#'
		#self.page_link = input('Enter your web-site address:')
		#self.point = input ('Enter what we need to search:')
		self.point = 'locality-selector-popup__content'


	#get code from page
	def get_page(self):
		self.page_response = requests.get(self.page_link, timeout=5)

	#find information about place
	def get_data(self): 
		self.page_content = BeautifulSoup(self.page_response.content, "html.parser")
		self.search_data = self.page_content.find_all(class_=self.point)
		print(self.search_data)
	
	#write our data to csv
	def csv_writer(self):
		with open(self.path, "w", newline='') as csv_file:
			writer = csv.writer(csv_file, delimiter=';')
			i=0
			#for depth in len(list(self.point_info[0])):
			for depth in range(len(list(data.point_info[0]))):
			#for rows in self.point_info:
				writer.writerow(self.point_info[0][i])
				writer.writerow(self.point_info[1][i])
				writer.writerow(self.point_info[2][i])
				i+=1

	

data = Scraping_information()
data.data_about_site()
data.get_page()
data.get_data()
i=1
#parsing information
data.point_info = [["Name"], ["Metro"], ["Time"]]
for point in data.search_data:
	temporary_info=[]
	for string in point.strings:
		temporary_info.append(repr(string))
	p=point.find_all(class_='contacts-pizzerias__item contacts-pizzerias__item_metro')
	if not (point.find_all(class_='contacts-pizzerias__item contacts-pizzerias__item_metro')):
		data.point_info[0].append(temporary_info[0])
		data.point_info[1].append("Point has no metro")
		data.point_info[2].append(temporary_info[1])
	else:
		data.point_info[0].append(temporary_info[0])
		data.point_info[1].append(temporary_info[1])
		data.point_info[2].append(temporary_info[2])
	i+=1
#data.csv_writer()