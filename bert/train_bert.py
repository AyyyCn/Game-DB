"""Loads the pre-trained BERT model.
Fine-tunes BERT on your sentiment-labeled data.
Saves the fine-tuned model."""
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import LabelEncoder

# Check GPU availability
print("GPU Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device Name:", torch.cuda.get_device_name(0))
else:
    print("Using CPU.")

# Load Data
train_df = pd.read_csv('bert/train.csv')
val_df = pd.read_csv('bert/val.csv')

# Ensure all texts are strings
train_df['text'] = train_df['text'].astype(str).fillna('')
val_df['text'] = val_df['text'].astype(str).fillna('')

# Encode Labels (0, 1, 2 for Negative, Neutral, Positive)
encoder = LabelEncoder()
train_labels = encoder.fit_transform(train_df['label'])
val_labels = encoder.transform(val_df['label'])

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Dataset Class
class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(list(texts), truncation=True, padding=True, max_length=128, return_tensors="pt")
        self.labels = torch.tensor(labels, dtype=torch.long)  # Ensure labels are LongTensor

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}, self.labels[idx]

    def __len__(self):
        return len(self.labels)


# Prepare Datasets and DataLoaders
train_dataset = SentimentDataset(train_df['text'], train_labels)
val_dataset = SentimentDataset(val_df['text'], val_labels)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Load Model and Optimizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3).to(device)
optimizer = AdamW(model.parameters(), lr=5e-5)

# Training Loop
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0
    print(f"Starting Epoch {epoch + 1}/{epochs}...")
    
    for batch, labels in train_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(**batch, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1} Completed. Average Loss: {total_loss / len(train_loader):.4f}")

# Save Fine-Tuned Model
output_dir = "bert/fine_tuned_model"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Model fine-tuned and saved to {output_dir}.")
