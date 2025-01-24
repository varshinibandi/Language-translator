# Language Translator 🗣️

A powerful, user-friendly Language Translator built using **Streamlit**, **LangChain**, and **Google Text-to-Speech (gTTS)**. This application is designed specifically for Indian languages, enabling translations and audio playback in multiple regional languages.

---

## **Explanation**

This Language Translator takes a user-inputted sentence or word and translates it into one of the supported Indian languages. It also provides audio playback of the translated sentence using Google Text-to-Speech (gTTS). The application leverages:

- **LangChain**: For managing and processing prompt chains with the `Ollama` language model.
- **Ollama Model**: A language model used to generate the translations.
- **gTTS**: Converts the translated text into audio for playback.

The app is styled using custom CSS for a visually appealing UI and uses Streamlit for a simple yet dynamic interface.

---

## **Features**

- **Multi-Language Support**: Translates sentences into 12 popular Indian languages:
  - Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Urdu, Kannada, Malayalam, Punjabi, Assamese, Odia.
- **Audio Playback**: Listen to the translated text in the selected language.
- **Interactive Interface**: Simple and user-friendly design powered by Streamlit.
- **Custom Styling**: Attractive UI with animations and hover effects.
- **Error Handling**: Displays proper error messages for invalid input or connection issues.

---

## **Installation Guide**

### **1. Prerequisites**
Ensure you have the following installed:
- Python 3.8 or higher
- Anaconda or Virtual Environment (optional)
- Git

### **2. Clone the Repository**
```bash
git clone https://github.com/your-username/language-translator.git
cd language-translator

