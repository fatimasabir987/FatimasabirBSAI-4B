"""
build_index.py — Hotel QnA Bot (Lab 12)
Builds FAISS vector index from hotel_data.csv using MiniLM embeddings.

Pipeline:
  1. Load & preprocess hotel_data.csv
  2. Embed questions using paraphrase-MiniLM-L6-v2 (Hugging Face)
  3. Store embeddings in FAISS IndexFlatL2
  4. Save index + cleaned data for use in app.py

Usage: python build_index.py
"""

import pandas as pd
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer

# ── 1. Load & Preprocess ──────────────────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv("hotel_data.csv")

# Drop empty rows
df.dropna(subset=["question", "answer"], inplace=True)
df.reset_index(drop=True, inplace=True)

def clean_text(text):
    """Lowercase and remove non-alphabetic characters."""
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower().strip()
    else:
        text = ''
    return text

df["clean_question"] = df["question"].apply(clean_text)

print(f"Total QnA pairs loaded: {len(df)}")
print(f"Categories: {list(df['category'].unique())}")

# ── 2. Embed using Hugging Face MiniLM ───────────────────────────────────────
print("\nLoading MiniLM model (paraphrase-MiniLM-L6-v2)...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

print("Generating embeddings...")
embeddings = model.encode(df["clean_question"].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

print(f"Embedding shape: {embeddings.shape}")  # (56, 384)

# ── 3. Build FAISS Index (IndexFlatL2) ────────────────────────────────────────
print("\nBuilding FAISS index (IndexFlatL2)...")
d = embeddings.shape[1]   # 384 dimensions for MiniLM
index = faiss.IndexFlatL2(d)
index.add(embeddings)

print(f"Total vectors in index: {index.ntotal}")

# Save index to disk
faiss.write_index(index, "hotel_faiss.index")
print("FAISS index saved -> hotel_faiss.index")

# Save cleaned dataframe
df.to_csv("hotel_data_clean.csv", index=False)
print("Cleaned data saved -> hotel_data_clean.csv")

print("\nIndex build complete! Now run: python app.py")