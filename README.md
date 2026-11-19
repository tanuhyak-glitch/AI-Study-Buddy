🎓 AI Study Buddy

An AI-powered study assistant built with Python, Streamlit, and Groq AI to help students learn concepts, summarize notes, practice quizzes, and track their learning activities.

🚀 Live Demo

"Try AI Study Buddy" (PASTE_YOUR_DEPLOYED_APP_URL_HERE)

✨ Features

- Topic Explainer — Learn complex topics with simple explanations, examples, analogies, and programming examples.
- Notes Summarizer — Convert lengthy study material into structured revision notes.
- Interactive Quiz — Generate AI-powered MCQs, answer questions, receive feedback, and view your score.
- Study History — Review saved explanations, summaries, and quiz results.
- Dashboard — Track study activities and quiz performance.

🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- GPT-OSS 20B
- JSON for local study-history storage

⚙️ Run Locally

1. Clone the repository:
   
   git clone https://github.com/YOUR_USERNAME/AI-Study-Buddy.git

2. Navigate to the project directory:
   
   cd AI-Study-Buddy

3. Create a virtual environment:
   
   python -m venv .venv

4. Activate the environment (Windows):
   
   .\.venv\Scripts\Activate.ps1

5. Install dependencies:
   
   pip install -r requirements.txt

6. Create ".streamlit/secrets.toml" and add:
   
   GROQ_API_KEY = "your_groq_api_key"

7. Run the application:
   
   streamlit run app.py

🔐 API Key Security

The Groq API key is stored using Streamlit secrets and is excluded from Git through ".gitignore".

Never commit API keys or other sensitive credentials.

📌 Future Improvements

- Persistent cloud database for study history
- User authentication and personalized study profiles
- Flashcards and spaced repetition
- Progress analytics
- Additional quiz formats

👩‍💻 Author

Built as a hands-on project to explore Python, AI integration, API usage, application development, and deployment.
