
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

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/insights', methods=['GET'])
def get_insights():
    data = load_data()
    return jsonify(data.get('insights', []))

@app.route('/insights', methods=['POST'])
def add_insight():
    new_insight = request.json
    data = load_data()
    data['insights'].append(new_insight)
    save_data(data)
    return jsonify({"message": "Insight added successfully!"}), 201

@app.route('/insights/<insight_id>', methods=['DELETE'])
def delete_insight(insight_id):
    data = load_data()
    original_len = len(data['insights'])
    data['insights'] = [i for i in data['insights'] if i.get('id') != insight_id]
    if len(data['insights']) < original_len:
        save_data(data)
        return jsonify({"message": "Insight deleted successfully!"})
    else:
        return jsonify({"message": "Insight not found."}), 404

@app.route('/patterns', methods=['GET'])
def get_patterns():
    data = load_data()
    insights = data.get('insights', [])

    if not insights:
        return jsonify({"message": "No insights data available."})

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

    emerging_threshold = 5
    high_value_threshold = 3
    neglected_threshold = 0

    patterns_report = {
        "emerging_topics": [topic for topic, count in relevance_counter.items() if count >= emerging_threshold],
        "high_value_topics": [topic for topic, count in high_value_counter.items() if count >= high_value_threshold],
        "neglected_topics": [topic for topic, count in relevance_counter.items() if count <= neglected_threshold]
    }

    return jsonify(patterns_report)



@app.route('/dashboard/summary', methods=['GET'])
def dashboard_summary():
    data = load_data()
    insights = data.get('insights', [])
    summary = {
        "total_insights": len(insights),
        "new_insights": sum(1 for i in insights if i.get('readiness') == 'New'),
        "high_confidence": sum(1 for i in insights if i.get('confidence') == 'High'),
        "pending_actions": sum(1 for i in insights if i.get('readiness') == 'New' and i.get('significance') == '5')
    }
    return jsonify(summary)


@app.route('/dashboard/metrics', methods=['GET'])
def dashboard_metrics():
    data = load_data()
    insights = data.get('insights', [])
    from collections import Counter
    relevance_counter = Counter(i.get('relevance_to', 'Unknown') for i in insights)
    confidence_counter = Counter(i.get('confidence', 'Unknown') for i in insights)
    readiness_counter = Counter(i.get('readiness', 'Unknown') for i in insights)

    metrics = {
        "topics_distribution": dict(relevance_counter),
        "confidence_distribution": dict(confidence_counter),
        "readiness_distribution": dict(readiness_counter)
    }
    return jsonify(metrics)


@app.route('/dashboard/alerts', methods=['GET'])
def dashboard_alerts():
    data = load_data()
    insights = data.get('insights', [])
    alerts = []
    for insight in insights:
        if insight.get('readiness') == 'New' and insight.get('significance') == '5':
            alerts.append(f"High-importance new insight: {insight.get('summary')}")
    if not alerts:
        alerts.append("No critical alerts at the moment.")
    return jsonify({"alerts": alerts})


@app.route('/critique', methods=['POST'])
def critique_text():
    data = request.get_json()
    text = data.get('text', '')
    critique = []
    improved_text = text

    if len(text.split()) < 10:
        critique.append("הניסוח קצר מדי, כדאי להרחיב ולהוסיף דוגמאות או הסבר מפורט יותר.")
    if not any(word in text.lower() for word in ["מומלץ", "כדאי", "אפשר", "נסה", "נסי"]):
        critique.append("אין קריאה ברורה לפעולה, הוסיפי הצעת פעולה ישירה.")
    if "לדוגמה" not in text and "כגון" not in text:
        critique.append("חסרה דוגמה מעשית להמחשה.")

    if critique:
        improved_text = text + " (הוסיפי דוגמה והנחיות פעולה ישירות)."

    return jsonify({
        "critique": critique,
        "improved_text": improved_text
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
