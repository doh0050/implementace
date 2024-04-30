import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

cache_dir = './../models/cx'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

model_path = 'tscholak/cxmefzzi'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, cache_dir=cache_dir).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=cache_dir)

#schema= db_create

def generate_sql(input_text):
    #input_text = " ".join(["Question: ", q, "Schema:", schema])

    model_inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**model_inputs, max_length=512)

    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    outsplit =output_text.split('|')
    if len(outsplit)==1:
        return outsplit[0]
    print(outsplit)
    return outsplit[1]

def answer_my_question(input_seq):
    return generate_sql(input_seq)
