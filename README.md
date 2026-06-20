# banking-streamlit-dashboard
# 🏦 Simple Banking Dashboard

A polished, responsive, and secure banking web application built with Python, Streamlit, and SQLite3. This dashboard features a modern user interface styled with custom CSS and provides real-time banking simulations like account creation, secure deposits, PIN-authenticated withdrawals, and dynamic performance metrics.

---

## ✨ Features

* 📊 **Interactive Overview:** Real-time summary cards displaying active accounts, total bank assets, and the most recently generated account number.
* 💳 **Instant Account Creation:** Auto-generates random, unique 10-digit account numbers with mandatory secure 4-digit PIN setup.
* 💰 **Deposits & Withdrawals:** Smooth numerical financial transaction controls with automated balance updates and input validations.
* 🔒 **PIN Verification:** Core operations (withdrawals and balance inquiry) strictly require accurate 4-digit PIN checks.
* 🎨 **Premium UI/UX:** Custom-tailored dark/light linear gradients, soft shadow containers, modern input borders, and responsive layouts.
* 🚀 **Easter Egg:** Includes a playful "Antigravity Feature" launching Python's classic XKCD comic tribute.

---

## 🛠️ Tech Stack

* **Frontend UI:** Streamlit (Python-based framework) + Custom HTML/CSS injection
* **Database:** SQLite3 (Lightweight, serverless relational database)
* **Backend Logic:** Python 3.x (Utilizing `sqlite3`, `random`, `re`, and `os` modules)

---

## 📦 Project Structure

```text
Banking_streamlit/
│
├── .venv/                  # Python Virtual Environment
├── app.py                  # Main Streamlit application source code
├── bank.db                 # SQLite database file (auto-generated)
└── README.md               # Project documentation.
