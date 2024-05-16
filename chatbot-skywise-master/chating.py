import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataset = pd.read_csv('response.csv', header=None, names=['Response'])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(dataset['Response'])

def get_response(user_input):
    user_input_vectorized = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_input_vectorized, X)
    idx = similarities.argmax()
    response = dataset.loc[idx, 'Response']
    return response

print("Welcome! Ask me anything (type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    response = get_response(user_input)
    print("Chatbot:", response)