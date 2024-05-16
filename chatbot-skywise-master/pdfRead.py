import PyPDF2
import json
import re

def pdf_to_json(pdf_path, json_path):
    try:
      
        with open(pdf_path, 'rb') as file:
            
            pdf_reader = PyPDF2.PdfReader(file)

            
            intents = []

            
            for page_num in range(len(pdf_reader.pages)):
                
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                
                matches = re.findall(r'"tag": "(.*?)",\s*"patterns": \[(.*?)\],\s*"responses": \[(.*?)\]', text)
                for match in matches:
                    tag, patterns, responses = match
                    patterns_list = [p.strip('"') for p in patterns.split(',')]
                    responses_list = [r.strip('"') for r in responses.split(',')]
                    intent = {"tag": tag, "patterns": patterns_list, "responses": responses_list}
                    intents.append(intent)

          
            existing_data = {}
            try:
                with open(json_path, 'r') as existing_file:
                    existing_data = json.load(existing_file)
            except FileNotFoundError:
                pass 

            existing_data.setdefault('intents', []).extend(intents)
            with open(json_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=2)
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'.")

if __name__ == "__main__":
   
        pdf_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\azure-ai-services-luis.pdf'
        json_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\intents.json'
        pdf_to_json(pdf_path, json_path)
        

        