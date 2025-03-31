# Travel-Agent-AI-bot  

**Travel Agent AI Bot** is an interactive Streamlit application that leverages AI to plan personalized travel itineraries.  
It uses the **Mistral API** for natural language processing and the **SerpAPI** for fetching travel attraction data.  

---

## 🌟 Features  

### 🔹 Interactive Chat Interface  
- Chat with an AI travel buddy to plan your trip.  
- Conversational UI with customizable prompts.  

### 🔹 Dynamic Travel Itinerary Generation  
- Extracts key travel details from your conversation (**destination, duration, interests, budget, dietary needs, mobility, accommodation, and purpose**).  
- Fetches top attractions using **Google Search via SerpAPI**.  
- Generates a detailed, **day-by-day itinerary** using Mistral AI.  

### 🔹 User API Key Management  
- Securely enter your own **API keys (Mistral and SerpAPI)** to avoid consuming your developer credits.  
- Only loads the chatbot UI after valid API keys are provided.  

### 🔹 Customizable UI  
- Built with **Streamlit**, making it easy to adjust and extend the UI.  
- Possibility to incorporate **custom CSS and themes** for a unique look.  

---

## 🛠 Prerequisites  

Before running the app, ensure you have the following installed on your Ubuntu system:  
- **Python 3.8+**  
- **pip**  

---

## 📥 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Cyanide-03/Travel-Agent-AI-bot.git
cd Travel-Agent-AI-bot
```

### 2️⃣ Create a Virtual Environment  
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies  
Ensure you have a `requirements.txt` file in the repo. Then run:  
```bash
pip install -r requirements.txt
```
If `serpapi` is not in the file, add it manually:  
```bash
pip install serpapi
```

---

## 🚀 Usage  

### 1️⃣ Run the Streamlit App  
```bash
streamlit run travel_planner.py
```

### 2️⃣ Enter Your API Keys  
When the app loads, you will first see an API key entry screen. Enter your:  
- **Mistral API Key**  
- **SerpAPI Key**  

After entering valid keys, the chatbot interface will load.  

### 3️⃣ Chat with the AI Travel Buddy  
✅ Start by telling the AI where you'd like to travel.  
✅ Answer follow-up questions (**destination, duration, interests, etc.**).  
✅ Get your **personalized travel itinerary!** 🎉  

---

## 🤝 Contributing  
We welcome contributions! If you’d like to improve the project, feel free to:  
- Fork the repository  
- Create a new branch  
- Submit a pull request  

---

## ⚖️ License  
This project is licensed under the **MIT License**. See the `LICENSE` file for details.  

---

## 📞 Contact  
For any queries or feedback, reach out via:  
- **GitHub Issues**: [Cyanide-03/Travel-Agent-AI-bot](https://github.com/Cyanide-03/Travel-Agent-AI-bot/issues)  
- **Email**: your.email@example.com  

Happy Travels! ✈️🌍

