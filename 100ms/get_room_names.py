import pandas as pd
import requests

# Replace with your actual file path
file_path = 'sessions.csv'

# Replace with your actual management token
management_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDY2NjEwMzEsImV4cCI6MTcwNjc0NzQzMSwianRpIjoiand0X25vbmNlIiwidHlwZSI6Im1hbmFnZW1lbnQiLCJ2ZXJzaW9uIjoyLCJuYmYiOjE3MDY2NjEwMzEsImFjY2Vzc19rZXkiOiI2NGMxYWJhYTkxYzAyM2I0ZTJkNzZlODQifQ.lnoIisp7IPmbERjCQkn6KsHF3QAdpB9d8Ivyra3yjls'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Function to make API call and return name
def get_room_name(room_id, token):
    url = f'https://api.100ms.live/v2/rooms/{room_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('name', None)
    else:
        return None

df['game_id'] = df['room_id'].apply(lambda x: get_room_name(x, management_token))
df = df.loc[:, ['session_id', 'room_id', 'game_id']]

df.to_csv('session_room_game.csv', index=False)