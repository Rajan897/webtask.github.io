import PyPDF2
import json

def add_pdf_content_to_json(pdf_file_path, existing_json_path, output_json_path):
    # Open and load the existing JSON file
    with open(existing_json_path, 'r') as existing_json_file:
        existing_data = json.load(existing_json_file)

    # Open the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize a list to store formatted data
        formatted_data = []

        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the text content of the page
            page = pdf_reader.pages[page_num]
            page_content = page.extract_text()

            # Split the content into lines
            lines = [line.strip() for line in page_content.split('\n') if line.strip()]

            # Process lines and extract tags, patterns, and responses
            for line in lines:
                if line.startswith("Tag:"):
                    tag = line.split(":")[1].strip()
                    patterns = []
                    responses = []

                    # Extract patterns and responses
                    while True:
                        line = lines.pop(0).strip()
                        if line.startswith("Pattern:"):
                            patterns.append(line.split(":")[1].strip())
                        elif line.startswith("Response:"):
                            responses.append(line.split(":")[1].strip())
                        elif not line:
                            break

                    # Append the formatted data to the list
                    formatted_data.append({
                        'tag': tag,
                        'patterns': patterns,
                        'responses': responses
                    })

    # Check if 'formatted_data' key already exists in the existing JSON
    if 'formatted_data' in existing_data:
        # Append the new data to the existing list
        existing_data['formatted_data'].extend(formatted_data)
    else:
        # Create 'formatted_data' key if it doesn't exist
        existing_data['formatted_data'] = formatted_data

    # Write the updated JSON data to a new file
    with open(output_json_path, 'w') as output_json_file:
        json.dump(existing_data, output_json_file, indent=4)

if __name__ == "__main__":
    # Provide the path to your PDF file, existing JSON file, and the output JSON file
    pdf_file_path =  pdf_file_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\azure-ai-services-luis.pdf'
    existing_json_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\intents.json'
    output_json_path = r'C:\Users\gaurasingh\Desktop\Guarav\chatbot-deployment-main gaurav\chatbot-deployment-main123\intents.json'
    
    # Call the function to add PDF content to the existing JSON
    add_pdf_content_to_json(pdf_file_path, existing_json_path, output_json_path)

    print(f"Formatted data from PDF added to the existing JSON. Updated JSON saved at: {output_json_path}")
