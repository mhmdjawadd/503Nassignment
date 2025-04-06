from transformers import pipeline

fill_mask = pipeline('fill-mask', model = 'bert-base-uncased')

#takes sentence w/ [MASK] token & returns completed sentence
#argument: sentence (str) = takes input sentence including the [MASK] token
#returns: str = sentence / [MASK] replaced by the model's top (best) prediction

def autocomplete_sentence(sentence: str) -> str: 
    if "[MASK]" not in sentence:
        raise ValueError("The input sentence must contain a [MASK] token!")

    try:
        predictions = fill_mask(sentence)
        if predictions:
            top_prediction = predictions[0]['token_str'].strip()
            complete_sentence = sentence.replace("[MASK]", top_prediction, 1)
            return complete_sentence
        else:
            return "Prediction can't be generated."
        
    except Exception as e:
        return str(e)


