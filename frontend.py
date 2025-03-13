import streamlit as st
import pandas as pd
from backend import register_user, search_books,login_user, login_admin, get_books, borrow_book, get_borrowed_books, return_book,get_all_users

st.set_page_config(page_title="Library Management", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None

st.sidebar.title("🔐 Authentication")

auth_choice = st.sidebar.radio("Select Role", ["User Login", "Admin Login", "Register User"])

if auth_choice == "Register User":
    st.sidebar.subheader("User Registration")
    new_name = st.sidebar.text_input("Full Name")
    new_email = st.sidebar.text_input("Email")
    new_password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Register"):
        msg = register_user(new_name, new_email, new_password)
        st.sidebar.success(msg)


elif auth_choice == "User Login":
    st.sidebar.subheader("User Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user_info = login_user(email, password)
        if user_info:
            st.session_state.logged_in = True
            st.session_state.user_id = user_info["user_id"]
            st.session_state.user_role = "user"
            st.sidebar.success(f"✅ Logged in as User ({email})")
        else:
            st.sidebar.error("❌ Invalid email or password!")

elif auth_choice == "Admin Login":
    st.sidebar.subheader("Admin Login")
    email = st.sidebar.text_input("Admin Email")
    password = st.sidebar.text_input("Admin Password", type="password")

    if st.sidebar.button("Login"):
        admin_info = login_admin(email, password)
        if admin_info:
            st.session_state.logged_in = True
            st.session_state.user_id = admin_info["admin_id"]
            st.session_state.user_role = "admin"
            st.sidebar.success(f"✅ Logged in as Admin ({email})")
        else:
            st.sidebar.error("❌ Invalid admin credentials!")

if st.session_state.logged_in:
    st.title("📚 Library Management System")

    if st.session_state.user_role == "admin":
        st.subheader("📌 Admin Panel")

        # 📌 Section 1: Show All Registered Users
        st.subheader("👥 Registered Users")
        users = get_all_users()  # Fetch all users

        if users:
            for user in users:
                user_id, name, email = user
                st.write(f"🔹 **{name}** | ✉️ {email}")
        else:
            st.info("No users registered yet.")

        # 📌 Section 2: Show Borrowed Books
        st.subheader("📖 Borrowed Books")
        borrowed_books = get_borrowed_books()

        if borrowed_books:
            for transaction in borrowed_books:
                transaction_id, user_name, book_title, borrow_date, book_id = transaction
                st.write(f"📖 **{book_title}** borrowed by **{user_name}** on {borrow_date}")
                if st.button(f"Return '{book_title}'", key=transaction_id):
                    msg = return_book(transaction_id, book_id)
                    st.success(msg)
                    st.rerun()
        else:
            st.info("No books are currently borrowed.")

    else:
        search_term = st.text_input("🔍 Search for a book by title, author, or genre:")
        if search_term:
            books = search_books(search_term)
            if books:
                df = pd.DataFrame(books, columns=["Book ID", "Title", "Author", "Genre", "Year", "Available"])
                st.dataframe(df)
            else:
                st.warning("No books found!")


        st.subheader("📖 Borrow a Book")
        books = get_books()
        for book in books:
            book_id, title, author, genre, year = book
            st.write(f"**{title}** by {author} ({year}) - *{genre}*")
            if st.button(f"Borrow '{title}'", key=book_id):
                msg = borrow_book(st.session_state.user_id, book_id)
                st.success(msg)
                st.rerun()

       
        



else:
    st.markdown(
        """
        <div style="text-align:center; padding:50px; background-color:#f4f4f4; border-radius:10px;">
            <h1 style="color:#2E3B55; font-size:48px;">📚 Jaipur Central Library 📚</h1>
            <h3 style="color:#555;">"A gateway to knowledge and wisdom"</h3>
            <p style="color:#777; font-size:18px;">
                Welcome to Jaipur Central Library. Explore thousands of books, borrow and return with ease. 
                Please log in to continue.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

