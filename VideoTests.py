import google.generativeai as genai
from openai import OpenAI
import anthropic
import ollama
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
#This TOT works good for bigger companies and solving problems but struggles with smaller companies like 7Rivers Inc.
# Imagine three different experts are answering this question.
# They will brainstorm the answer step by step reasoning carefully and taking all facts into consideration
# All experts will write down 1 step of their thinking,
# then share it with the group.
# They will each critique their response, and the all the responses of others
# They will check their answer based on accuracy and correctness. 
# Then all experts will go on to the next step and write down this step of their thinking.
# They will keep going through steps until they reach their conclusion taking into account the thoughts of the other experts
# If at any time they realize that there is a flaw in their logic they will backtrack to where that flaw occurred 
# If any expert realizes they're wrong at any point then they acknowledges this and start another train of thought
# Each expert will assign a likelihood of their current assertion being correct
# Continue until the experts agree on the single most likely location
# The question is you are a dossier creator, help me make a sales dossier sheet that has executive overview, products and services and the industries served and any other useful information for this company. The company is apple.


def google_response(company):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        system_instruction=f"You are an proffesional dossier creator. We will be using this dossier to gain info on this company and all insights within it. it is very important that this info is correct and accurate and none of it is made up. You will help me create a dossier for the the company {company}. The sections you are creating are the executive overview (Company name, URL, year founded, location, number of employees, revenue, CEO, Brief description and other relevant information), products and services (List of products and services offered by the company with a short description, and any other relevant information), and industries served (List of industries served by the company with a short description, and any other relevant information). Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served.")
    response = model.generate_content(f"Generate a dossier for the company {company}.")
    return response.text


def openai_response(company):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    system_message = f"You are an proffesional dossier creator. We will be using this dossier to gain info on this company and all insights within it. it is very important that this info is correct and accurate and none of it is made up. You will help me create a dossier for the the company {company}. The sections you are creating are the executive overview (Company name, URL, year founded, location, number of employees, revenue, CEO, Brief description and other relevant information), products and services (List of products and services offered by the company with a short description, and any other relevant information), and industries served (List of industries served by the company with a short description, and any other relevant information). Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served."

    user_message = f"Generate a dossier for the company {company}."

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
    return response.choices[0].message.content.strip()

def anthropic_response(company):
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-opus-20240229",
        system= f"You are an proffesional dossier creator. We will be using this dossier to gain info on this company and all insights within it. it is very important that this info is correct and accurate and none of it is made up. You will help me create a dossier for the the company {company}. The sections you are creating are the executive overview (Company name, URL, year founded, location, number of employees, revenue, CEO, Brief description and other relevant information), products and services (List of products and services offered by the company with a short description, and any other relevant information), and industries served (List of industries served by the company with a short description, and any other relevant information). Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served.",
        max_tokens=1000,
        messages=[
            {
                'role': 'user',
                'content': f'Generate a dossier for the company {company}.',
            },
        ]
    )
    return response.content[0].text
                    
def ollama_response(company): #phi3:mini #llama3:8b
    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {
                'role': 'system',
                'content': f"You are an proffesional dossier creator. We will be using this dossier to gain info on this company and all insights within it. it is very important that this info is correct and accurate and none of it is made up. You will help me create a dossier for the the company {company}. The sections you are creating are the executive overview (Company name, URL, year founded, location, number of employees, revenue, CEO, Brief description and other relevant information), products and services (List of products and services offered by the company with a short description, and any other relevant information), and industries served (List of industries served by the company with a short description, and any other relevant information). Format all this information in an organized way with the following headings: Executive Overview, Products & Services, Industries Served.",
            },
            {
                'role': 'user',
                'content': f"Generate a dossier for the company {company}.",
            },
        ]
    )
    return response['message']['content']

def save(data, timestamp, AIname, output_folder='doc'):
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'{AIname}_{timestamp}.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"{AIname}: \n{data}")

def main():
    while True:
        # User input to choose an action
        user_input = input("Enter 'run' to generate documents or 'quit' to exit the program: ").lower().strip()
        
        if user_input == "run":
            Company = input("Enter the company you want to learn about: ")
            try:
                timestamp = datetime.datetime.now().strftime('%H%M%S')
                save(google_response(Company), timestamp, 'Gemini')
                save(openai_response(Company), timestamp, 'OpenAI')
                save(ollama_response(Company), timestamp, 'Ollama')
                save(anthropic_response(Company), timestamp, 'Anthropic')  
            
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
