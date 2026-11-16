# SmartStudy AI

A beginner-friendly Prompt Engineering course project. Upload a text-based PDF or paste notes to generate:
- Chapter summaries
- Multiple-choice questions with answers and explanations
- Context-grounded question answers
- Active-recall flashcards

## 1. Requirements
- Python 3.10+
- A Gemini API key
- Internet connection for Gemini API calls

## 2. Setup

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace `your_gemini_api_key_here` with your API key.

Get a key from Google AI Studio: https://aistudio.google.com/apikey

## 3. Run
```bash
streamlit run app.py
```
Streamlit will open the app in your browser.

## 4. How to use
1. Upload a text-based PDF in the sidebar, or paste text.
2. Click **Read PDF** or **Use pasted text**.
3. Choose a tab: Summarize, Generate MCQs, Ask questions or Flashcards.
4. Generate and download the result.

## 5. Prompt engineering techniques used
| Technique | Where it is used | Why |
|---|---|---|
| Role prompting | Tutor / assessment designer roles | Gives the model a clear task identity |
| Contextual prompting | Source material included in every request | Grounds responses in the student's material |
| Constraint-based prompting | Exact number of MCQs/cards, allowed source | Controls scope and reduces unsupported content |
| Structured prompting | Fixed output formats | Makes responses readable and consistent |
| Task-specific prompts | Separate prompts per feature | Improves relevance over one generic prompt |

## 6. Suggested evaluation for your report
Test at least two prompt versions for the same task:
- Baseline: "Make questions from this chapter."
- Engineered: Ask for a fixed number of four-option MCQs, one correct answer, explanations, a difficulty level, and source-only facts.

Compare:
- Instruction following (did it generate the requested number?)
- Relevance (are questions based on the chapter?)
- Clarity (are questions understandable?)
- Answer correctness (verify against the source)
- Format consistency

Use a small test set of 10 questions and manually verify the answers. Do not claim the model is always accurate.

## 7. Current limitations
- Scanned/image-only PDFs need OCR and are not supported in this starter version.
- Very long PDFs are truncated to fit the prompt. For a larger version, add chunking and retrieval (RAG).
- The app sends the extracted text and question to the Gemini API. Do not upload confidential or sensitive documents.
- Generated material should be checked against your course material.

## 8. Project abstract
SmartStudy AI is an AI-assisted learning application designed to reduce the effort required to prepare for examinations. It uses prompt engineering techniques to transform user-provided study material into summaries, multiple-choice questions, contextual explanations and flashcards. Each feature uses a task-specific prompt with explicit role, context, constraints and output structure. The project demonstrates how prompt design influences the relevance, consistency and usability of large language model outputs.
