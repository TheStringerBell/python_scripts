import requests
from bs4 import BeautifulSoup
import webbrowser

from tkinter import * 

'''
Web scrapper for a torrent site which lists most popular 10 movies and opens them on CSFD.cz in a browser.
'''

root = Tk()

with open("already_seen.txt", "r") as f:
        already_seen = f.read()
        already_seen = already_seen.split("\n")

def trade_spider():
	
		
	url = "https://kat.cr/full/"
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	for link in soup.find_all("a", {"class" : "cellMainLink"}, limit = 15):
		href = "https://kat.cr" + link.get("href")
		title = link.string
		get_single_item_data(href)
	



def get_single_item_data(item_url):
	source_code = requests.get(item_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	
	for item_name in soup.find_all("ul" , {"class" : "block overauto botmarg0"}):
		for movie_name in item_name.find_all("a", limit = 1):
			movie_name = movie_name.string
			if movie_name not in already_seen:
				print(movie_name)
				with open("already_seen.txt", "a") as f:
					f.write(movie_name + "\n")
				csfd(movie_name)

	
	
def csfd(movie_name):
	
	movie_name = movie_name
	movie = movie_name.replace(":", "")
	movie = movie.replace(" ", "+")
	url = "http://www.csfd.cz/hledat/?q=" + movie
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	
	link = soup.find_all("a", {"class" : "film"}, limit = 1)
	if not link:
		
		webbrowser.open_new_tab(url)
		
		

	else:
		for link in soup.find_all("a", {"class" : "film"}, limit = 1):
			
			href = "http://www.csfd.cz" + link.get("href")
			title = link.string
			
			webbrowser.open_new_tab(href)

def DoIt(event):
	trade_spider()

def close(event):
	root.quit()

# def lprint(event):

topframe = Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

button_1 = Button(topframe, text="START", fg = "green")
button_1.bind("<Button-1>", DoIt)


button_2 = Button(topframe, text="STOP", fg = "red")
button_2.bind("<Button-1>", close)
button_1.pack()
button_2.pack()
w = Label(bottomframe, text="Saved to \"already_seen.txt\"")
w.pack()


root.mainloop()










