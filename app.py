
from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
from reconstruct import reconstruct_sentence_with_model
from generate import generate_k_sentences  # Import the sentence generation function
from autocomplete import autocomplete_sentence

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

@app.route('/generate', methods=['GET'])
def generate():
    # Get parameters from request, with defaults
    k = request.args.get('k', default=5, type=int)
    length = request.args.get('length', default=5, type=int)
    
    # Validate parameters
    if k <= 0 or length <= 0:
        return jsonify({'error': 'Parameters k and length must be positive integers'}), 400
    
    try:
        # Generate sentences
        sentences = generate_k_sentences(k, length)
        return jsonify({
            'sentences': sentences,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    data = request.get_json()
    sentence = data.get('sentence', '')

    if not sentence:
        return jsonify({'error': 'No sentence was provided'}), 400
    
    try:
        complete_sentence = autocomplete_sentence(sentence)
        return jsonify({'original': sentence, 'completed': complete_sentence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
           

if __name__ == '__main__':
    app.run(debug=True)