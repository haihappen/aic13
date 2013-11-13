import json
import requests


data = [{'answer':'positive', 'task': 1, 'user': 1},
        {'answer':'positive', 'task': 2, 'user': 1},
        {'answer':'neutral',  'task': 3, 'user': 1},
        {'answer':'positive', 'task': 4, 'user': 1},
        {'answer':'negative', 'task': 5, 'user': 1},
        {'answer':'negative', 'task': 6, 'user': 1},
        {'answer':'positive', 'task': 7, 'user': 1},
        {'answer':'positive', 'task': 8, 'user': 1},
        {'answer':'positive', 'task': 9, 'user': 1},

        {'answer':'negative', 'task': 11, 'user': 1},
        {'answer':'negative', 'task': 12, 'user': 1},
        {'answer':'positive', 'task': 13, 'user': 1},
        {'answer':'positive', 'task': 14, 'user': 1},
        {'answer':'positive', 'task': 15, 'user': 1},

        {'answer':'neutral', 'task': 16, 'user': 1},
        {'answer':'neutral', 'task': 17, 'user': 1},
        {'answer':'neutral', 'task': 18, 'user': 1},
        ]

    
data_json = json.dumps(data)

r = requests.post('http://127.0.0.1:8001/callback/', data=data_json)
