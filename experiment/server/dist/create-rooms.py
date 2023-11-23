import requests
import json
import csv

base_url = 'https://api.100ms.live/v2/'
management_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTA5OTYxNjAsImV4cCI6MTY5MTA4MjU2MCwianRpIjoiand0X25vbmNlIiwidHlwZSI6Im1hbmFnZW1lbnQiLCJ2ZXJzaW9uIjoyLCJuYmYiOjE2OTA5OTYxNjAsImFjY2Vzc19rZXkiOiI2NGMxYWJhYTkxYzAyM2I0ZTJkNzZlODQifQ.JRrKMGwEOIQ_rUl9EM0Pl-zA4d7PhDRQBajqeVltWvs'
template_id = '64caab519847271c8b8359b3'
num_rooms = 10
rooms = {}
headers = {
    'Authorization': f'Bearer {management_token}',
    'Content-Type': 'application/json',
}

for i in range(1+5, num_rooms + 6):
    get_room = requests.post(
        base_url + 'rooms',
        data = json.dumps({
            'name': 'room' + str(i),
            'description': 'audio call room',
            'template_id': template_id,
            'region': 'us',
            'recording_info': {
            'enabled': True
            },
        }),
        headers = headers
    )

    room_id = json.loads(get_room.content)['id']
    get_code = requests.post(
        base_url + 'room-codes/room/' + room_id,
        data = {},
        headers = headers
    )
    room_code = json.loads(get_code.content)['data'][0]['code']
    rooms[room_code] = 'NULL'

with open('room-codes.csv', 'w') as f:
    writer = csv.writer(f)
    for code in rooms:
        writer.writerow([code, rooms[code]])