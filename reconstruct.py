def reconstruct_sentence_with_model(sentence: str, fill_mask_model) -> str:
    """
    Reconstructs a sentence by masking one word at a time (alternating odd/even indices),
    getting the model's prediction, and updating the sentence immediately.
    
    Args:
        sentence: Input sentence to process
        fill_mask_model: A fill-mask model that predicts a single [MASK] token
    
    Returns:
        Reconstructed sentence using model predictions
    """
    words = sentence.split()
    words.append('.')
    # First pass: predict odd-indexed words (1, 3, 5...)
    for i in range(1, len(words), 2):
        # Mask the current word
        masked_sentence = words.copy()
        masked_sentence[i] = "[MASK]"
        masked_sentence = " ".join(masked_sentence)
        
        # Get model prediction (assuming it returns a list of candidates)
        predictions = fill_mask_model(masked_sentence)
        
        # Update with the top prediction (adjust based on model output format)
        if predictions and len(predictions) > 0:
            top_prediction = predictions[0]['token_str']  # HuggingFace format
            words[i] = top_prediction
    
    # Second pass: predict even-indexed words (0, 2, 4...)
    for i in range(0, len(words), 2):
        # Mask the current word
        masked_sentence = words.copy()
        masked_sentence[i] = "[MASK]"
        masked_sentence = " ".join(masked_sentence)
        
        # Get model prediction
        predictions = fill_mask_model(masked_sentence)
        
        # Update with the top prediction
        if predictions and len(predictions) > 0:
            top_prediction = predictions[0]['token_str']
            words[i] = top_prediction
    
    return " ".join(words)


