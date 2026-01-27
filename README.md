# Employee Self-Service (ESS) AI Chatbot

A modern AI-powered Employee Self-Service chatbot system that uses natural language processing to understand employee queries and provide relevant information about HR policies, benefits, leave, attendance, and more.

## 🎯 Features

### Core Functionality
- **AI-Based Intent Detection** - Uses sentence transformers for semantic understanding
- **Entity Extraction** - Extracts dates, leave duration, and leave types from queries
- **Authentication** - Employee login with session management
- **Permission Control** - Private queries require authentication
- **Business Logic Handler** - Responds based on intent with actual employee data
- **Streamlit UI** - User-friendly chat interface

### Intents Supported

#### General Queries (No Login Required)
1. **Leave Policy** - Information about leave types and duration
2. **Company Holidays** - List of company holidays
3. **HR Contact** - HR phone and email information
4. **Company Info** - Company mission and background
5. **Benefits** - Employee benefits information

#### Employee-Specific Queries (Login Required)
1. **Leave Balance** - Check remaining leaves
2. **My Manager** - Find out your reporting manager
3. **My Department** - View your department
4. **My Attendance** - Check attendance record
5. **Apply for Leave** - Submit leave request
6. **Salary Info** - View salary details

## 📁 Project Structure

```
ess-new/
├── app.py                      # Streamlit UI application with profile management
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART.md               # Quick start guide
├── test_*.py                   # Test files for different components
├── config/
│   └── intents.json           # Intent definitions with examples (25+ intents)
├── data/
│   ├── employees.json         # Mock employee database
│   └── profile_manager.py     # Profile update functionality
├── src/
│   ├── __init__.py
│   ├── auth.py                # Authentication manager
│   ├── chatbot.py             # Main chatbot orchestrator
│   ├── intent_detector.py     # Semantic intent detection using embeddings
│   ├── embedding_utils.py     # Sentence-transformer embeddings
│   ├── similarity.py          # Cosine similarity calculations
│   ├── entity_extractor.py    # Entity extraction from queries
│   ├── business_logic.py      # Business logic handlers
│   ├── response_generator.py  # LLM response generation
│   └── phone_validator.py     # Phone number validation
└── venv/                       # Python virtual environment
```

## 🚀 Quick Start

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the Application
```bash
streamlit run app.py
```

The chatbot will open in your browser at `http://localhost:8501`

## 🔐 Demo Login Credentials

| Employee ID | Password | Name | Department |
|---|---|---|---|
| E001 | pass123 | Alice Johnson | Engineering |
| E002 | pass456 | Bob Smith | Engineering |
| E003 | pass789 | Carol White | HR |
| E004 | pass000 | David Brown | Management |
| E005 | pass111 | Emma Davis | Sales |

## 💬 Example Queries

### General Queries (No Login)
- "What is the leave policy?"
- "When are the company holidays?"
- "How do I contact HR?"
- "Tell me about the company"
- "What benefits are available?"
- "Hello" / "Hi there"

### Employee-Specific Queries (After Login)

**Leave Management:**
- "How many leaves do I have?" / "What is my leave balance?"
- "Am I applicable to take sick leave?"
- "Show my leave history for this year"
- "Has my leave been approved?"
- "I want to apply for leave on January 15 for 3 days"

**Personal Information:**
- "Who is my manager?"
- "What is my department?"
- "What is my attendance record?"
- "Show my birthday / work anniversary"
- "What are my skills?"

**Payroll & Career:**
- "What is my salary?" / "Show my payslip"
- "Show my tax calculation for 2025"
- "When is the appraisal cycle?"
- "Show my goals and objectives"

**Profile Updates:**
- "Update my phone number"
- "Change my emergency contact"

## 🔧 How It Works

### 1. Intent Detection
- User query is encoded using sentence-transformers
- Similarity is computed with intent embeddings
- Best matching intent is selected

### 2. Entity Extraction
- spaCy NLP extracts named entities
- Regex patterns extract dates and leave duration
- Structured data is prepared for business logic

### 3. Permission Check
- If intent is private, authentication is verified
- Unauthenticated users get login prompt

### 4. Business Logic
- Handler processes intent with user data
- Fetches information from mock database
- Computes results (e.g., leave balance)

### 5. Response Generation
- Structured response is formatted
- Natural language message is returned
- Chat history is maintained

## Email Configuration

This project uses SMTP for admin email notifications.

Before running:
1. Create a `.env` file
2. Copy values from `.env.example`
3. Use an app-specific SMTP password

## 📊 Architecture

```
User Query
    ↓
Intent Detection (Sentence Transformers)
    ↓
Entity Extraction (Regex Patterns)
    ↓
Permission Check (Auth Manager)
    ↓
Business Logic Handler
    ↓
Formatted Response
    ↓
Streamlit UI
```

## 🔨 Customization

### Add New Intent
1. Add entry to `config/intents.json`
2. Add handler method to `src/business_logic.py`
3. Add case in `src/chatbot.py` handle_intent()

### Add New Employee
1. Edit `data/employees.json`
2. Add employee record with all required fields

### Modify Leave Policy
1. Edit `_handle_leave_policy()` in `src/business_logic.py`
2. Update policy details as needed

## 🧪 Testing

### Test without Streamlit
```python
from src.chatbot import ESSChatbot

chatbot = ESSChatbot()

# Test general query
response = chatbot.process_message("What is the leave policy?")
print(response)

# Test login and employee query
chatbot.auth_manager.login("E001", "pass123")
response = chatbot.process_message("How many leaves do I have?")
print(response)
```

## 📝 Commands

Available in chat:
- `/login <employee_id> <password>` - Login
- `/logout` - Logout
- `/status` - Check login status
- `/help` - Show help message

## 🔄 Workflow Summary

1. **Step 1-2:** Environment setup ✅
   - Project folder created
   - Virtual environment configured
   - Dependencies installed

2. **Step 3-5:** Scope & Data ✅
   - Intents defined (6 general + 5 employee-specific)
   - Intent examples created (3-5 per intent)
   - Mock database with 5 employees

3. **Step 6-7:** Authentication & Intent Detection ✅
   - Login with employee ID/password
   - Session management
   - Semantic intent detection

4. **Step 8-9:** Entity Extraction & Permissions ✅
   - Extract dates, months, leave duration
   - Private intent authentication check
   - Permission-based access control

5. **Step 10-11:** Business Logic & UI ✅
   - Intent handlers for all intents
   - Leave balance, manager lookup, attendance
   - Streamlit chat interface

## 🎓 Learning Outcomes

This chatbot demonstrates:
- **NLP:** Sentence embeddings, semantic similarity
- **ML:** Cosine similarity for intent matching
- **Backend:** Authentication, business logic, data handling
- **Frontend:** Streamlit UI, session management
- **System Design:** Modular architecture, separation of concerns

## 📚 Technologies Used

- **NLP:** Sentence Transformers (all-mpnet-base-v2 model)
- **ML:** Cosine similarity calculations
- **Backend:** Python
- **UI:** Streamlit
- **Data:** JSON (mock HRMS)
- **Environment:** python-dotenv for configuration

## 🐛 Troubleshooting

### Streamlit not starting
```bash
pip install --upgrade streamlit
```

### Import errors
Ensure you're in the project root directory and the virtual environment is activated.

## 📈 Future Enhancements

- Integration with real HRMS databases
- LLM-based natural language response generation
- Multi-language support
- Conversation context management
- Employee feedback and ratings
- Analytics and reporting
- Slack/Teams integration

## 📄 License

This is a demo/educational project.

## 👨‍💼 Author

Created as a comprehensive ESS Chatbot solution demonstrating modern NLP and AI techniques.
