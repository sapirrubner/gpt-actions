
from flask import Flask, request, jsonify
import json
import os
from collections import Counter

app = Flask(__name__)

DATA_FILE = 'Insights_Sample.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"insights": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/patterns', methods=['GET'])
def get_patterns():
    data = load_data()
    insights = data.get('insights', [])

    if not insights:
        return jsonify({"message": "No insights data available."})

    # Analyze patterns based on relevance_to, significance, confidence, readiness
    relevance_counter = Counter()
    high_value_counter = Counter()
    new_readiness_counter = Counter()

    for insight in insights:
        relevance = insight.get('relevance_to', 'Unknown')
        significance = insight.get('significance', '0')
        confidence = insight.get('confidence', 'Low')
        readiness = insight.get('readiness', 'New')

        relevance_counter[relevance] += 1
        if significance == '5' and confidence == 'High':
            high_value_counter[relevance] += 1
        if readiness == 'New':
            new_readiness_counter[relevance] += 1

    # Define thresholds for pattern detection
    emerging_threshold = 5
    high_value_threshold = 3
    neglected_threshold = 0

    patterns_report = {
        "emerging_topics": [topic for topic, count in relevance_counter.items() if count >= emerging_threshold],
        "high_value_topics": [topic for topic, count in high_value_counter.items() if count >= high_value_threshold],
        "neglected_topics": [topic for topic, count in relevance_counter.items() if count <= neglected_threshold]
    }

    return jsonify(patterns_report)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
