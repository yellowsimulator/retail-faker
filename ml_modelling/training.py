from pathlib import Path
from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

from preprocessing import preprocess_examples
from models import t5_models

model_name = t5_models["small"]["name"]
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)



# dataset for training
trainin_data_path = str(Path("data/train.csv"))
validation_data_path = str(Path("data/validation.csv"))
train_dataset = load_dataset("csv", data_files=trainin_data_path, split="train",
                             column_names=["input_text", "target_text"])
validation_dataset = load_dataset("csv", data_files=validation_data_path, split="train",
                                   column_names=["input_text", "target_text"])

train_dataset = train_dataset.map(lambda examples: preprocess_examples(examples, tokenizer), batched=True)
validation_dataset = validation_dataset.map(lambda examples: preprocess_examples(examples, tokenizer), batched=True)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)


# setup training
training_args = Seq2SeqTrainingArguments(
    output_dir="./models",
    num_train_epochs=50,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    save_steps=500,
    save_total_limit=2,
    evaluation_strategy="steps",
    eval_steps=500,
    logging_steps=100,
    learning_rate=3e-3,
    warmup_steps=200,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)

trainer.train()

# save the fine-tuned model
model.save_pretrained("./models")
tokenizer.save_pretrained("./models")





