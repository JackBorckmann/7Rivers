#.env is where you can put in your API keys for firecrawl and openai.
#requirements.txt is a list of pip install commands needed to be done for the code to work.
#pip install -r requirements.txt

from firecrawl import FirecrawlApp
from openai import OpenAI
from dotenv import load_dotenv
import os
import csv
import json
import asyncio


def scrape_data(url):
    load_dotenv()
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    # scraped_data = app.scrape_url(url)
    crawl_data = app.crawl_url(url, params={
    'crawlerOptions': {
        'limit': 20,
        'maxDepth': 2,
        'excludes': ['/contact-us/*','/terms-conditions/*','/social_media/*','/privacy-policy/*', '/blog/*','/news/*','/events/*','/case-studies/*','/clients/*','/testimonials/*','/faq/*']
        },
    'pageOptions': {
        'onlyMainContent': True
            }
        }
    )
    return str(crawl_data)


def format_data(data, fields=None):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    #can change these (fields, user_message, system_message) to fit the specific data we want to extract and want to pick through.
    #the scrape will scrape through everything and this is the sorter.
    #still unaware of how to change the parameters on the scrape to only scrape the stuff we want. Benefit of that would be saves us some credits on firecrawl.
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
        model="gpt-4-0125-preview",
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
        print(f"Formatted data received from API: {formatted_data}")

        try:
            parsed_json = json.loads(formatted_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Formatted data that caused the error: {formatted_data}")
            raise ValueError("The formatted data could not be decoded into JSON")
        return parsed_json
    else:
        raise ValueError("The OpenAI API response did not contain the expected choices of data.")

def save_formatted_data(formatted_data, filename, output_folder='output'):
    folder_path = os.path.join(output_folder, filename)
    os.makedirs(folder_path, exist_ok=True)
    output_path = os.path.join(folder_path, f'sorted_{filename}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Formatted data saved to {output_path}")

async def generate_docs(csv_file):
    # Path to the root directory for docs
    root_directory = "docs"
    os.makedirs(root_directory, exist_ok=True)
    
    # Reading in the csv file
    with open(csv_file, newline='', encoding='utf-8', errors='replace') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            company_name, url, publicly_traded, consulting = row[0], row[1], row[2], row[3]
            # Skip companies that are not publicly traded
            # if publicly_traded.lower() == "yes" or publicly_traded.lower() == "n/a":
            #     print(f"Skipping {company_name} because it is publicly traded.")
            #     continue
            #skip companies that do not have a url
            if url.lower() == "n/a":
                print(f"Skipping {company_name} because it does not have url.")
                continue
            #Skip companies that are consulting companies
            # if consulting.lower() == "yes":
            #     print(f"Skipping {company_name} because it is a consulting company.")
            #     continue
            # Format the directory name: lowercase, replace spaces with underscores
            formatted_company_name = company_name.lower().replace(" ", "_")
            company_folder = os.path.join(root_directory, formatted_company_name)
            
            # Create a folder for the company if it doesn't exist
            os.makedirs(company_folder, exist_ok=True)
            
            # Define the path for the mini dossier file
            mini_dossier_path = os.path.join(company_folder, "mini_dossier.txt")
            
            # Check if the mini dossier already exists
            if not os.path.exists(mini_dossier_path):
                # Generate the mini dossier for this company
                raw_data = scrape_data(url)
                formatted_data = format_data(raw_data)
                save_formatted_data(formatted_data, formatted_company_name)
            else:
                print(f"Mini dossier already exists for {company_name}, skipping generation.")

def main():
    while True:
        # User input to choose an action
        user_input = input("Enter 'run' to generate documents or 'quit' to exit the program: ").lower().strip()
        
        if user_input == "run":
            # List CSV files in the root directory
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            if not csv_files:
                print("No CSV files found in the directory.")
                continue
            
            # Display CSV files to the user
            print("Available CSV files:")
            for idx, file in enumerate(csv_files, 1):
                print(f"{idx}. {file}")
            
            # Ask the user to select a CSV file
            csv_file_index = input("Enter the number of the CSV file you want to use: ")
            try:
                selected_csv_file = csv_files[int(csv_file_index) - 1]
            except (IndexError, ValueError):
                print("Invalid selection, please enter a valid number.")
                continue

            print(f"Starting document generation using {selected_csv_file}...")
            asyncio.run(generate_docs(selected_csv_file))
            print("Document generation completed.")

        elif user_input == "quit":
            # Exit the program
            print("Exiting the program.")
            break
        else:
            # Handle unexpected input
            print("Invalid input. Please enter 'run' or 'quit'.")


if __name__ == "__main__":
    main()