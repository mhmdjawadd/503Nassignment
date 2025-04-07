# Flask API for Sentence Generation, Reconstruction, and Autocompletion

This repo contains a Flask API with 3 main functionalities pertaining to sentence manipulation using the Hugging Face transformers fill-mask model:
- **Sentence reconstruction**: reconstructing a sentence by masking one word at a time and predicting each one
- **Sentence generation**: generating sentences by predicting & replacing masked words
- **Sentence autocompletion**: ‘autocompleting’ a sentence with missing words that are denoted by [MASK]

## Setup

### Prerequisites
- Python 3.7 or above
- pip

### Install dependencies
1. Clone repo:
 ```
 bash git clone https://github.com/mhmdjawadd/503Nassignment
 cd 503Nassignment
 ```
2. Create & activate a virtual environment (recommended):
 ```
 python -m venv venv
 venv\Scripts\activate # on Windows
 ```
3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage
1. Run the Flask app locally:
```
python app.py
```
The server will start at ```http://127.0.0.1:5000/```

### For sentence reconstruction ```/reconstruct ```
- Method: POST
- Request:
```
{
"sentence": "The quick brown [MASK] jumps over the lazy dog."
}
```
- Response:
```
{
"original": "The quick brown [MASK] jumps over the lazy dog.",
"reconstructed": "The quick brown fox jumps over the lazy dog."
}
```

### For sentence generation ```/generate ```
- Method: GET
- Request: query parameters k (# of sentences) and length (# of words in each sentence)
```
/generate?k=2&length=9
```
- Response:
```
{
  "sentences": [
      "The quick brown fox jumped over the lazy dog.",
      "The cat and dog slept under the tree shadow."
  ]
}
```
### For sentence autocompletion ```/autocomplete ```
- Method: POST
- Request: 
```
{
  "sentence": "The quick brown [MASK] jumps over the lazy dog."
}
```
- Response:
```
{
  "original": "The quick brown [MASK] jumps over the lazy dog.",
  "completed": "The quick brown fox jumps over the lazy dog."
}
```
## Testing with curl
1. For /reconstruct:
```
curl -X POST http://127.0.0.1:5000/reconstruct -H "Content-Type: application/json" -d '{"sentence": "The quick brown [MASK] jumps over the lazy dog."}'
```
3. For /generate:
```
curl "http://127.0.0.1:5000/generate?k=5&length=10"
```
5. For /autocomplete:
```
curl -X POST http://127.0.0.1:5000/autocomplete -H "Content-Type: application/json" -d '{"sentence": "The quick brown [MASK] jumps over the lazy dog."}'
```
  

