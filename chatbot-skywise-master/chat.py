import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

# Load dataset
dataset = pd.read_csv("response.csv", header=None, names=['Response'])

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Tokenization and lemmatization function
def tokenize_and_lemmatize(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Apply tokenization and lemmatization to dataset
dataset['Processed_Response'] = dataset['Response'].apply(tokenize_and_lemmatize)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(dataset['Processed_Response'])

# Function to handle team descriptions
def handle_team_description(team_name):
    if team_name.lower() == 'asgard':
        return "Asgard Team works on AWS and has 3 members"
    elif team_name.lower() == 'isard':
        return "Isard Team works on Python and has 4 members"
    elif team_name.lower() == 'snct':
        return "SNCT has 10 members and works on Foundry"
    else:
        return "I'm sorry, I don't have information about that team."

# Function to get response
def get_response(user_input):
    processed_input = tokenize_and_lemmatize(user_input)
    user_input_vectorized = vectorizer.transform([processed_input])
    similarities = cosine_similarity(user_input_vectorized, X)
    idx = similarities.argmax()
    response = dataset.loc[idx, 'Response']
    return response

# Function to handle fetching data from a hyperlink
def fetch_hyperlink_data(user_input):
    # Check if the user input contains a hyperlink
    if "http" in user_input:
        # Extract the hyperlink from the user input
        hyperlink = user_input.split()[-1]
        try:
            # Fetch data from the hyperlink
            response = requests.get(hyperlink)
            if response.status_code == 200:
                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract relevant data from the HTML
                # For demonstration purposes, let's just return the title of the webpage
                title = soup.title.string
                return f"Data retrieved from the provided link: {title}"
            else:
                return "Failed to fetch data from the provided link."
        except Exception as e:
            return f"An error occurred while fetching data from the provided link: {str(e)}"
    else:
        return "No hyperlink found in the input."

# Function to handle user input
def process_user_input(user_input):
    # Check if the user input contains a hyperlink
    if "http" in user_input:
        # Fetch data from the hyperlink
        response = fetch_hyperlink_data(user_input)
    else:
        # Get response based on user input
        response = get_response(user_input)
    return response
