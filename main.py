from openai import OpenAI
from google.generativeai import genai
from IPython.display import display, Image
import os

client = OpenAI(api_key=os.environ["SECRET_KEY"]
)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def story_ai(msg, sysprompt):
    story_response = client.chat.completions.create(model="gpt-4o",
    messages=[{
        "role":"system",
        "content":sysprompt},
            {
                "role": "user",
                "content": msg
        }],
         max_tokens=300)

    story = story_response.choices[0].message.content
    return story


def art_ai(msg):
    art_response = client.images.generate(model="dall-e-2",
                                          prompt=msg,
                                          size="1024x1024",
                                          n=1)

    art = art_response.data[0].url
    return art


def design_ai(msg):
    design_model = genai.GenerativeModel('gemini-1.5-flash')
    design = design_model.generate_content([
        f"""
  Define a fiting prompt for an AI image generator
  to generate a most fitting cover art for this story:
  {msg}
  """
    ])

    return design.text


def storybook_ai(msg, sysprompt):
    story = story_ai(msg, sysprompt)
    art = art_ai(story)
    design = design_ai(story)
    st.image(art)
    st.write(story)

sysprompt = """
You are a bestselling author.
You will take in a user's request and create a 100 word short story.
The story should be suitable for children ages 7-9.
"""

msg = st.text_input("Write a story about a boy meet a spiderman")
storybook_ai(msg, sysprompt)
