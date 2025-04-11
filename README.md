# Hiring_Assistant_Chatbot (TalentScout)

## 🚀 Project Overview

The **Hiring_Assistant_Chatbot (TalentScout)** is an intelligent chatbot built to initially screen technology candidates. It simulates the role of a technical recruiter by collecting essential candidate details and generating technical questions based on the candidate’s tech stack. 

This assistant aims to streamline the hiring process by offering:
- Automated collection of candidate information.
- Dynamic generation of technical questions tailored to tech stacks.
- Context-aware and coherent multi-turn conversations.
- Secure storage of candidate responses.

---

## 🛠 Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/IbrahimParkar/Hiring_Assistant_Chatbot.git
cd Hiring_Assistant_Chatbot
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file and add your Hugging Face API key:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## Usage Guide

1. Launch the chatbot via Streamlit.
2. The chatbot will greet the candidate and ask for essential details after they start the interview:
   - Full Name
   - Email Address
   - Phone Number
   - Experience
   - Desired Position
   - Location
   - Tech Stack
3. After they accept the Privacy Notice. Based on thier Profile, the assistant will:
   - Generate 4 technical questions using the LLM.
   - Allow the candidate to answer them.
   - Log the entire interview history in the Profiles folder in JSON format.
4. End the conversation gracefully with closing remarks when.
5. Optional: Restart or exit anytime by typing an end keyword like `exit` or `quit`.

---

## Technical Details

- **Frontend:** Streamlit
- **Language Model APIs:** Hugging Face Inference API (Falcon-7B-Instruct for QG, BART for Summarization)
- **Libraries Used:**
  - `streamlit`, `requests`, `dotenv`, `pandas`, `re`, `json`, `datetime`, `os`
- **Architecture:**
  - Modular design with `utils.py`, `prompt.py`, and `app.py`
  - Prompts crafted for question generation, relevance checks, and fallback handling
  - Context maintained across turns using Streamlit's session state
- **Storage:** Candidate responses are logged locally in the Profiles folder.

---

## Prompt Design Strategy

Prompts are designed to guide the model effectively:

1. **Information Gathering:**
   - "What is your desired position?" → Stored for context.
2. **Tech Stack-Based Question Generation:**
   - Prompt instructs model to generate a question specifically for the provided tech stack and experience.
   - E.g., “Generate a Python + Django technical question for a backend developer.”
3. **Follow-Up Questioning:**
   - Follows up using previous Q&A and full profile to generate deeper, contextual queries.
4. **Fallback Relevance Checks:**
   - If the input is irrelevant to the asked question, logic detects and prompts the user to answer again.

---

## Challenges & Solutions

| Challenge | Solution |
|----------|----------|
| Integrating LLMs with reliable context management | Used prompt chaining and session state to maintain a coherent flow |
| Handling vague or off-topic responses | Implemented relevance prompts to evaluate answer validity |
| Generating high-quality tech questions dynamically | Used Falcon-7B-Instruct via Hugging Face for rich and accurate question generation |
| Ensuring a smooth Streamlit UI flow | Modularized input blocks, controlled session state resets, and streamlined user prompts |
| Data storage and privacy | Logged data locally only and followed best practices by not storing sensitive info online |

---

## Demo

- 🔗 [Demo Video Link (Loom)](https://loom.com/share/your-demo-url) *(Replace with your Loom link once recorded)*

---

## Folder Structure

```
TalentScout-Hiring-Assistant/
│
├── app.py                   # Main Streamlit app
├── prompt.py                # Prompt templates for LLM
├── utils.py                 # Helper functions (API calls, validation)
├── Profiles                 # Interview history log (generated)
├── requirements.txt         # Python dependencies
├── .env                     # Hugging Face API key
└── README.md                # Project documentation
```

---

## 📌 Author

Developed by **Ibrahim Parkar**  
📧 ibrahimparkar888@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ibrahim-parkar-8004b1212) | [GitHub](https://github.com/IbrahimParkar)

---

## 📄 License

This project is for educational/demo purposes only and is not intended for commercial deployment without proper data privacy & security measures.
