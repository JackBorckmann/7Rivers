#V1 works better but uses a lot of credits for the AI. V2 works but not as well and uses less AI credits and more of the firecrawl credits.


from firecrawl import FirecrawlApp
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import datetime


def scrape_data(url):
    load_dotenv()
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    # scraped_data = app.scrape_url(url)
    crawl_data = app.scrape_url_url(url=url, params={
        'extractorOptions': {
        'mode': 'llm-extraction',
        'extractionPrompt': 'Based on the information on the page, extract the information from the schema. ',
        'extractionSchema': {
            "type": "object",
            "properties": {
                    "company_Name": {
                            "type": "string"
                    },
                    "executive_Overview": {
                            "type": "string"
                    },
                    "products_and_Services": {
                            "type": "string"
                    },
                    "industries_Served": {
                            "type": "string"
                    },
                    "company_URL": {
                            "type": "string"
                    }
                }
            }
        },
        'crawlerOptions': {
            'limit': 40,
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

def format_data(data, fields=None):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if fields is None:
        fields = ['executive overview', 'products and services', 'industries served', 'company name', 'company url']

    system_message = f"""You are an intelligent text extraction, conversion assistant and professional dossier creator. Your task is to extract the structured information from the given text
                    and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, with no additional commentary, explanation, or extraneous information.
                    You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                    Please process the following text and provide the output in pure JSON format with no words before or after the JSON. It is very important
                    that the information is accurate. The sections you are creating are the following: executive overview, products and services 
                    and industries served. Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served."""
    
    user_message = f"Extract the following information from the provided text:\n\n{data}\n\nInformation to extract: {fields}"

    response = client.chat.completions.create(
        #can get it to work on this but cost is high cannot get it to work on "gpt-3.5-turbo" because the amount of tokens is too high.
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    if response and response.choices:
        formatted_data = response.choices[0].message.content.strip()
        print(f"Formatted data received from API")

        try:
            parsed_json = json.loads(formatted_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Formatted data that caused the error: {formatted_data}")
            raise ValueError("The formatted data could not be decoded into JSON")
        return parsed_json
    else:
        raise ValueError("The OpenAI API response did not contain the expected choices of data.")

def save_formatted_data(formatted_data, timestamp, filename, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'sorted_{filename}_{timestamp}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Formatted data saved to {output_path}")

def main():
    while True:
        # User input to choose an action
        user_input = input("Enter 'run' to generate documents or 'quit' to exit the program: ").lower().strip()
        
        if user_input == "run":
            url = input("Enter the URL you want to scrape: ")
            try:
                timestamp = datetime.datetime.now().strftime('%m%d%H%M')
                filenames = url.split("//")[-1].split("/")[0].split(".")[0]
                raw_data = scrape_data(url)
                save_raw_data(raw_data, timestamp, filenames)
                formatted_data = format_data(raw_data)
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



