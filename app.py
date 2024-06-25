from flask import Flask, request, jsonify, render_template
from pprint import pprint
import json
import os

app = Flask(__name__)

# Liste, um die empfangenen Daten zu speichern
received_data = []

@app.route('/delivery', methods=['POST'])
def handle_delivery():
    data = request.json
    print("Eingehende Daten:")
    pprint(data)
    
    # Speichere die empfangenen Daten in der Liste
    received_data.append(data)
    
    # Speichere die empfangenen Daten in einer JSON-Datei
    with open('eingehende_daten.json', 'w') as f:
        json.dump(received_data, f, indent=4)
    
    return jsonify({"status": "success"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    # Gebe die gespeicherten Daten als JSON zurück
    return jsonify(received_data)

@app.route('/')
def index():
    # Lade die HTML-Vorlage
    return render_template('template.html')

if __name__ == '__main__':
    # Erstelle die HTML-Vorlage, falls sie noch nicht existiert
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    with open('templates/template.html', 'w') as f:
        f.write('''<!doctype html>
<html>
<head>
    <title>Empfangene Daten</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow: auto;
        }
    </style>
</head>
<body>
    <h1>Empfangene Daten</h1>
    <pre id="json-data"></pre>

    <script>
        // Fetch the data from the server
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                // Format the JSON data for display
                document.getElementById('json-data').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => console.error('Error fetching data:', error));
    </script>
</body>
</html>''')
    
    # Starte den Flask-Server
    app.run(host='0.0.0.0', port=5000)
