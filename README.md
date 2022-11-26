# DogSavior
Scrapes and curates in danger pets from local shelters

First install all uninstalled dependancies by running 
python3 -m pip install MISSINGDEPENDANCY

Once installed navigate to the correct directory and run the main program with 
python main.py

the user is first givin a choise to input a custom URL (expiramental feature, this may change to 5 digit zip code, which auto searches the nearby shelters)
if this is declined the program looks to check if a 'doglist' file already exists to read from in the present working directory
if it does not it will scrape the URL to create one
it then filters the results for unwanted strings caught by the scraper
this filtered list of dog ID numbers is then stored as a doglist.json file in the local directory

the program will then proceed to iterate thru the doglist and querry the shelter's website for each dogID to find a picture and description of the ascociated dog
these are saved as files to the working directory, this results in a .txt and a .jpeg file for each dog, these files are named with the corrosponding dogID

this step is skipped if the dog's txt and jpeg file already exist in the working directory

after downloading the description and picture for all dogs in the doglist, the program will construct a simple index.html page with each dogs picture and description in no particular order (A.I. neural net will be used to sort this in the future)

after the htmlpage is written the program will launch a local http server on a secure port to serve the information to the user
the pictures of the dogs on the local https site will contain links to the original post on the shelter's website
