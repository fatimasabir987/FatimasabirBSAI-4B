"""
app.py — Hotel Information QnA Bot (Lab 12)

Pipeline:
  1. Load hotel_data_clean.csv + FAISS index
  2. Load MiniLM model for query embedding
  3. On /search: clean query -> MiniLM embed -> FAISS search -> return top-3
  4. Serve Flask routes to HTML frontend

Usage:
  1. Run build_index.py first (once)
  2. python app.py
  3. Open http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ── Load resources at startup ─────────────────────────────────────────────────
print("Loading FAISS index and dataset...")
df = pd.read_csv("hotel_data_clean.csv")
index = faiss.read_index("hotel_faiss.index")

print("Loading MiniLM model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

print(f"Ready! {len(df)} QnA entries | FAISS index: {index.ntotal} vectors.")


# ── Text cleaning (same as build_index.py) ────────────────────────────────────
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower().strip()
    else:
        text = ''
    return text


# ── Embed query using MiniLM ──────────────────────────────────────────────────
def embed_query(query):
    """Clean query text and embed using MiniLM (same model as build_index.py)."""
    cleaned = clean_text(query)
    embedding = model.encode([cleaned])
    return np.array(embedding).astype("float32")


# ── FAISS Retrieval ───────────────────────────────────────────────────────────
def retrieve_top_k(query, k=3):
    """
    Embed query -> search FAISS index -> return top-k results.
    Lower L2 distance = more semantically similar.
    """
    query_vec = embed_query(query)
    distances, indices = index.search(query_vec, k)

    results = []
    for i in range(k):
        idx = indices[0][i]
        dist = float(distances[0][i])
        if idx < len(df):
            results.append({
                "question": df["question"].iloc[idx],
                "answer":   df["answer"].iloc[idx],
                "category": df["category"].iloc[idx],
                "distance": round(dist, 4),
                "rank":     i + 1
            })
    return results


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    results = retrieve_top_k(query, k=3)
    return jsonify({
        "query":   query,
        "results": results,
        "total":   len(results)
    })


@app.route("/categories", methods=["GET"])
def categories():
    cats = df["category"].value_counts().to_dict()
    return jsonify(cats)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)