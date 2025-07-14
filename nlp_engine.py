# nlp_engine.py

import json
import spacy
from risk_scorer import calculate_risk_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

# Initialize the VADER sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()


def classify_threat(text: str) -> str:
    """
    Classifies a threat based on keywords in the text.
    This is our rule-based classification logic.
    """
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ["protest", "activist", "blockade", "peta"]):
        return "Activism / Physical Security"
    elif any(keyword in text_lower for keyword in ["tariff", "government", "diplomatic", "trade", "policy"]):
        return "Geopolitical / Market Risk"
    elif any(keyword in text_lower for keyword in ["arbitration", "charge", "financial", "investor"]):
        return "Legal / Financial"
    else:
        return "General Intelligence"


def extract_entities(text: str) -> dict:
    """
    Extracts named entities from text using spaCy.
    Recognizes organizations, locations, etc.
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text)
    # Remove duplicate entities
    for label in entities:
        entities[label] = list(set(entities[label]))
    return entities


def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of a text using VADER.
    Returns a dictionary with positive, negative, neutral, and compound scores.
    """
    return sentiment_analyzer.polarity_scores(text)


def analyze_events_from_file(filepath: str = 'events.json') -> list:
    """
    Main function to load events from a JSON file and run full analysis on each.
    CORRECTED LOGIC FLOW.
    """
    try:
        with open(filepath, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []

    analyzed_results = []
    for event in events:
        details = event.get("details", "")

        # --- CORRECTED ORDER OF OPERATIONS ---

        # 1. First, perform the basic NLP analysis
        threat_type = classify_threat(details)
        entities = extract_entities(details)
        sentiment = analyze_sentiment(details)

        # 2. NOW, call the risk scorer and PASS the threat_type to it
        risk_assessment = calculate_risk_score(event, threat_type)

        # 3. Finally, assemble the complete analysis object
        event['analysis'] = {
            'classified_threat': threat_type,
            'extracted_entities': entities,
            'sentiment_scores': sentiment,
            'risk_assessment': risk_assessment
        }
        analyzed_results.append(event)

    return analyzed_results


# This block allows us to test the engine by running this file directly
if __name__ == "__main__":
    print("🔬 Running NLP Analysis Engine on 'events.json'...")

    # Run the main analysis function
    final_analysis = analyze_events_from_file()

    if final_analysis:
        print("\n✅ Analysis Complete. Results:")
        print("=" * 40)
        # Pretty-print the results
        # Pretty-print the results
        for event in final_analysis:
            print(f"\n📄 Event Title: {event['title']}")
            print(f"   📍 Location: {event['location']}")
            print("-" * 20)
            analysis = event['analysis']
            risk = analysis['risk_assessment']  # Get the risk data
            print(f"   Threat Classified As: {analysis['classified_threat']}")
            # Print the new risk information
            print(
                f"   >> Risk Score: {risk['risk_score']} (Likelihood: {risk['likelihood']}/5, Impact: {risk['impact']}/5)")
            print(f"   >> Primary Impact: {risk['primary_impact']}")

            print(f"   Sentiment (Compound Score): {analysis['sentiment_scores']['compound']:.2f}")
            print("   Extracted Entities:")
            if analysis['extracted_entities']:
                for label, ents in analysis['extracted_entities'].items():
                    print(f"     - {label}: {', '.join(ents)}")
            else:
                print("     - None Found")