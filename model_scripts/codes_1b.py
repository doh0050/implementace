from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

cache_dir = '../models/codes-1b'

tokenizer = AutoTokenizer.from_pretrained('seeklhy/codes-1b', cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained('seeklhy/codes-1b', torch_dtype=torch.float16, cache_dir=cache_dir)
#model = AutoModelForCausalLM.from_pretrained('seeklhy/codes-1b', torch_dtype=torch.float32, cache_dir=cache_dir)

model = model.to("cuda")###
model.eval()

# update eos token id of the tokenizer and the model to support early stop SQL generation
token_ids_of_example_sql = tokenizer("SELECT * FROM table ;")["input_ids"]
#print(token_ids_of_example_sql)
if token_ids_of_example_sql[-1] == tokenizer.eos_token_id:
    new_eos_token_id = token_ids_of_example_sql[-2]
else:
    new_eos_token_id = token_ids_of_example_sql[-1]
model.config.eos_token_id = new_eos_token_id
tokenizer.eos_token_id = new_eos_token_id
    # print("new_eos_token_id:", new_eos_token_id)
    # print("tokenizer.decode(new_eos_token_id): '{}'".format(tokenizer.decode(new_eos_token_id)))
max_tokens = 8192
max_new_tokens = 256





def prepare_input_ids_and_attention_mask(tokenizer, input_seq, max_input_length, device):
    input_ids = tokenizer(input_seq , truncation = False)["input_ids"]

    if len(input_ids) <= max_input_length:
        input_ids = input_ids
        attention_mask = [1] * len(input_ids)
    else:
        if tokenizer.name_or_path == "THUDM/codegeex2-6b":
            input_ids = [64790, 64792] + input_ids[-(max_input_length-2):]
        else:
            input_ids = [tokenizer.bos_token_id] + input_ids[-(max_input_length-1):]

        attention_mask = [1] * max_input_length

    #print("len(input_ids):", len(input_ids))

    return {
        "input_ids": torch.tensor([input_ids]).to(device), # torch.int64
        "attention_mask": torch.tensor([attention_mask]).to(device) # torch.int64
    }

def text2sql_func(model, text2sql_input_seq, tokenizer, max_tokens, max_new_tokens):
    inputs = prepare_input_ids_and_attention_mask(
        tokenizer,
        text2sql_input_seq,
        max_tokens - max_new_tokens,
        model.device
    )

    input_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        generate_ids = model.generate(
            **inputs,
            max_new_tokens = max_new_tokens,
            num_beams = 4,
            num_return_sequences = 4,
            use_cache = True
        )

    generated_sqls = tokenizer.batch_decode(generate_ids[:, input_length:], skip_special_tokens = True, clean_up_tokenization_spaces = False)

    return generated_sqls


def answer_my_question(input_seq):
    an = text2sql_func(model, input_seq, tokenizer, max_tokens, max_new_tokens)
    text=an[0]

    #ořez
    position = text.find("answer this")
    #position = text.find("QUERY")

    # Pokud bylo slovo "QUERY" nalezeno, ořízněte text před ním
    if position != -1:
        return text[:position]
    else:
        return text  # Pokud slovo "QUERY" není nalezeno, zachovejte původní text
    




