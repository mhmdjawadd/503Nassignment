from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
from reconstruct import reconstruct_sentence_with_model

app = Flask(__name__)

# Initialize the model
fill_mask_model = pipeline('fill-mask', model='bert-base-uncased')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/reconstruct', methods=['POST'])
def reconstruct():
    data = request.get_json()
    sentence = data.get('sentence', '')
    
    if not sentence:
        return jsonify({'error': 'No sentence provided'}), 400
    
    try:
        reconstructed = reconstruct_sentence_with_model(sentence, fill_mask_model)
        return jsonify({'original': sentence, 'reconstructed': reconstructed})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create the template file if it doesn't exist
template_path = os.path.join('templates', 'index.html')
if not os.path.exists(template_path):
    with open(template_path, 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Sentence Reconstructor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; padding: 8px; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        #result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Sentence Reconstructor</h1>
    <p>Enter a sentence below and the model will reconstruct it word by word.</p>
    
    <textarea id="sentence" placeholder="Enter a sentence..."></textarea>
    <button onclick="reconstructSentence()">Reconstruct</button>
    
    <div id="result" style="display: none;">
        <h3>Results:</h3>
        <p><strong>Original:</strong> <span id="original"></span></p>
        <p><strong>Reconstructed:</strong> <span id="reconstructed"></span></p>
    </div>

    <script>
        function reconstructSentence() {
            const sentence = document.getElementById('sentence').value;
            if (!sentence) {
                alert('Please enter a sentence');
                return;
            }
            
            fetch('/reconstruct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sentence: sentence }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }
                
                document.getElementById('original').textContent = data.original;
                document.getElementById('reconstructed').textContent = data.reconstructed;
                document.getElementById('result').style.display = 'block';
            })
            .catch(error => {
                alert('Error: ' + error);
            });
        }
    </script>
</body>
</html>
        ''')

if __name__ == '__main__':
    app.run(debug=True)
