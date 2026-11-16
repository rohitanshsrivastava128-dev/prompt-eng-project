# SmartStudy AI — Prompt Engineering Notes

## Problem statement
Students often need to convert lengthy study material into revision notes and practice questions. Creating these manually takes time and can make revision less efficient.

## Objective
Build a web application that uses carefully designed prompts to generate study aids from user-provided text.

## System workflow
1. User uploads a PDF or pastes study material.
2. The application extracts text.
3. The user chooses a task.
4. A task-specific prompt is constructed with instructions and source context.
5. Gemini generates the response.
6. The application displays the result and allows it to be downloaded.

## Prompt design framework
Each engineered prompt includes:
- **Role:** Who the model should act as.
- **Task:** What it must produce.
- **Context:** The uploaded source text.
- **Constraints:** What it may or may not do.
- **Output format:** How the result should be structured.

## Example: baseline vs engineered prompt

### Baseline
> Make MCQs from this chapter.

### Engineered
> You are an assessment designer creating a fair university-level practice quiz. Create exactly 10 multiple-choice questions at medium difficulty using only the source material. Each question must have four options labelled A, B, C, D, exactly one correct answer, and a short explanation. Avoid duplicate questions and trick wording. Do not include facts absent from the source.

### Expected difference
The engineered prompt is more specific about role, number of questions, difficulty, option count, answer uniqueness, explanations and source restrictions. Evaluate actual outputs rather than assuming the engineered prompt is always better.

## Evaluation plan
Use the same chapter and compare baseline and engineered prompts. Score each output from 1–5 on:
1. Relevance to source
2. Factual correctness
3. Instruction following
4. Clarity
5. Format consistency

Have a student manually verify factual correctness against the source. Record scores in a comparison table.

## Conclusion
The project demonstrates that prompt engineering is not simply sending text to an AI model. It involves defining the role, context, task constraints and output structure to make model responses more useful and assessable.
