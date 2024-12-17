import pandas as pd
from transformers import BertTokenizerFast
from datasets import Dataset

# Load CSV dataset
csv_path = "expanded_medical_intent_dataset.csv"  # Path to your dataset
df = pd.read_csv(csv_path)

# Parse NER tags and sentences
def parse_ner_column(ner_column):
    tokens, tags = [], []
    for word_tag in ner_column.split():
        print(word_tag.rsplit("/", 1) )
        word, tag = word_tag.rsplit("/", 1)  # Split word and tag
        tokens.append(word)
        tags.append(tag)
    return tokens, tags
# Process the dataset
def process_dataset(df):
    tokens_list, tags_list = [], []
    for ner in df["NER"]:
        tokens, tags = parse_ner_column(ner)
        tokens_list.append(tokens)
        tags_list.append(tags)
    
    return {
        "tokens": tokens_list,
        "ner_tags": tags_list,
        "intent": df["Intent"].tolist(),  # Optional, to keep intent for reference
    }

# Processed dataset
processed_data = process_dataset(df)
print(processed_data[0])
# # Extract unique NER tags and map to IDs
# unique_tags = sorted(set(tag for tags in processed_data["ner_tags"] for tag in tags))
# tag2id = {tag: idx for idx, tag in enumerate(unique_tags)}
# id2tag = {idx: tag for tag, idx in tag2id.items()}

# # Map NER tags to IDs
# def tags_to_ids(tags_list, tag2id):
#     return [[tag2id[tag] for tag in tags] for tags in tags_list]

# processed_data["ner_tags_ids"] = tags_to_ids(processed_data["ner_tags"], tag2id)
