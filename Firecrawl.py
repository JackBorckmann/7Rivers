#Scrape entire websites to get the raw data into a file and then parse it to get the summary we need of the data.
#start with testing it out and making it work with just our site.
#eventually we will need this to scrape 500 websites and get the data we need from them in individual files.

from pydantic import BaseModel, Field
import pprint
from typing import List
import firecrawl
from firecrawl import FirecrawlApp
import json

# Initialize the FirecrawlApp with your API key (this is my api key)
app = FirecrawlApp(api_key='fc-6ca5bb8c9a914d2d9e2d21fbe5b9d418')

class ArticleSchema(BaseModel):
    title: str
    description: str

class Schema(BaseModel):
    articles: List[ArticleSchema] = Field(..., max_items=5, description="List of top 5 articles")

#for testing purposes: scrapes only the main page of the website
#Used this for testing the code and making sure it works and not using up all credits.
def scrape_website(url):
    #will comment out these 3 lines when we are ready to scrape the whole website
    #will uncomment the block of code below these 3 for the whole website.
    scraped_url = url
    scraped_data = app.scrape_url(scraped_url, {
        'extractorOptions': {
        'extractionSchema': ArticleSchema.model_json_schema(),
        'mode': 'llm-extraction'
        },
        'pageOptions': {
            'onlyMainContent': True
        }
    })
    print(scraped_data["llm-extraction"]) #pprint is used to print the data in a more readable format for us.
    
    filename = url.split("//")[-1].split("/")[0].split(".")[0]
    print(filename)
    with open(filename, 'w') as file:
        file.write(scraped_data)
        #json.dump(crawl_result, file, indent=4) #when doing whole website change scraped_data to crawl_result
    print(f"Data scraped from {url} and saved to {filename}")

if __name__ == "__main__":
    url = input("Enter the URL you want to scrape: ")
    scrape_website(url)

    #this asks for the url from the user must be in a https:// format.
    #can add a simple loop to go through a list of companies urls and scrape them all.
    #should create a new file for each website and save the raw data in it.
    #This code also get all raw data and doesn't summarize it yet.

     #searches all the the web for anything relevant to the filename(companies name)
    #still need to submit this data into the file created above as well.
    # query = (f"Everything about {filename}")
    # search_result = app.search(query)
    # pprint.pprint(search_result)

     # Crawl whole website, will go into all subpages and extract all data from there.
    #can adjust the parameters to change what the crawler does.
    # crawl_url = url
    # params = {
    #  'pageOptions': {
    #       'onlyMainContent': True
    #  }
    # }
    # crawl_result = app.crawl_url(crawl_url, params=params) 
    # pprint.pprint(crawl_result) #pprint is used to print the data in a more readable format for us.

    #creates the filename from the domain of the website, adds the raw data from the crawl 
    #to a new json file with the filename being the domain of the website.
