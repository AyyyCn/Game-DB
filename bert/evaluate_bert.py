"""Loads the fine-tuned model.
Evaluates model accuracy on the validation set."""
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, classification_report

# Load Data
val_df = pd.read_csv('bert/val.csv')
val_df['text'] = val_df['text'].astype(str).fillna('')
# Load Model and Tokenizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained("bert/fine_tuned_model")
model = BertForSequenceClassification.from_pretrained("bert/fine_tuned_model").to(device)

class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(list(texts), truncation=True, padding=True, max_length=128, return_tensors="pt")
        self.labels = torch.tensor(labels,dtype=torch.long)

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}, self.labels[idx]

    def __len__(self):
        return len(self.labels)

# Encode Labels
val_labels = val_df['label'].factorize()[0]  # Assuming already labeled as 0, 1, 2
val_dataset = SentimentDataset(val_df['text'], val_labels)
val_loader = DataLoader(val_dataset, batch_size=16)

# Evaluation
model.eval()
preds, truths = [], []

with torch.no_grad():
    for batch, labels in val_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)

        preds.extend(predictions.cpu().numpy())
        truths.extend(labels.numpy())

# Accuracy and Report
print("Accuracy:", accuracy_score(truths, preds))
print("Classification Report:\n", classification_report(truths, preds, target_names=['Negative', 'Neutral', 'Positive']))
