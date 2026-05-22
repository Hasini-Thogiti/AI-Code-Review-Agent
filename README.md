# AI Code Review Agent with Self-Reflection 🚀

An AI-powered Python code review system built using Streamlit, OpenRouter, and Pylint.

This project analyzes Python code, detects mistakes, suggests improvements, follows best practices, and performs a self-reflection review loop to improve AI-generated feedback.

---

## ✨ Features

- AI-powered Python code review
- Syntax error detection
- Pylint integration
- Code quality score generation
- Mistakes detection
- Improvement suggestions
- Best practices recommendations
- Time & Space complexity analysis
- Corrected code generation
- Self-reflection AI review system
- AI chat assistant for code-related questions

---

## 🧠 Self-Reflection Workflow

Initial AI Review  
↓  
Self-Reflection Review  
↓  
Improved Final Review

The second AI review analyzes the first AI-generated response and improves its accuracy and clarity.

---

## 🛠 Technologies Used

- Python
- Streamlit
- Streamlit Ace
- OpenRouter API
- OpenAI SDK
- Pylint

---

## ▶ Run the Project

Install dependencies:

```bash
pip install streamlit openai streamlit-ace pylint

Run the application:

streamlit run app.py
🔑 API Key Setup

Replace:

api_key="YOUR_OPENROUTER_API_KEY"

with your actual OpenRouter API key.

Get your API key from:
https://openrouter.ai