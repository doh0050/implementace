from transformers import GPT2LMHeadModel, GPT2Tokenizer


cache_dir = '../models/gpt2_medium'
finetunedGPT = GPT2LMHeadModel.from_pretrained("rakeshkiriyath/gpt2Medium_text_to_sql", cache_dir=cache_dir)
finetunedTokenizer = GPT2Tokenizer.from_pretrained("rakeshkiriyath/gpt2Medium_text_to_sql", cache_dir=cache_dir)
finetunedGPT.to('cuda')

def generate_text_to_sql(query, model, tokenizer, max_length=256):
    max_length = 400
    prompt = f"Translate the following English question to SQL: {query}"

    input_tensor = tokenizer.encode(prompt, return_tensors='pt').to('cuda')

    output = model.generate(input_tensor, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

    sql_output = decoded_output[len(prompt):].strip()

    return sql_output

def answer_my_question(input_seq):
    return generate_text_to_sql(input_seq, finetunedGPT, finetunedTokenizer)
