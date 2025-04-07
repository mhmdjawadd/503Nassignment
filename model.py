from transformers import pipeline
# Initialize the model
fill_mask_model = pipeline('fill-mask', model='bert-base-uncased')

