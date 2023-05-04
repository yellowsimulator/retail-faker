from transformers import T5Tokenizer, T5ForConditionalGeneration
from models import t5_models


# load the fine-tuned model and use it to generate predictions/text
model = T5ForConditionalGeneration.from_pretrained("./models")
tokenizer = T5Tokenizer.from_pretrained("./models")
k = 2
input_text = f"generate product name: Grocery & Gourmet Foods,  Beverages"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
num_return_sequences = 20
temperature = 0.8
num_words = 3
num_special_tokens = 1
max_output_length = num_words + num_special_tokens

generated_outputs = model.generate(
    input_ids,
    max_length=max_output_length,
    min_length=max_output_length,
    num_return_sequences=num_return_sequences,
    temperature=temperature,
    do_sample=True,
    top_k=0,
    top_p=0.95,
)

for i in range(num_return_sequences):
    output = generated_outputs[i]
    decoded_output = tokenizer.decode(output, skip_special_tokens=True)
    print(f"Generated product name {i + 1}: {decoded_output}")