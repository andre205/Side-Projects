import urllib
import json
import webbrowser

articlecounter = 0
running  = 1
print "Welcome to the Random Wikipedia Article Generator"
while (running):

	url = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=10&format=json"
	json_response = urllib.urlopen(url)
	fullquery = json.loads(json_response.read())
	#str1 = ''.join(dict.items(fullquery["query"]))
	#data = json.loads(str1)

	#for i in range(0,9):
	#	print fullquery["query"]["random"][i]["title"]
	#	print fullquery["query"]["random"][i]["id"]


	print "Would you like to read about " + fullquery["query"]["random"][articlecounter]["title"] + "?"
	choice = 0
	while choice < 1 or choice > 3:
		response = raw_input("1. Yes\n2. No\n3. Quit\n")
		if response == "":
			choice = 2
		if response != "":
			try:
				choice = int(response)
			except ValueError:
				print "\nPlease enter a valid response (1 or 2)."
	if choice == 1:
		webpageurl = "https://en.wikipedia.org/?curid=" + str(fullquery["query"]["random"][articlecounter]["id"])
		webbrowser.open(webpageurl,2)
		#open the article
		articlecounter = articlecounter + 1;
		
	elif choice == 2:
		articlecounter = articlecounter + 1;
		if articlecounter == 9:
			url = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=10&format=json"
			json_response = urllib.urlopen(url)
			fullquery = json.loads(json_response.read())
			articlecounter = 0
	elif choice == 3:
		running = 0	
	else:
		print "something went wrong"
	
