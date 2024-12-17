import pandas as pd
from datasets import Dataset, ClassLabel
from transformers import BertTokenizerFast, BertForTokenClassification, TrainingArguments, Trainer

# Load Dataset
file_path = "processed_ner_dataset.csv"
df = pd.read_csv(file_path)

# Ensure token and ner_tags are in list format
df["tokens"] = df["tokens"].apply(eval)  # Convert strings to lists
df["ner_tags"] = df["ner_tags"].apply(eval)  # Convert strings to lists

# Extract unique tags
unique_tags = sorted(set(tag for tags in df["ner_tags"] for tag in tags))
tag2id = {tag: idx for idx, tag in enumerate(unique_tags)}
id2tag = {idx: tag for tag, idx in tag2id.items()}

# Convert ner_tags to ID format
df["ner_tags_ids"] = df["ner_tags"].apply(lambda tags: [tag2id[tag] for tag in tags])

# Convert to Hugging Face Dataset
hf_dataset = Dataset.from_pandas(df)

# Preprocessing
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True, padding="max_length"
    )
    labels = []
    for i, ner_tags in enumerate(examples["ner_tags_ids"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None or word_idx == previous_word_idx:
                label_ids.append(-100)  # Ignore token
            else:
                label_ids.append(ner_tags[word_idx])
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Apply preprocessing
tokenized_dataset = hf_dataset.map(tokenize_and_align_labels, batched=True)

# Train-Test Split
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split["train"]
test_dataset = train_test_split["test"]

# Fine-Tune BERT
model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(unique_tags))

training_args = TrainingArguments(
    output_dir="./ner_finetuned_model",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()
