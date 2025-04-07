import random
from .model import fill_mask_model as fill_mask

def generate_k_sentences(k: int, length: int):
    
    # Your text
    text = """The quick brown fox jumps over the lazy dog. The quick brown fox is quick and smart. Dogs are lazy but loyal. Foxes are clever, fast, and curious. The dog barked, the fox ran. The sky was blue, the grass was green, and the sun was shining. Everyone loved the peaceful day. Birds chirped. Leaves rustled. The wind blew softly. Children played outside. The cat slept. The rabbit hopped. The flowers bloomed. The bees buzzed. The world felt calm. The quick brown fox watched from a hill. The lazy dog slept under a tree. Clouds passed by. Time moved slowly. It was a good day. It was a simple day. It was a quiet day. It was a lovely day. Over and over, the fox ran and the dog napped. Harmony filled the land. Nothing was urgent. Nothing was wrong. Just a moment of peace, lasting long. The quick brown fox, the lazy dog, the calm wind — all in sync, all in stillness."""

    words = [word.lower().strip('.,!?;:"') for word in text.split() if word.strip()]
    word_set = list(set([w for w in words if w.isalpha() and len(w) > 2]))  # Clean unique words

    def generate_clean_sentence(length=10):
        """Generates clean sentences with real words only"""
        # Start with a random word from our cleaned set
        sentence = [random.choice(word_set)]
        
        while len(sentence) < length:
            input_sentence = " ".join(sentence + ["[MASK]"])
            
            try:
                predictions = fill_mask(input_sentence)
                if predictions:
                    # Filter to keep only proper words
                    valid_predictions = [
                        p for p in predictions 
                        if (p['token_str'].strip().isalpha() and  # letters only
                            len(p['token_str'].strip()) > 2 and  # minimum length
                            p['token_str'].strip().lower() == p['token_str'].strip()  # no proper nouns
                        )
                    ]
                    
                    if valid_predictions:
                        chosen = random.choice(valid_predictions)
                        sentence.append(chosen['token_str'].strip())
                    else:
                        # Fallback to random word from our set
                        sentence.append(random.choice(word_set))
                else:
                    sentence.append(random.choice(word_set))
            except:
                sentence.append(random.choice(word_set))
        
        # Final cleanup
        clean_sentence = " ".join(sentence).capitalize()
        clean_sentence = clean_sentence.replace(" ' ", "'")  # Fix contractions
        return clean_sentence + "."

    # Generate clean examples
    results = []
    for _ in range(k):
        results.append(generate_clean_sentence(length))
    return results

print(generate_k_sentences(5, 5))