import os
import csv
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
 
env_path = ".env"
load_dotenv(env_path)
 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


genai.configure()


model = genai.GenerativeModel("gemini-1.5-pro-latest")

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
            if publicly_traded.lower() == "yes" or publicly_traded.lower() == "n/a":
                print(f"Skipping {company_name} because it is publicly traded.")
                continue
            #skip companies that do not have a url
            if url.lower() == "n/a":
                print(f"Skipping {company_name} because it does not have url.")
                continue
            #Skip companies that are consulting companies
            if consulting.lower() == "yes":
                print(f"Skipping {company_name} because it is a consulting company.")
                continue
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
                await generate_mini_dossier(company_folder, company_name, url)
            else:
                print(f"Mini dossier already exists for {company_name}, skipping generation.")


def call_gemini(prompt):
    # Replace with your actual Gemini API key
    #genai.configure(GOOGLE_API_KEY)
    # Send the prompt to Gemini and store the response
    response = model.generate_content(prompt)
    return response


async def generate_mini_dossier(folder, company_name, url):
    print(f"Generating mini dossier for {company_name}")

    mini_dossier_company = (call_gemini(f"""You are a professional dossier creator. You create dossiers for specific companies to help the sales team. You are going to help me create a dossier for the company {company_name}. Here is the link to the website for this company: {url}. You do not need to only use the website to gather information, it is simply a reference to ensure that you are gathering data for the right company and not another company with the same name. It is very important that the information is accurate. The sections you are creating are the following: executive overview, products and services and industries served. 
    Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served.""")).text

    # Ensure the folder exists
    print(f"Creating folder {folder}")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"mini_dossier.txt")

    # Write the data to a file
    with open(file_path, "w") as file:
        file.write(mini_dossier_company)
    print(f"Data written to {file_path}")


def main():
    while True:
        # User input to choose an action
        print(GOOGLE_API_KEY)
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
            
            # Call the async function to generate documents using asyncio
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