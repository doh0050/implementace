import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration


cache_dir = './../models/t5_small'
tokenizer = T5Tokenizer.from_pretrained('t5-small', cache_dir=cache_dir)
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql', cache_dir=cache_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

def generate_sql(input_prompt):
    # Tokenize the input prompt
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    
    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

def answer_my_question(input_seq):
    return generate_sql(input_seq)
