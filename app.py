import os
import streamlit as st
import sqlite3
import random
import string
import re


DB_PATH = os.path.join(os.path.dirname(__file__), "bank.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def init_db():
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    owner_name TEXT NOT NULL,
                    pin TEXT NOT NULL,
                    balance REAL NOT NULL
                )
                """
            )
    finally:
        conn.close()


def generate_account_number(length=10):
    conn = get_connection()
    try:
        while True:
            acct = "".join(random.choices(string.digits, k=length))
            cur = conn.execute("SELECT 1 FROM accounts WHERE account_number = ?", (acct,))
            if not cur.fetchone():
                return acct
    finally:
        conn.close()


def create_account(owner_name, pin, starting_balance=100.0):
    acct = generate_account_number()
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO accounts (account_number, owner_name, pin, balance) VALUES (?, ?, ?, ?)",
                (acct, owner_name, pin, starting_balance),
            )
        return acct
    finally:
        conn.close()


def get_account(account_number):
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT account_number, owner_name, pin, balance FROM accounts WHERE account_number = ?",
            (account_number,),
        )
        row = cur.fetchone()
        if row:
            return {
                "account_number": row[0],
                "owner_name": row[1],
                "pin": row[2],
                "balance": float(row[3]),
            }
        return None
    finally:
        conn.close()


def update_balance(account_number, new_balance):
    conn = get_connection()
    try:
        with conn:
            conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
    finally:
        conn.close()


def get_bank_metrics():
    conn = get_connection()
    try:
        cur = conn.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0) FROM accounts")
        row = cur.fetchone()
        return {
            "accounts": row[0],
            "total_balance": float(row[1] or 0.0),
        }
    finally:
        conn.close()


def apply_styles():
    st.markdown(
        """
        <style>
            body {
                background: #eef3f8;
            }
            .stApp {
                background: linear-gradient(180deg, #f7f9fb 0%, #eef3f8 45%, #ffffff 100%);
            }
            .block-container {
                padding-top: 2.5rem;
                padding-bottom: 2.5rem;
                padding-left: 2.5rem;
                padding-right: 2.5rem;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                box-shadow: 0 22px 55px rgba(15, 41, 78, 0.08);
            }
            .stSidebar {
                background: #f7fbff;
            }
            .css-18e3th9 {
                padding-top: 0 !important;
            }
            .stButton>button {
                border-radius: 12px;
                background: #2f5d9f;
                color: white;
                border: none;
                padding: 0.9rem 1.4rem;
                font-weight: 600;
                box-shadow: 0 12px 24px rgba(47, 93, 159, 0.12);
            }
            .stButton>button:hover {
                background: #244e88;
            }
            .stTextInput>div>div>input,
            .stTextInput>div>div>textarea,
            .stNumberInput>div>div>input {
                border-radius: 14px;
                border: 1px solid #dce6f3;
                padding: 0.95rem 1rem;
                background: #fbfdff;
                color: #1f3b5d;
            }
            .stTextInput>label,
            .stNumberInput>label {
                font-weight: 700;
                color: #1f3b5d;
            }
            .stAlert {
                border-radius: 14px;
            }
            .stMarkdown h1,
            .stMarkdown h2,
            .stMarkdown h3 {
                color: #1f3b5d;
            }
            .hero-panel {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 1.5rem;
                background: linear-gradient(120deg, #ffffff 0%, #f4f8fc 100%);
                border: 1px solid #dce7f0;
                border-radius: 24px;
                padding: 2rem;
                margin-bottom: 2rem;
            }
            .hero-copy {
                max-width: 680px;
            }
            .hero-copy h1 {
                margin-bottom: 0.5rem;
                font-size: 2.8rem;
                line-height: 1.05;
            }
            .hero-copy p {
                color: #4b627d;
                font-size: 1.05rem;
                line-height: 1.8;
            }
            .hero-badge {
                min-width: 210px;
                background: #ffffff;
                border: 1px solid #d5e1f0;
                border-radius: 20px;
                padding: 1.8rem;
                text-align: center;
                box-shadow: 0 16px 35px rgba(47, 93, 159, 0.08);
            }
            .hero-badge h2 {
                margin: 0;
                color: #2f5d9f;
                font-size: 2.6rem;
                line-height: 1;
            }
            .hero-badge span {
                color: #5b718f;
                font-size: 0.95rem;
            }
            .metric-card-row {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                margin-bottom: 1.5rem;
            }
            .metric-card {
                flex: 1 1 260px;
                min-width: 220px;
                background: #ffffff;
                border: 1px solid #dce7f0;
                border-radius: 18px;
                padding: 1.5rem;
                box-shadow: 0 12px 28px rgba(15, 41, 78, 0.06);
            }
            .metric-card h3 {
                margin-bottom: 0.75rem;
                color: #1f3b5d;
            }
            .metric-card p {
                margin: 0;
                font-size: 1.6rem;
                font-weight: 700;
                color: #244e88;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    st.sidebar.title("Banking Hub")
    st.sidebar.write("A polished finance demo for account creation, deposits, withdrawals, and balance checking.")
    st.sidebar.divider()
    st.sidebar.markdown(
        "**Quick tips:**\n\n- Use the exact account number shown after creation.\n- Deposit and withdraw values must be positive.\n- Balance checks require the 4-digit PIN."
    )
    st.sidebar.divider()
    st.sidebar.info("Built with Streamlit for a clean, professional banking dashboard.")


def main():
    st.set_page_config(page_title="Banking Dashboard", layout="wide", page_icon=":bank:")
    apply_styles()
    init_db()
    render_sidebar()

    if "last_created_account" not in st.session_state:
        st.session_state["last_created_account"] = ""

    st.title("Simple Banking Dashboard")
    st.markdown("Build reliable banking experiences with a clean interface, instant feedback, and polished form controls.")
    st.markdown(
        """
        <div class="hero-panel">
            <div class="hero-copy">
                <p class="eyebrow">Smart banking for modern teams</p>
                <h1>Manage accounts and money with clarity.</h1>
                <p>Clean workflows, fast updates, and a trusted dashboard experience for account creation, deposits, withdrawals, and balance monitoring.</p>
            </div>
            <div class="hero-badge">
                <h2>Ready to use</h2>
                <span>Designed for a professional banking demo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    menu = st.sidebar.selectbox(
        "Navigation",
        ["Overview", "Create Account", "Deposit", "Withdraw", "Check Balance", "Antigravity Feature"],
    )

    if menu == "Overview":
        metrics = get_bank_metrics()
        st.subheader("Dashboard Overview")
        st.markdown(
            f"""
            <div class="metric-card-row">
                <div class="metric-card"><h3>Active Accounts</h3><p>{metrics['accounts']}</p></div>
                <div class="metric-card"><h3>Total Balance</h3><p>${metrics['total_balance']:.2f}</p></div>
                <div class="metric-card"><h3>Last Created Account</h3><p>{st.session_state['last_created_account'] or 'None'}</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.write(
            "Use the navigation panel to create accounts, deposit funds, withdraw money, and verify balances with a secure PIN."
        )

    elif menu == "Create Account":
        st.subheader("Create a New Bank Account")
        with st.form("create_form"):
            name_col, pin_col = st.columns([3, 1], gap="medium")
            with name_col:
                name = st.text_input("Full name", placeholder="Enter your full name")
            with pin_col:
                pin = st.text_input("4-digit PIN", type="password", placeholder="1234")

            create_button = st.form_submit_button("Create Account")

        if create_button:
            if not name.strip():
                st.error("Please enter your full name.")
            elif not re.fullmatch(r"\d{4}", pin or ""):
                st.error("PIN must be exactly 4 digits.")
            else:
                try:
                    acct = create_account(name.strip(), pin)
                    st.success("Account created successfully.")
                    st.info("Your new account starts with $100.00.")
                    st.text_input("Account number", value=acct, disabled=True, key="new_acct")
                    st.session_state["last_created_account"] = acct
                except Exception as e:
                    st.error(f"Failed to create account: {e}")

    elif menu == "Deposit":
        st.subheader("Deposit Funds")
        default_acct = st.session_state.get("deposit_acct", st.session_state.get("last_created_account", ""))
        with st.form("deposit_form"):
            acct = st.text_input("Account number", key="deposit_acct", value=default_acct, placeholder="Enter account number")
            amt = st.number_input("Amount to deposit", min_value=1.0, step=1.0, format="%.2f")
            deposit_button = st.form_submit_button("Deposit")

        if deposit_button:
            if not acct.strip():
                st.error("Please enter an account number.")
            else:
                account = get_account(acct.strip())
                if not account:
                    st.error("Account not found.")
                else:
                    new_bal = account["balance"] + amt
                    update_balance(account["account_number"], new_bal)
                    st.success(f"Deposited ${amt:.2f}. New balance: ${new_bal:.2f}")

    elif menu == "Withdraw":
        st.subheader("Withdraw Funds")
        with st.form("withdraw_form"):
            acct = st.text_input("Account number", key="withdraw_acct", placeholder="Enter account number")
            pin = st.text_input("PIN", type="password", key="withdraw_pin", placeholder="1234")
            amt = st.number_input("Amount to withdraw", min_value=1.0, step=1.0, format="%.2f")
            withdraw_button = st.form_submit_button("Withdraw")

        if withdraw_button:
            if not acct.strip():
                st.error("Please enter an account number.")
            elif not re.fullmatch(r"\d{4}", pin or ""):
                st.error("Enter a valid 4-digit PIN.")
            else:
                account = get_account(acct.strip())
                if not account:
                    st.error("Account not found.")
                elif account["pin"] != pin:
                    st.error("Incorrect PIN.")
                elif amt > account["balance"]:
                    st.error("Insufficient funds.")
                else:
                    new_bal = account["balance"] - amt
                    update_balance(account["account_number"], new_bal)
                    st.success(f"Withdrew ${amt:.2f}. New balance: ${new_bal:.2f}")

    elif menu == "Check Balance":
        st.subheader("Check Account Balance")
        with st.form("check_form"):
            acct = st.text_input("Account number", key="check_acct", placeholder="Enter account number")
            pin = st.text_input("PIN", type="password", key="check_pin", placeholder="1234")
            check_button = st.form_submit_button("Check Balance")

        if check_button:
            if not acct.strip():
                st.error("Please enter an account number.")
            else:
                account = get_account(acct.strip())
                if not account:
                    st.error("Account not found.")
                elif not re.fullmatch(r"\d{4}", pin or ""):
                    st.error("Enter a valid 4-digit PIN.")
                elif account["pin"] != pin:
                    st.error("Incorrect PIN.")
                else:
                    st.success(f"Account owner: {account['owner_name']}")
                    st.info(f"Current balance: ${account['balance']:.2f}")

    elif menu == "Antigravity Feature":
        st.subheader("Antigravity Feature")
        st.write("A playful nod to Python's `antigravity` module.")
        if st.button("Lift Off 🚀"):
            try:
                import antigravity
                st.success("Opened antigravity (XKCD) — enjoy!")
            except Exception:
                st.markdown("[Open the XKCD Antigravity comic](https://xkcd.com/353/)")


if __name__ == "__main__":
    main()