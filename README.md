# Inventory Master Pro AI 🤖📦
AI-powered assistant  using RAG, ChromaDB, LangGraph, and Chainlit.

**Inventory Master Pro AI** is a **powerful AI-powered chatbot** designed to help businesses and users manage, explore, and gain insights into inventory data efficiently. Leveraging **Retrieval-Augmented Generation (RAG)**, it delivers **context-aware, intelligent responses** based on your inventory dataset. Built with **Chainlit**, **LangGraph**, **ChromaDB**, this chatbot is perfect for **real-time AI-assisted inventory management**.

---

🏆 Built With
- **Chainlit** - Rapid LLM app prototyping  
- **LangGraph** - Conversation orchestration  
- **LangChain** - LLM workflows & utilities  
- **ChromaDB** - Vector database for context retrieval  
- **Gemini-Flash 2.0** - Google Generative AI model for conversational responses  
- **NomicAI** - Model for embeddings and vector-based retrieval

## 🚀 Features

- **AI-Powered Chatbot:** Interactive, intelligent responses in real-time using **gemini-flash** chat model.
- **Embeddings:** Generate embeddings by using **Nomic AI** embedding model.
- **Context Retrieval:** Fetches relevant inventory insights from a ChromaDB vector store.  
- **Custom RAG Pipeline:** Combines large language models with your inventory data for accurate answers.  
- **Real-Time Streaming:** Seamless live response streaming for interactive conversations.  
- **Multi-Platform Ready:** Optimized for web deployment using Chainlit & LangGraph.  
- **Customizable UI:** Personalize your assistant’s avatar, welcome screen, and interface.

---
## 💡 How It Works
Scraping & Data Processing: Inventory data is scraped and cleaned into JSON files.

Vector Store Indexing: Data is embedded and indexed into ChromaDB for fast retrieval.

RAG Pipeline: embedded user queries are matched with relevant data chunks, then processed with an AI model.

Streaming Responses: Responses are sent to users in real-time via Chainlit interface.

<img width="2588" height="750" alt="image" src="https://github.com/user-attachments/assets/43dcd505-3564-456e-8a52-9c6e47bce672" />

## ⚡ Quick Start

**Clone the repository**
```
bash
git clone https://github.com/Ayesha-sadaf/Inventory-master-pro-ai.git
cd Inventory-master-AI-assistant-chatbot/Backend
```

**Create & activate a virtual environment**
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
**Install dependencies**
```
pip install -r requirements.txt
```
**Set environment variables**
```
GOOGLE_API_KEY=your_google_api_key
NOMIC_API_KEY= your_nomicai_key
```

**Run Locally**
```
chainlit run app.py -w
```
**Scraper**
The **Scraper Module** allows you to **scrape data from any website** and convert it into a structured JSON format suitable for AI processing. By modifying the target URL(s) and specifying the relevant HTML selectors, you can extract:

- Text content  
- Headings & subheadings  
- Paragraphs and lists  
- Metadata like URLs and timestamps  

## How It Works

1. **Specify Target URLs:** Add the websites you want to scrape in the script or a config file.  
2. **Define Selectors:** Adjust the scraping logic to capture the relevant content, e.g., headings, paragraphs, or specific HTML elements.  
3. **Run Scraper:** Execute the `scraper.py` script to fetch content.  
4. **Generate JSON:** The scraper outputs a JSON file


## 📌 Customization 
Welcome Screen: Edit chainlit.md to update the greeting message.

Avatar & Branding: Update images in public/ and reference them in .chainlit/config.toml.

## 📄 About The Inventory Data
Data is collected and processed from The Inventory Master to provide relevant insights and AI-powered recommendations for inventory management.

