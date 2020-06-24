# Instructions

To properly run the scrapy script, download the tutorial folder.
After the download, copy the text file that contains the path of the sites that need to be scraped and paste inside the folder spiders (the path to this folder is in the next step).
From that, open your command line prompt and navigate inside the tutorial folder: tutorial\tutorial\spiders.
Inside that working directory, run the following command: scrapy crawl sites -o data.json.
By the time one press enter, the following message will appear: Type the urls doc name with the extension: 
You should type, for example, sites_url.text. This text document should contain the website addresses that need to be scraped, one per line, and without a comma. From that, the script will run and create a json document, named data.json, inside the spiders folder.
This json document will contain a list with other jsons (one per website crawled). And for each json inside the list, it's found the logo  of the website, all the phone numbers found, and the website url. To open this document one just need to have a text editor and open the json document to have access to the data.


Note: To run this code the computer must have python and the scrapy module installed.

