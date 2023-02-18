import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class Trello:

    def __init__(self, endpoint, api_key, token):
# Define the API endpoint
        self.endpoint = endpoint
        self.api_key = api_key
        self.token = token
        self.params = {"key": self.api_key, "token": self.token}
        self.current_board = None
        self.done_list_name = "Done"

    def get_board(self, target_board):
        try:
            # Get all boards
            url_boards = f"{self.endpoint}/members/me/boards"
            r = requests.get(url_boards, params=self.params)
            r.raise_for_status()
            logging.info('Request to Trello for board list successful')
            boards = r.json()
            jobs = ""
            for board in boards:
                if board['name'] == target_board:
                    logging.info("Board found: %s", target_board)
                    url_target_board = f"{self.endpoint}/boards/{board['id']}/lists"
                    r = requests.get(url_target_board, params=self.params)
                    r.raise_for_status()
                    lists = r.json()
                    for lst in lists: 
                        if not self.done_list_name in lst['name']:
                            url_list = f"{self.endpoint}/lists/{lst['id']}/cards"
                            r = requests.get(url_list, params=self.params)
                            r.raise_for_status()
                            cards = r.json()
                            for card in cards: 
                                jobs += f"{lst['name']} - {card['name']}\n"
                    break
            else:
                logging.warning("Board NOT found: %s", target_board)
        except requests.exceptions.RequestException as e:
            logging.error("Request to Trello failed: %s", e)
            jobs = ""
        return jobs
