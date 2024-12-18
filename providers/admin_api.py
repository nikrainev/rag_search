import json

import requests
from typing import Dict
from providers.config import get_config

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InJvbGVzIjpbIlRnQm90Il19LCJpYXQiOjE3MzQ0Njc3NzAsImV4cCI6Mzc3MzQ0Njc3NzB9.zqO0iyv_wJTHEVt6hEBlNhFlvh6GBKakqfxwd1VoXKc',
    'Content-Type': 'application/json'
}

def send_create_user(chat_id:int, username:str, is_premium_tg:bool):
    config = get_config()

    print(chat_id)
    print(username)
    print(is_premium_tg)
    try:
        requests.post(f"{config.get('admin_api_url')}/tg-bot/user", headers=headers, data=json.dumps({
            'chat_id': chat_id,
            'username': username,
            'is_premium_tg': is_premium_tg
        }))
    except:
        print("An exception occurred")
    return


def send_create_file(chat_id:int, name:str, mimeType:str, content:str):
    config = get_config()

    try:
        requests.post(f"{config.get('admin_api_url')}/tg-bot/user/{chat_id}/file", headers=headers, data=json.dumps({
            'name': name,
            'mimeType': mimeType,
            'content': content
        }))
    except:
        print("An exception occurred")
    return

def send_create_user_request(chat_id:int, requestText:str, responseText:str):
    config = get_config()
    try:
        requests.post(f"{config.get('admin_api_url')}/tg-bot/user/{chat_id}/user-request",  headers=headers, data=json.dumps({
            'requestText': requestText,
            'responseText': responseText
        }))
    except:
        print("An exception occurred")
    return

def check_rate_limit(chat_id:int) -> Dict:
    config = get_config()
    try:
        result = requests.get(f"{config.get('admin_api_url')}/tg-bot/user/{chat_id}/rate-limit",  headers=headers)

        data = result.json().get('data')

        print(data)
        return {
            'isAvailable': data.get('available'),
            'errorText': data.get('notAvailabilityReason')
        }
    except:
        print("An exception occurred")
        return {
            'isAvailable': True,
            'errorText': None
        }