import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from datasets import Dataset
import pandas as pd

# Load the dataset generated previously
df = pd.read_csv("expanded_medical_intent_dataset.csv")

# Convert the dataset into a HuggingFace dataset format
dataset = Dataset.from_pandas(df)

# Load pre-trained BioBERT tokenizer and model (BioBERT is based on BERT, so we use BERT)
model_name = "dmis-lab/biobert-v1.1"  # BioBERT model name
tokenizer = BertTokenizer.from_pretrained(model_name)

# Tokenizing the dataset
def tokenize_function(examples):
    return tokenizer(examples['Sentence'], padding="max_length", truncation=True, max_length=128)

# Apply tokenization to the dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Convert the intent labels to integer indices
intent_labels = df['Intent'].unique().tolist()
intent_to_id = {intent: idx for idx, intent in enumerate(intent_labels)}
id_to_intent = {idx: intent for intent, idx in intent_to_id.items()}

# Add the labels to the tokenized dataset
def add_labels(examples):
    examples['labels'] = [intent_to_id[intent] for intent in examples['Intent']]
    return examples

# Apply the label conversion
tokenized_dataset = tokenized_dataset.map(add_labels, batched=True)

# Split the dataset into train and validation sets
train_dataset, val_dataset = tokenized_dataset.train_test_split(test_size=0.2).values()

# Load the BioBERT model for classification
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=len(intent_labels))

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=8,   # batch size for training
    per_device_eval_batch_size=16,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch",     # evaluate at the end of each epoch
)

# Define the Trainer
trainer = Trainer(
    model=model,                         # the model to be trained
    args=training_args,                  # training arguments
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset,            # evaluation dataset
    tokenizer=tokenizer,                 # tokenizer
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("fine_tuned_biobert")
tokenizer.save_pretrained("fine_tuned_biobert")

# Evaluate the model
trainer.evaluate()


# Prediction Example
sentence = "update patient contact info for Alice Johnson"
inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)

# Move the input tensors to the GPU if available
if torch.cuda.is_available():
    inputs = inputs.to("cuda") # Move inputs to the GPU

with torch.no_grad():
    outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=-1).item()
    print(f"Predicted intent: {id_to_intent[predicted_class]}")