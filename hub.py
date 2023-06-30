import pyrebase
import streamlit as st
from datetime import datetime
import pages
import requests
# Configuration Key
firebaseConfig = {
  'apiKey': "AIzaSyDUEY-XrqhXgMqPgFuJfTnjNaai3JgCwAM",
  'authDomain': "connect-it-c3162.firebaseapp.com",
  'projectId': "connect-it-c3162",
  'storageBucket': "connect-it-c3162.appspot.com",
  'databaseURL': "https://connect-it-c3162-default-rtdb.firebaseio.com/",
  'messagingSenderId': "837119462103",
  'appId': "1:837119462103:web:86b4c42f59f097e3587e92",
  'measurementId': "G-LRQQZPBQ6Z"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("Our community app")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password',type = 'password')
good = False

# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        try: 
            user = auth.create_user_with_email_and_password(email, password)
            st.success('Your account is created suceesfully!')
            st.balloons()
            # Sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome' + handle)
            st.info('Login via login drop down selection')
            
        except requests.exceptions.HTTPError:
            st.error("Please fill out the correct information")


# Login Block
if choice == 'Login':
    login = st.sidebar.button('Login')
    forgot_password = st.sidebar.button('Reset Pass')
    change_email = st.sidebar.button('Change Email')
    if login:
        try: 
            user = auth.sign_in_with_email_and_password(email,password)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            bio = st.radio('Jump to',['Home','Workplace Feeds', 'Settings'])
            good = True
        except requests.exceptions.HTTPError:
            st.error("Please fill out the correct information")


#',['Home','Workplace Feeds', 'Settings'
if good:
    if bio == 'Home':
        pages.home(db, user)
    if bio == 'Workplace Feeds':
        pages.workplace(db)
    if bio == 'Settings':
        pages.settings(db, user, storage)
    logout = st.sidebar.button('Logout')


