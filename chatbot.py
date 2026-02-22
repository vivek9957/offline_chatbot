import json
import re
from fuzzywuzzy import fuzz
from pypdf import PdfReader

# This function compares user input with known phrases
# using fuzzy string matching and returns the closest match.

# load responses
def load_responses(file="responses.json"):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: responses.json file not found.")
        return {}

# extract text from pdf
def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# search answer from PDF text
def search_pdf_answer(user_input, pdf_text):
    user_input = user_input.lower()

    sentences = pdf_text.split("\n")

    best_match = ""
    best_score = 0

    for sentence in sentences:
        score = fuzz.ratio(user_input, sentence.lower())

        if score > best_score:
            best_score = score
            best_match = sentence

    if best_score > 50:
        return best_match

    return None

# clean text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# find response
def get_response(user_input, responses):
    best_match = None
    best_score = 0

    for key in responses:
        score = fuzz.ratio(user_input, key)

        if score > best_score:
            best_score = score
            best_match = key

    if best_score > 60:
        return responses[best_match]
    else:
        return "Sorry, I don't understand."

# chat loop
def chatbot():
    responses = load_responses()

    # load PDF text once
    pdf_text = extract_pdf_text("company_policy.pdf")

    print("Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").lower()

        if not user_input.strip():
            print("Bot: Please enter something.")
            continue

        if user_input == "exit":
            print("Bot: Goodbye!")
            break

        user_input = preprocess(user_input)
        #check the pdf first
        pdf_reply = search_pdf_answer(user_input, pdf_text)

if pdf_reply:
    print("Bot:", pdf_reply)
else:
    reply = get_response(user_input, responses)
    print("Bot:", reply)

# run chatbot
if __name__ == "__main__":
    chatbot()
