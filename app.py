import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.llms import Ollama
from gtts import gTTS
import tempfile
import requests
import speech_recognition as sr

# Initialize the Ollama model with a specific model version (llama3.1:8b)
try:
    model = Ollama(model="llama3.1:8b")
except requests.exceptions.ConnectionError as e:
    st.error(f"Error connecting to Ollama: {e}")
    st.stop()

# Define a prompt template for Indian language translations
indian_languages = ["Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam", "Punjabi", "Assamese", "Odia"]

generic_template = "Translate the following into {language}:"

# Create a chat-based prompt template using the defined generic template
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Set up the output parser to process the model's output as a string
parser = StrOutputParser()

# Chain the prompt, model, and parser together
chain = prompt | model | parser

# Streamlit app interface begins
st.set_page_config(page_title="Language Translator", layout="centered")

# Apply custom CSS for better styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f8ff9a, #a1ffce);
        font-family: Arial, sans-serif;
        color: #333333;
    }
    .stButton>button {
        background-color: #FF5722;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 5px;
        transition: transform 0.2s, background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #E64A19;
        transform: scale(1.1);
    }
    .translated-text {
        margin-top: 20px;
        padding: 15px;
        background: #ffffff;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states for text input and speech recognition
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Title
st.markdown("<h1 style='text-align: center; animation: fadeIn 2s;'>Language Translator 🗣️</h1>", unsafe_allow_html=True)

# Add speech-to-text functionality
recognizer = sr.Recognizer()
st.subheader("Enter the details below:")
if st.button("🎤 Speak Now"):
    with st.spinner("Listening... Please speak clearly into the microphone."):
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                st.session_state.speech_text = recognizer.recognize_google(audio)
                st.success(f"You said: {st.session_state.speech_text}")
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service: {e}")

# Use speech text if available; otherwise, allow manual input
st.session_state.input_text = st.text_input("Type the Word or Sentence", st.session_state.speech_text)
input_language = st.selectbox("Select Translation Language", indian_languages)

# Define a button that will trigger the translation process
if st.button("Translate"):
    if not st.session_state.input_text.strip():
        st.error("Please enter a word or sentence to translate!")
    else:
        with st.spinner("Translating... please wait!"):
            try:
                # Invoke the chain of prompt, model, and parser to generate the translated output
                translated_output = chain.invoke({
                    "language": input_language,
                    "text": st.session_state.input_text
                })
                # Display the translated output
                st.markdown(
                    f"<div class='translated-text'><strong>Translated output:</strong> {translated_output}</div>",
                    unsafe_allow_html=True
                )

                # Generate and play the audio for the translated text
                st.subheader("🎧 Listen to the Translation")

                # Language mapping for gtts
                language_map = {
                    "Hindi": "hi",
                    "Bengali": "bn",
                    "Telugu": "te",
                    "Marathi": "mr",
                    "Tamil": "ta",
                    "Gujarati": "gu",
                    "Urdu": "ur",
                    "Kannada": "kn",
                    "Malayalam": "ml",
                    "Punjabi": "pa",
                    "Assamese": "as",
                    "Odia": "or"
                }

                tts = gTTS(text=translated_output, lang=language_map.get(input_language, "hi"))
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                    tts.save(temp_audio.name)
                    st.audio(temp_audio.name, format="audio/mp3")

            except requests.exceptions.ConnectionError as e:
                st.error(f"Error connecting to Ollama: {e}")
            except Exception as e:
                st.error(f"Error During Translation: {e}")

# Footer
st.markdown(
    "<p style='text-align: center; margin-top: 20px; font-size: 14px;'>Made with ❤️ for Indian languages using Streamlit</p>",
    unsafe_allow_html=True
)
