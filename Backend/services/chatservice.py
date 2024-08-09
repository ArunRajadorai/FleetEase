import requests
from ..config.ChatConfig import SEND_BIRD_API_TOKEN, SEND_BIRD_API_URL


class ChatService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SEND_BIRD_API_TOKEN}",
            "Content-Type": "application/json"
        }

    def create_channel(self, name: str, user_ids: list):
        url = f"{SEND_BIRD_API_URL}/group_channels"
        payload = {
            "name": name,
            "user_ids": user_ids
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def send_message(self, channel_url: str, message: str):
        url = f"{SEND_BIRD_API_URL}/group_channels/{channel_url}/messages"
        payload = {
            "message": message
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_channels(self):
        url = f"{SEND_BIRD_API_URL}/group_channels"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
