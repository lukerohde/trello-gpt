import os
import openai
import requests
import ipdb

# Define the API endpoint
endpoint = "https://api.trello.com/1"
trello_api_key = os.getenv("TRELLO_API_KEY")
trello_token = os.getenv("TRELLO_TOKEN")

# Get all boards
url = f"{endpoint}/members/me/boards?key={trello_api_key}&token={trello_token}"
r = requests.get(url)


jobs = ""
if r.status_code == 200: 
    boards = r.json()
    for board in boards:
        if board['name'] == "Odd Jobs Altona":
            print(board["id"] + ": " + board["name"] + " - " + board["url"])
            url = f"{endpoint}/boards/{board['id']}/lists?key={trello_api_key}&token={trello_token}"
            r = requests.get(url)
            if r.status_code == 200: 
                lists = r.json()
                for list in lists: 
                    if "Brook" in list['name'] and not "Done" in list['name']:
                        print("  " + list["id"] + ": " + list["name"])
                        url=f"{endpoint}/lists/{list['id']}/cards?key={trello_api_key}&token={trello_token}"
                        r = requests.get(url)
                        if r.status_code == 200:
                            cards = r.json()
                            for card in cards: 
                                jobs += f"{list['name']} - {card['name']}\n"
                                print("    " + card["id"] + ": " + card["name"])



openai.api_key = os.getenv("OPENAI_API_KEY")
history = f"Assistant: These are your jobs\n{jobs}\n\nAssistant: What can I help with?\n"

while True:
    # Prompt user for input
    print(history)

    prompt = input("\n You (type 'q' to quit): ")
    if prompt.lower() == 'q':
        break

    history += "\n\nUSER: " + prompt
    # Make API request
    response = openai.Completion.create(model="text-davinci-003", prompt=history, temperature=0.5, max_tokens=250)
    print(response)

    answer = response["choices"][0]["text"]
    history += answer 
            


    
