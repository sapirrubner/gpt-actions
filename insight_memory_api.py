
from flask import Flask, request, jsonify
import json
import os

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
    insights = data.get('insights', [])

    # Apply filters
    confidence = request.args.get('confidence')
    significance = request.args.get('significance')
    readiness = request.args.get('readiness')
    relevance_to = request.args.get('relevance_to')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    filtered = insights
    if confidence:
        filtered = [i for i in filtered if i.get('confidence') == confidence]
    if significance:
        filtered = [i for i in filtered if i.get('significance') == significance]
    if readiness:
        filtered = [i for i in filtered if i.get('readiness') == readiness]
    if relevance_to:
        filtered = [i for i in filtered if i.get('relevance_to') == relevance_to]

    return jsonify(filtered[offset:offset + limit])

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
