import os
from openai import OpenAI
import openai
import streamlit as st
import google.generativeai as genai
import json

answer = """ {
  "question": "What is the value of 7 multiplied by 5?",
  "choices": [
    "A. 30",
    "B. 35",
    "C. 40",
    "D. 45"
  ],
  "correct_answer": "B. 35",
  "explanation": "To find the value of 7 multiplied by 5, you can either add 7 together 5 times (7 + 7 + 7 + 7 + 7) or multiply directly (7 * 5). Both methods will give you the result of 35."
}
"""

# Initialize OpenAI and configure API keys
clients = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
genai.configure(api_key=st.secrets["GOOGLE_KEY"])

def get_question(subject):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an AI that generates educational content. You will generates question each time."""
                            ,
            },
            {
                "role": "user",
                "content": f"""Generate a random STEM related question for a 9-year-old about {subject}. Provide four multiple choices with the correct answer. Provide the correct answer separately and provide an explanation for the correct answer. Provide the response as a JSON containing question, choices, correct_answer, and explanation. Make the output like this: {answer}""",
            },
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    quiz = response.choices[0].message.content
    print(quiz)
    quiz_data = json.loads(quiz)
    return quiz_data

def initialize_session_state():
    if 'form_count' not in st.session_state:
        st.session_state.form_count = 0
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'selected_subject' not in st.session_state:
        st.session_state.selected_subject = None

def main():
    st.markdown(
        """
        <style>
        .title {
            font-size: 3em;
            font-weight: bold;
            color: #FFFF7A;
            text-align: center;
            margin-top: 0.5em;
            margin-bottom: 0.5em;
        }
        .subtitle {
            font-size: 1.5em;
            color: #306998;
            text-align: center;
            margin-bottom: 1.5em;
        }
        .stButton button {
            background-color: #FFFF7A;
            color: black;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 1em;
        }
        .stButton button:hover {
            background-color: #FFFF7A;
        }
        .question {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 1em;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="title">Interactive Learning Quiz</div>', unsafe_allow_html=True)

    # Initialize session state variables
    initialize_session_state()

    subjects = ["Mathematic", "Science", "History", "Islamic Religious Education","Music"]
    selected_subject = st.selectbox("Choose a subject:", subjects)

    if st.button("Generate Quiz"):
        with st.spinner("Generating the quiz..."):
            st.session_state.quiz_data = get_question(selected_subject)
            st.session_state.selected_subject = selected_subject
            st.session_state.form_count = 0
        st.rerun()

    if st.session_state.quiz_data:
        quiz_data = st.session_state.quiz_data

        st.markdown(f'<div class="question">Question: {quiz_data["question"]}</div>', unsafe_allow_html=True)

        form = st.form(key=f"quiz_form{st.session_state.form_count}")
        user_choice = form.radio(label="Choose an answer", options=quiz_data['choices'])
        submitted = form.form_submit_button("Submit")

        if submitted:
            if user_choice == quiz_data['correct_answer']:
                st.success("Correct!", icon="✅")
            else:
                st.error(f"Incorrect. The correct answer is: {quiz_data['correct_answer']}")
            st.markdown(f"**Explanation:** {quiz_data['explanation']}")

        if st.button("Another question"):
            with st.spinner("Generating the next question..."):
                st.session_state.quiz_data = get_question(st.session_state.selected_subject)
                st.session_state.form_count += 1
            st.rerun()

if __name__ == "__main__":
    main()
