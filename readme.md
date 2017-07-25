# Flatfinder

Tool to automate house finding in Spain based on the demo in my [EE24 talk](https://github.com/Achifaifa/slides/tree/master/EE24-findaflat). 

### Usage

#### Spider

* Get a starting URL by searching in idealista for flats in your prefered zone
* Put that url in the `spider-idealista.py` file, replacing whatever's already there
* run `spider-idealista.py` with scrapy and save the data to a json file (`scrapy runspider -s USER_AGENT="mozilla" -s DOWNLOAD_DELAY=3 spider-idealista.py -o data.json`). Make sure you debug the spider first and check for missing data, since the website changes from time to time. Check all the XPATHs and replace as needed. The delay avoids getting captcha'd in the website, and the scraping speed is 20 flats/minute. Getting all the results for a moderate sized city should take around an hour.
* Go to `process.py` and modify your ranges, scores and weights. The scores express how good that range is for you, and the weights how important that characteristic is.
* Run `process.py`. You should get the 50 best flats according to the scores and weights you specified. You can pipe this to a text file for future reference.

#### Updater

* Go to `getlist.py` and change the `start_url` variable for whatever search term or page you want to monitor changes in
* Run getlist.py and pipe the output to old.txt. This will create an initial snapshot against which new ones can be compared.
* Run `findnew.sh`. This will get all new flats and put them in `update.txt`. If the `xargs` line on the script is uncommented, it will open all the new flats in the default web browser.

### Dependencies

* Scrapy
* Geocoder
