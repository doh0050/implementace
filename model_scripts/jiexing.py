import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

cdir='./../models/jiexing/'
model_path = 'Jiexing/spider_relation_t5_3b-2624'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

model = AutoModelForSeq2SeqLM.from_pretrained(model_path, cache_dir=cdir).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=cdir)

#schema= db_create

def generate_sql(input_text):
    #input_text = " ".join(["Question: ", q, "Schema:", schema])

    model_inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**model_inputs, max_length=512)

    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return output_text

def answer_my_question(input_seq):
    out =generate_sql(input_seq)
    outsplit=out.split('|')
    if len(outsplit) ==1:
        return outsplit[0] 
    return outsplit[1]
