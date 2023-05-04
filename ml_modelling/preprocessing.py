import transformers



def preprocess_examples(examples: dict, tokenizer: transformers.T5Tokenizer):
    """Preprocess function for the T5 model.

    Parameters
    ----------
        examples: the examples to preprocess, this is a batch of examples
                  containing the input and target text.
        tokenizer: the tokenizer to use to preprocess the examples.
                   handles converting text to numerical values.

    Returns
    -------
        dict: the preprocessed examples.
    """
    inputs = examples["input_text"]
    targets = examples["target_text"]
    input_encodings = tokenizer(inputs, truncation=True, padding="longest", max_length=128)
    target_encodings = tokenizer(targets, truncation=True, padding="longest", max_length=128)
    return {
        "input_ids": input_encodings["input_ids"],
        "attention_mask": input_encodings["attention_mask"],
        "labels": target_encodings["input_ids"],
    }