import re
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="sanatann/legal-summarizer-bart",
        tokenizer="sanatann/legal-summarizer-bart"
    )

summarizer = load_summarizer()

def split_text(text, max_chunk_words=450, overlap=50):
    words = text.strip().split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + max_chunk_words]
        chunks.append(" ".join(chunk))
        i += max_chunk_words - overlap
    return chunks

def summarize_text(text):
    chunks = split_text(text)
    summaries = []
    for i, chunk in enumerate(chunks):
        try:
            res = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
            summaries.append(res[0]['summary_text'])
        except Exception as e:
            summaries.append(f"[Error summarizing part {i+1}: {e}]")
    return "\n\n".join(summaries)

def find_red_flags(text):
    red_flags = []
    patterns = {
        "Data Sharing": r"(share|sell).*(data|information)",
        "Third Parties": r"third[- ]?part(y|ies)",
        "No Opt-Out": r"not.*opt[- ]?out",
        "Tracking": r"(track|monitor|collect).*behavior",
        "Retain Data": r"retain.*data.*(indefinitely|long)"
    }
    for label, pat in patterns.items():
        if re.search(pat, text, re.IGNORECASE):
            red_flags.append(f"⚠️ Potential issue with: {label}")
    return red_flags
