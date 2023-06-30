import pyrebase
import streamlit as st
from datetime import datetime


def settings(db, user, storage):
# SETTINGS PAGE 
    # CHECK FOR IMAGE
    nImage = db.child(user['localId']).child("Image").get().val()    
    # IMAGE FOUND     
    if nImage is not None:
        # We plan to store all our image under the child image
        Image = db.child(user['localId']).child("Image").get()
        for img in Image.each():
            img_choice = img.val()
            #st.write(img_choice)
        st.image(img_choice)
        exp = st.expander('Change Bio and Image')  
        # User plan to change profile picture  
        with exp:
            newImgPath = st.text_input('Enter full path of your profile imgae')
            upload_new = st.button('Upload')
            if upload_new:
                uid = user['localId']
                fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
                db.child(user['localId']).child("Image").push(a_imgdata_url)
                st.success('Success!')           
    # IF THERE IS NO IMAGE
    else:    
        st.info("No profile picture yet")
        newImgPath = st.text_input('Enter full path of your profile image')
        upload_new = st.button('Upload')
        if upload_new:
            uid = user['localId']
            # Stored Initated Bucket in Firebase
            fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
            # Get the url for easy access
            a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
            # Put it in our real time database
            db.child(user['localId']).child("Image").push(a_imgdata_url)       


def home(db, user):
    st.subheader("Date")
    st.info(datetime)
    col1, col2 = st.columns(2)
    # col for Profile picture
    with col1:
        nImage = db.child(user['localId']).child("Image").get().val()         
        if nImage is not None:
            val = db.child(user['localId']).child("Image").get()
            for img in val.each():
                img_choice = img.val()
            st.image(img_choice,use_column_width=True)
        else:
            st.info("No profile picture yet. Go to Edit Profile and choose one!")
        
        post = st.text_input("Let's share my current mood as a post!",max_chars = 100)
        add_post = st.button('Share Posts')
    if add_post:   
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")              
        post = {'Post:' : post,
                'Timestamp' : dt_string}                           
        results = db.child(user['localId']).child("Posts").push(post)
        st.balloons()

    # This coloumn for the post Display
    with col2:
        
        all_posts = db.child(user['localId']).child("Posts").get()
        if all_posts.val() is not None:    
            for Posts in reversed(all_posts.each()):
                    #st.write(Posts.key()) # Morty
                    st.code(Posts.val(),language = '') 


def workplace(db):
    all_users = db.get()
    res = []
    # Store all the users handle name
    for users_handle in all_users.each():
        k = users_handle.val()["Handle"]
        res.append(k)
    # Total users
    nl = len(res)
    st.write('Total users here: '+ str(nl)) 
    
    # Allow the user to choose which other user he/she wants to see 
    choice = st.selectbox('My Collegues',res)
    push = st.button('Show Profile')
    
    # Show the choosen Profile
    if push:
        for users_handle in all_users.each():
            k = users_handle.val()["Handle"]
            # 
            if k == choice:
                lid = users_handle.val()["ID"]
                
                handlename = db.child(lid).child("Handle").get().val()             
                
                st.markdown(handlename, unsafe_allow_html=True)
                
                nImage = db.child(lid).child("Image").get().val()         
                if nImage is not None:
                    val = db.child(lid).child("Image").get()
                    for img in val.each():
                        img_choice = img.val()
                        st.image(img_choice)
                else:
                    st.info("No profile picture yet. Go to Edit Profile and choose one!")

                # All posts
                all_posts = db.child(lid).child("Posts").get()
                if all_posts.val() is not None:    
                    for Posts in reversed(all_posts.each()):
                        st.code(Posts.val(),language = '')
