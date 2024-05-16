import pandas as pd
import json


csv_file_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\name.csv'


df = pd.read_csv(csv_file_path)

json_data_list = []
for index, row in df.iterrows():
    json_data_list.append({
        "tag": row.get('tag'),
        "patterns": [pattern.strip() for pattern in str(row.get('patterns', '')).split(',')],
        "responses": [response.strip() for response in str(row.get('responses', '')).split(',')]
    })


existing_json_file_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\intents.json'


try:
    with open(existing_json_file_path, 'r') as existing_json_file:
        existing_data = json.load(existing_json_file)
except FileNotFoundError:
    
    existing_data = {}

existing_data['intents'] = existing_data.get('intents', []) + json_data_list


json_file_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\intents.json'



with open(json_file_path, 'w') as json_file:
    json.dump(existing_data, json_file, indent=2)

print(f'Update successful. JSON file updated at {json_file_path}')
