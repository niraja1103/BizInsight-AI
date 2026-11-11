# BizInsight AI 📊

An AI-powered Business Intelligence Dashboard that helps businesses understand their sales performance, analyze profits, and make smarter business decisions.

## 🚀 Features

- Upload sales data using CSV or Excel files.
- Automatically calculate total revenue, cost, profit, and profit margin.
- Analyze product-wise sales and profits.
- Interactive charts and visualizations.
- Identify best-selling products.
- Generate business recommendations.
- Ask business-related questions using the Gemini AI Advisor.
- Download analyzed data as a CSV file.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Google Gemini API
- OpenPyXL
- Python-dotenv

## 📂 Project Structure

```text
BizInsight-AI/
│
├── app.py
├── sample_sales.csv
├── requirements.txt
├── README.md
├── .gitignore
└── .env (not uploaded)
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/niraja1103/BizInsight-AI.git
```

### 2. Open the project folder

```bash
cd BizInsight-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini API

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own Gemini API key. Never share or upload this key.

### 7. Run the application

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## 📈 Project Goal

The goal of BizInsight AI is to simplify business data analysis by transforming sales data into meaningful insights and actionable recommendations.

## 👩‍💻 Developed By

**Niraja**

B.Tech – Computer Science and Engineering

---

*BizInsight AI – Turning Business Data into Smart Decisions.*