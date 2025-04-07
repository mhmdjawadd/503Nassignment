from ..model import fill_mask_model as fill_mask


def autocomplete_sentence(sentence: str) -> str: 
    
    """takes sentence w/ [MASK] token & returns completed sentence
    argument: sentence (str) = takes input sentence including the [MASK] token
    returns: str = sentence / [MASK] replaced by the model's top (best) prediction"""

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


