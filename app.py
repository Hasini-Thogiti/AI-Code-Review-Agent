import streamlit as st
from streamlit_ace import st_ace
from openai import OpenAI
import re
import tempfile
import subprocess

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🚀",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

h1, h2, h3 {
    color: #00FFD1;
}

.stButton > button {
    background-color: #00FFD1;
    color: black;
    border-radius: 10px;
    height: 50px;
    width: 220px;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #00C9A7;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stMetricValue"] {
    color: #00FFD1;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# OPENROUTER CLIENT
# =====================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY"
)
# =====================================
# TITLE
# =====================================

st.title("🚀 AI Code Review Agent with Self-Reflection")

st.write(
    "Analyze Python code using AI + Self Reflection + Pylint"
)

# =====================================
# FUNCTIONS
# =====================================

def display_review(review_text):

    sections = review_text.split("🚀 Score:")

    if len(sections) > 1:

        formatted_result = "🚀 Score:" + sections[1]

        # SCORE

        score_match = re.search(
            r'(\d+)\s*/\s*100',
            formatted_result
        )

        if score_match:
            score = int(score_match.group(1))
        else:
            score = 75

        st.subheader("🚀 Code Quality Score")

        st.progress(score / 100)

        st.metric(
            label="Score",
            value=f"{score}/100"
        )

        # MISTAKES

        mistakes_match = re.search(
            r'❌ Mistakes:(.*?)⚡ Improvements:',
            formatted_result,
            re.DOTALL
        )

        if mistakes_match:

            st.subheader("❌ Mistakes")

            st.error(
                mistakes_match.group(1).strip()
            )

        # IMPROVEMENTS

        improvements_match = re.search(
            r'⚡ Improvements:(.*?)✅ Best Practices:',
            formatted_result,
            re.DOTALL
        )

        if improvements_match:

            st.subheader("⚡ Improvements")

            st.info(
                improvements_match.group(1).strip()
            )

        # BEST PRACTICES

        best_match = re.search(
            r'✅ Best Practices:(.*?)🧠 Complexity Analysis:',
            formatted_result,
            re.DOTALL
        )

        if best_match:

            st.subheader("✅ Best Practices")

            st.success(
                best_match.group(1).strip()
            )

        # COMPLEXITY

        complexity_match = re.search(
            r'🧠 Complexity Analysis:(.*?)🛠 Fixed Code:',
            formatted_result,
            re.DOTALL
        )

        if complexity_match:

            st.subheader("🧠 Complexity Analysis")

            st.warning(
                complexity_match.group(1).strip()
            )

        # FIXED CODE

        code_match = re.search(
            r'```python(.*?)```',
            formatted_result,
            re.DOTALL
        )

        if code_match:

            st.subheader("🛠 Corrected Code")

            st.code(
                code_match.group(1).strip(),
                language="python"
            )

    else:

        st.write(review_text)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([2, 1])

# =====================================
# LEFT SIDE
# =====================================

with left_col:

    st.subheader("💻 Code Editor")

    code = st_ace(
        placeholder="Write your Python code here...",
        language="python",
        theme="monokai",
        height=500
    )

    review_button = st.button("Review Code")

# =====================================
# RIGHT SIDE
# =====================================

with right_col:

    st.subheader("🤖 AI Assistant")

    if review_button:

        if code.strip() == "":

            st.warning("Please enter some code.")

        else:

            # =====================================
            # SYNTAX CHECK
            # =====================================

            try:

                compile(code, "<string>", "exec")

                syntax_result = "✅ No syntax errors detected."

            except Exception as e:

                syntax_result = f"❌ Syntax Error: {e}"

            # =====================================
            # PYLINT ANALYSIS
            # =====================================

            pylint_output = ""

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".py",
                    mode="w"
                ) as temp_file:

                    temp_file.write(code)

                    temp_file_path = temp_file.name

                pylint_result = subprocess.run(
                    [
                        "pylint",
                        temp_file_path,
                        "--disable=all",
                        "--enable=E,W",
                        "--score=n"
                    ],
                    capture_output=True,
                    text=True
                )

                pylint_output = pylint_result.stdout

            except Exception as e:

                pylint_output = f"Pylint Error: {e}"

            # =====================================
            # FIRST AI REVIEW PROMPT
            # =====================================

            prompt = f"""
You are an expert Python code reviewer.

Analyze the given Python code carefully.

Use BOTH:
1. Pylint analysis
2. Your own reasoning

IMPORTANT:
- Detect REAL mistakes only
- Do NOT complain about tiny style issues
- If code is correct, clearly say it
- Do NOT invent fake problems

Return response in EXACT format:

🚀 Score:
score/100

❌ Mistakes:
- point

⚡ Improvements:
- point

✅ Best Practices:
- point

🧠 Complexity Analysis:
- Time Complexity:
- Space Complexity:

🛠 Fixed Code:
```python
fixed_code_here
Pylint Analysis:
{pylint_output}

Python Code:
{code}
"""

        try:

            # =====================================
            # INITIAL REVIEW
            # =====================================

            with st.spinner("🤖 AI is reviewing your code..."):

                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                initial_result = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            # =====================================
            # SELF REFLECTION
            # =====================================

            reflection_prompt = f"""

You are reviewing an AI-generated code review.

Your job:

Remove false mistakes
Remove unnecessary style complaints
Improve accuracy
Improve clarity

Return response in EXACT SAME FORMAT:

🚀 Score:
score/100

❌ Mistakes:

point

⚡ Improvements:

point

✅ Best Practices:

point

🧠 Complexity Analysis:

Time Complexity:
Space Complexity:

🛠 Fixed Code:

fixed_code_here

Original Python Code:
{code}

Initial Review:
{initial_result}
"""

            with st.spinner("🧠 AI is reflecting on its review..."):

                reflection_response = (
                    client.chat.completions.create(
                        model="openai/gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "user",
                                "content": reflection_prompt
                            }
                        ]
                    )
                )

                final_result = (
                    reflection_response
                    .choices[0]
                    .message
                    .content
                )

        except Exception as e:

            st.error(f"AI Error: {e}")

            st.stop()

        # =====================================
        # DISPLAY RESULTS
        # =====================================

        st.subheader("📌 Syntax Check")

        st.write(syntax_result)

        st.subheader("🛠 Pylint Analysis")

        st.code(pylint_output)

        st.divider()

        # =====================================
        # INITIAL REVIEW
        # =====================================

        st.subheader("🤖 Initial AI Review")

        display_review(initial_result)

        st.divider()

        # =====================================
        # SELF REFLECTION REVIEW
        # =====================================

        st.subheader("🧠 Self Reflection Review")

        display_review(final_result)
#=====================================
#AI CHAT ASSISTANT
#=====================================

st.divider()

st.subheader("💬 Ask AI About Your Code")

user_question = st.text_input(
"Ask something about your code..."
)

if st.button("Ask AI"):

 if user_question.strip() != "":

    chat_prompt = f"""

You are a helpful Python mentor.

Python Code:
{code}

User Question:
{user_question}

Explain clearly and simply.
"""

    try:

        with st.spinner("🤖 AI is thinking..."):

            chat_response = (
                client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": chat_prompt
                        }
                    ]
                )
            )

            answer = (
                chat_response
                .choices[0]
                .message
                .content
            )

            st.success(answer)

    except Exception as e:

        st.error(f"AI Error: {e}")