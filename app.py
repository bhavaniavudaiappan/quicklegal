import streamlit as st
st.set_page_config(page_title="QuickLegal", layout="centered")

import time
from utils import summarize_text, find_red_flags, split_text
from PyPDF2 import PdfReader

st.title("📜 QuickLegal - Legal Document Summarizer")

# 📤 File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
content = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            content += page.extract_text() or ""
    elif uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")

# 🔼 Text input
manual_input = st.text_area("📄 Or paste your legal text here:", height=300)
if manual_input.strip():
    content = manual_input

# 📤 Button to summarize
if st.button("🧠 Summarize") and content.strip():
    st.info("⏳ Starting summarization...")

    # Split text to show chunk info
    chunks = split_text(content)
    total_chunks = len(chunks)

    # Calculate word count
    original_word_count = len(content.split())

    start_time = time.time()

    # Progress and timing
    with st.spinner(f"Summarizing {total_chunks} chunk(s)..."):
        summary = summarize_text(content)

    end_time = time.time()
    time_taken = end_time - start_time
    summarized_word_count = len(summary.split())

    # 📈 Results
    st.success("✅ Summary Generated!")

    col1, col2, col3 = st.columns(3)
    col1.metric("📝 Original Words", f"{original_word_count}")
    col2.metric("✂️ Summary Words", f"{summarized_word_count}")
    col3.metric("⏱ Time Taken (s)", f"{round(time_taken, 2)}")

    st.markdown("### 📌 Summary")
    st.markdown(f"<div style='background-color:#f0f2f6;padding:10px;border-radius:6px'>{summary}</div>", unsafe_allow_html=True)

    # 📥 Download button
    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="summary.txt",
        mime="text/plain"
    )

    st.markdown("### 🚨 Red Flags (if any)")
    red_flags = find_red_flags(content)
    if red_flags:
        for flag in red_flags:
            st.warning(flag)
    else:
        st.success("✅ No red flags found.")
