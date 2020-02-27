from multiprocessing import Pool
import bs4 as bs
import random
import requests
import string

#This function will generate a random 3 letter url for us#
def random_starting_url():
	#Generating our starting random 3 characters in lower case#
	starting = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(3))
	#Creating our random 3 letter url#
	url = ''.join(['http://', starting, '.com'])
	return url

#A handle for local links since some websites will have local links & not start with a http or https & start with a slash instead(browser knows but program does not know)#
def handle_local_links(url,link):
	if link.startswith('/'):
		#Join the url & the link as a list & return it# 
		return ''.join([url,link])
	else:
		return link

#This function finds all the links from our given url#
def get_links(url):
	try:
		#Grab the source code#
		resp = requests.get(url)
		#Creating our beautiful soup object that will store the source code in a certain format.The 1st paramter is--->"source" which is the text of the source code,The 2nd paramter is--->the parser)#
		soup = bs.BeautifulSoup(resp.text, 'lxml')
		#Get the contents contianed within body section of our source code#
		body = soup.body
		#Finding all links by using the <a>tags to get the hyperlinks from the body section of our source code#
		links = [link.get('href') for link in body.find_all('a')]
		#Taking our parameter "url" from our "get_links" function & passing it along with the above hyperlinks to the "handle_local_links" function#
		links = [handle_local_links(url,link) for link in links]
		#Finally,encoding all our urls & hyperlinks into ascii & converting them to string#
		links = [str(link.encode("ascii")) for link in links]
		return links
	#What if there are no links at all on the webpage.Then return an empty list & that is acceptable for our program#
	except TypeError as e:
		print(e)
		print('Got a TypeError, probably got a None that we tried to iterate over')
		return []
	#Errors while iterating through the links.Then return an empty list & that is acceptable for our program#
	except IndexError as e:
		print(e)
		print('We probably did not find any useful links, returning empty list')
		return []
	#Raised when an attribute reference or assignment fails#
	except AttributeError as e:
		print(e)
		print('Likely got None for links, so we are throwing this')
		return []
	#General exception#
	except Exception as e:
		print(str(e))
		#log this error#
		return []

#Main Function & hence we start here#
def main():
	#how many links we wish to start with#
	how_many = int(input("How many links do you wish to start with in this spider web:\n"))
	#how many processes will we have#
	p = Pool(processes=how_many)
	#This will give us a list of all 3 character random links/urls after being parsed#
	parse_us = [random_starting_url() for _ in range(how_many)]
	#Map or Send our created list of 3 character links/urls to the "get_links" function(Return type is an iterator)#
	data = p.map(get_links, [link for link in parse_us])
	#Creating a new list of the urls & sub urls found.And the code simplified looks like this-->for url_list in data<\n>for url in url_list<\n>data.append()#
	data = [url for url_list in data for url in url_list]
	#close the pool#
	p.close()
	#Save the links to a text file#
	with open('urls.txt','w') as f:
		#Convert our data object to string#
		f.write(str(data))

if __name__ == '__main__':
	main()



