import torch
import torch.nn.functional as F
import numpy as np
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)
import streamlit as st

@st.cache_resource
def load_model():
    return DistilBertForSequenceClassification.from_pretrained("saved_model_final")
# === Les 13 émotions ===
labels = [
    "anger",
    "boredom",
    "empty",
    "enthusiasm",
    "fun",
    "happiness",
    "hate",
    "love",
    "neutral",
    "relief",
    "sadness",
    "surprise",
    "worry"
]

# === Chargement du modèle ===
model = DistilBertForSequenceClassification.from_pretrained(
    "saved_model_final"
)

tokenizer = DistilBertTokenizer.from_pretrained(
    "saved_model_final"
)

# Mode évaluation
model.eval()

# === Fonction principale ===
def analyze_user_text(text):

    # Tokenization
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    # Désactivation du gradient
    with torch.no_grad():

        outputs = model(**inputs)

        # Softmax → probabilités
        probs = F.softmax(
            outputs.logits,
            dim=-1
        ).squeeze().cpu().numpy()

    # Création du vecteur émotionnel
    sentiment_vector = {
        labels[i]: round(float(probs[i]) * 100, 2)
        for i in range(len(labels))
    }

    # Emotion dominante
    dominant = labels[int(np.argmax(probs))]

    return dominant, sentiment_vector