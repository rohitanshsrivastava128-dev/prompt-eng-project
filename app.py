import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

load_dotenv()

st.set_page_config(page_title="SmartStudy AI", page_icon="📚", layout="wide")

st.markdown("""
<style>
.main {background: #f7f8fc;}
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {padding: 1.5rem 1.8rem; border-radius: 18px; background: linear-gradient(120deg,#182848,#4b6cb7); color: white; margin-bottom: 1.2rem;}
.hero h1 {color:white; margin:0;}
.hero p {color:#e9efff; margin:.4rem 0 0 0;}
.small-note {color:#667085; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

if "study_text" not in st.session_state:
    st.session_state.study_text = ""
if "source_name" not in st.session_state:
    st.session_state.source_name = ""

def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def extract_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages).strip()

def ask_gemini(prompt):
    client = get_client()
    if client is None:
        st.error("Gemini API key not found. Add GEMINI_API_KEY to your .env file and restart the app.")
        return None
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as exc:
        st.error(f"Could not generate a response: {exc}")
        return None

def source_context():
    return st.session_state.study_text[:45000]

st.markdown("""
<div class="hero">
  <h1>📚 SmartStudy AI</h1>
  <p>Turn your study material into clear notes, practice questions and exam-ready revision.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("1. Add study material")
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded is not None:
        if st.button("Read PDF", type="primary", use_container_width=True):
            with st.spinner("Reading your PDF..."):
                extracted = extract_pdf(uploaded)
                if extracted:
                    st.session_state.study_text = extracted
                    st.session_state.source_name = uploaded.name
                    st.success(f"Loaded {uploaded.name}")
                else:
                    st.warning("No selectable text was found. This app currently supports text-based PDFs, not scanned PDFs.")
    st.caption("You can also paste text below.")
    pasted = st.text_area("Paste notes or textbook content", height=180, placeholder="Paste your study material here...")
    if st.button("Use pasted text", use_container_width=True):
        if pasted.strip():
            st.session_state.study_text = pasted.strip()
            st.session_state.source_name = "Pasted text"
            st.success("Study material loaded.")
        else:
            st.warning("Paste some text first.")
    if st.session_state.study_text:
        st.divider()
        st.success(f"Material ready: {st.session_state.source_name}")
        st.caption(f"{len(st.session_state.study_text):,} characters loaded.")
        if st.button("Clear material", use_container_width=True):
            st.session_state.study_text = ""
            st.session_state.source_name = ""

if not st.session_state.study_text:
    st.info("Start by uploading a text-based PDF or pasting your notes in the sidebar.")
    st.markdown("### What you can do")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**📝 Smart notes**\\n\\nConvert lengthy chapters into structured revision notes.")
    c2.markdown("**❓ Practice MCQs**\\n\\nGenerate questions with answer keys and explanations.")
    c3.markdown("**💬 Ask your material**\\n\\nAsk questions and get answers grounded in your uploaded content.")
    st.stop()

st.caption(f"Working from: **{st.session_state.source_name}**")
tab_summary, tab_mcq, tab_qa, tab_flash = st.tabs(["📝 Summarize", "❓ Generate MCQs", "💬 Ask questions", "🗂️ Flashcards"])

with tab_summary:
    st.subheader("Chapter summary")
    col1, col2 = st.columns([1, 1])
    with col1:
        length = st.selectbox("Summary length", ["Quick revision", "Detailed notes", "Exam-focused"])
    with col2:
        level = st.selectbox("Language level", ["Simple student-friendly language", "University-level language"])
    if st.button("Generate summary", type="primary", key="summary"):
        prompt = f"""
You are an expert university tutor helping a student prepare for exams.
Use only the source material below. Do not invent facts.
Create {length.lower()} in {level.lower()}.
Organize the response with:
1. A short overview
2. Important concepts and definitions
3. Key points in bullet form
4. Examples, if present in the source
5. Five likely exam takeaways
If information is missing, say so instead of guessing.

SOURCE MATERIAL:
{source_context()}
"""
        with st.spinner("Creating your notes..."):
            result = ask_gemini(prompt)
        if result:
            st.markdown(result)
            st.download_button("Download notes (.txt)", result, file_name="smartstudy_notes.txt")

with tab_mcq:
    st.subheader("MCQ practice generator")
    a, b = st.columns(2)
    with a:
        count = st.slider("Number of questions", 5, 20, 10)
    with b:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])
    if st.button("Generate MCQs", type="primary", key="mcq"):
        prompt = f"""
You are an assessment designer creating a fair university-level practice quiz.
Create exactly {count} multiple-choice questions at {difficulty.lower()} difficulty using ONLY the source material.
Each question must have four options labelled A, B, C, D, exactly one correct answer,
the correct answer, and a short explanation. Avoid duplicate questions and trick wording.
Use this format:
### Q1. [Question]
A. ...
B. ...
C. ...
D. ...
**Answer:** ...
**Explanation:** ...
Do not include facts absent from the source.

SOURCE MATERIAL:
{source_context()}
"""
        with st.spinner("Writing your practice questions..."):
            result = ask_gemini(prompt)
        if result:
            st.markdown(result)
            st.download_button("Download MCQs (.txt)", result, file_name="smartstudy_mcqs.txt")

with tab_qa:
    st.subheader("Ask your study material")
    question = st.text_area("What would you like to understand?", placeholder="Example: Explain the difference between supervised and unsupervised learning.")
    style = st.selectbox("Answer style", ["Explain simply with an example", "Give a concise exam answer", "Explain step by step"])
    if st.button("Get answer", type="primary", key="qa"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            prompt = f"""
You are a patient university tutor.
Answer the student's question in this style: {style}.
Base the answer ONLY on the source material. If the source does not contain enough information,
clearly say that. Do not fabricate citations, page numbers or facts.
Where useful, finish with a one-sentence recap.

STUDENT QUESTION:
{question}

SOURCE MATERIAL:
{source_context()}
"""
            with st.spinner("Finding an answer in your material..."):
                result = ask_gemini(prompt)
            if result:
                st.markdown(result)

with tab_flash:
    st.subheader("Flashcard generator")
    number = st.slider("Number of flashcards", 5, 20, 10, key="flashcount")
    if st.button("Create flashcards", type="primary", key="flash"):
        prompt = f"""
You are creating active-recall flashcards for university students.
Create exactly {number} concise flashcards from the source material.
Each card must test one important concept. Avoid vague questions.
Format each as:
**Card 1 — Front:** [question or term]
**Back:** [clear answer, maximum 3 sentences]
Use only information in the source.

SOURCE MATERIAL:
{source_context()}
"""
        with st.spinner("Creating flashcards..."):
            result = ask_gemini(prompt)
        if result:
            st.markdown(result)
            st.download_button("Download flashcards (.txt)", result, file_name="smartstudy_flashcards.txt")

st.divider()
with st.expander("How this project demonstrates prompt engineering"):
    st.markdown("""
    - **Role prompting:** The model is assigned a specific role such as university tutor or assessment designer.
    - **Contextual prompting:** Uploaded study material is supplied as context.
    - **Constraint-based prompting:** Prompts specify exact question counts, answer formats and source-grounding rules.
    - **Task decomposition:** Different tabs use purpose-built prompts for summarizing, question answering and assessment generation.
    - **Structured output:** The model is instructed to follow repeatable formats.

    For your project demonstration, compare a vague prompt with one of the engineered prompts and discuss differences in relevance, structure and factual grounding.
    """)
st.caption("SmartStudy AI • Academic prototype. Always verify generated study material against your course notes.")
