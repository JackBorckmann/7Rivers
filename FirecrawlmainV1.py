#.env is where you can put in your API keys for firecrawl and openai.
#requirements.txt is a list of pip install commands needed to be done for the code to work.
#pip install -r requirements.txt

from firecrawl import FirecrawlApp
from openai import OpenAI
from dotenv import load_dotenv
import os
import google.generativeai as genai
import datetime
from urllib.parse import urlparse


def scrape_data(url):
    load_dotenv()
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    # scraped_data = app.scrape_url(url)
    crawl_data = app.crawl_url(url, params={
    'crawlerOptions': {
        'limit': 20,
        'maxDepth': 2,
        'excludes': ['/contact-us/*','/terms-conditions/*','/social_media/*','/privacy-policy/*', '/blog/*','/news/*','/events/*','/case-studies/*','/clients/*','/testimonials/*','/faq/*', 'wp-content']
        },
    'pageOptions': {
        'onlyMainContent': True
            }
        }
    )
    return str(crawl_data)
   
def save_raw_data(raw_data, timestamp, filename, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    raw_output_path = os.path.join(output_folder, f'raw_{filename}_{timestamp}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    print(f"Raw data saved to {raw_output_path}")

def format_data(data, company_URL, filename, fields=None):
    load_dotenv()
    #client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure()

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    if fields is None:
        fields = ['executive overview', 'products and services', 'industries served', 'company name', 'company url']

    prompt = f"""You are a professional dossier creator. You create dossiers for specific companies to help the sales team. You are going to help me create a dossier for the company: {filename}. Here is the link to the website for this company: {company_URL}. You do not need to only use the data to gather information, it is simply a reference to ensure that you are gathering data for the right company and not another company with the same name. It is very important that the information is accurate. The sections you are creating are the following: {fields}. You could encounter cases where you can't find the data for the fields you have to extract or the data will be in a foreign language. Please process the following text and provide the output in .txt format. It is very important that the information is accurate. Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served. Extract the following information from the provided text:\n\n{data}\n\n"""    

    response = model.generate_content(prompt)      
    formatted_data = response.candidates[0].content.parts[0].text
    return(formatted_data)

def save_formatted_data(formatted_data, timestamp, filename, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'sorted_{filename}_{timestamp}.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted_data)
    print(f"Formatted data saved to {output_path}")

def extract_domain(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Get the netloc (network location part)
    netloc = parsed_url.netloc
    # Split by dots
    parts = netloc.split('.')
    # Check if there's a 'www' prefix and remove it
    if parts[0] == 'www':
        parts = parts[1:]
    # Join remaining parts to form the domain name
    domain = '.'.join(parts[:-1])
    return domain

def main():
    while True:
        # User input to choose an action
        user_input = input("Enter 'run' to generate documents or 'quit' to exit the program: ").lower().strip()
        
        if user_input == "run":
            url = input("Enter the URL you want to scrape: ")
            try:
                timestamp = datetime.datetime.now().strftime('%m%d%H%M')
                filenames = extract_domain(url)
                raw_data = scrape_data(url)
                save_raw_data(raw_data, timestamp, filenames)
                formatted_data = format_data(raw_data, url, filenames)
                save_formatted_data(formatted_data, timestamp, filenames)
            except Exception as e:
                print(f"An error occurred: {e}")
        elif user_input == "quit":
            # Exit the program
            print("Exiting the program.")
            break
        else:
            # Handle unexpected input
            print("Invalid input. Please enter 'run' or 'quit'.")


if __name__ == "__main__":
    main()