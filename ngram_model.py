from bs4 import BeautifulSoup
import pickle

def extract_text(html):
    """ Extracts visible text from HTML content. """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ")

def predict(html_path):
    """ Predicts whether a given website HTML is defaced or safe. """
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    text = extract_text(html_content)
    
    # Load trained model
    with open("defacement_detector.pkl", "rb") as f:
        vectorizer, classifier = pickle.load(f)
    
    # Make prediction
    text_tfidf = vectorizer.transform([text])
    prediction = classifier.predict(text_tfidf)[0]
    # print the confidence
    confidence = classifier.predict_proba(text_tfidf)[0]
    label = "Defaced" if prediction == 1 else "Safe"
    print(f"Confidence: {confidence}")
    
    print(f"Prediction for {html_path}: {label}")
    return prediction == 0