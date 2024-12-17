import pandas as pd
from transformers import BertTokenizerFast
from datasets import Dataset

# Load CSV dataset
csv_path = "expanded_medical_intent_dataset.csv"  # Path to your dataset
df = pd.read_csv(csv_path)

# Parse NER tags and sentences
def parse_ner_column(ner_column):
    tokens, tags = [], []
    word_tag_pairs = ner_column.split()
    i = 0
    while i < len(word_tag_pairs):
        if i + 1 < len(word_tag_pairs) and word_tag_pairs[i + 1].startswith("B-"):
            word = word_tag_pairs[i]
            tag = word_tag_pairs[i + 1]
            tokens.append(word)
            tags.append(tag)
            i += 2
        else:
            word, tag = word_tag_pairs[i].rsplit("/", 1)
            tokens.append(word)
            tags.append(tag)
            i += 1
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
processed_data_df = pd.DataFrame(processed_data)
processed_data_df.to_csv("processed_ner_dataset.csv", index=False)

