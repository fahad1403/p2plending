import streamlit as st
from bcommon import set_custom_css
from alraedah_investor import investor_main
from userapp import business_main, business_overview

if 'main_step' not in st.session_state:
    st.session_state.main_step = 0

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header{visibility:hidden;}
</style>
"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def check_business_credentials(username, password):
    return username == 'business' and password == 'new_business'

def check_investor_credentials(username, password):
    return username == 'investor' and password == 'new_investor'

def signin():
    set_custom_css()
    print(f"user type sigin: {st.session_state.user_type}")
    st.markdown('<h1 class="signin_title">Dear Alraedah company user, welcome to National Single Sign-On</h1>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .horizontal-bar {
        background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
        box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
        color: #ffffff;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="horizontal-bar">User name and password</div>
    """, unsafe_allow_html=True)
    st.markdown('<hr>',unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.form("login"):
            st.markdown('<h2 class="creds">Enter your credentials</h2>', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            # if username == 'business' and password == 'new_business':
            #     st.session_state.main_step = 3
            #     st.experimental_rerun()

            # elif username == 'investor' and password == 'new_investor':
            #     st.session_state.main_step = 2
            #     st.experimental_rerun()

            custom_css = """
            <style>
            .button-123 {
                background-color: #FF5733; /* Change the background color */
                color: white; /* Change the text color */
                border: none; /* Remove the border */
                padding: 10px 20px; /* Adjust padding as needed */
                border-radius: 5px; /* Add rounded corners */
            }
            </style>
            """
        
            st.markdown(custom_css, unsafe_allow_html=True)
            # st.markdown('<button class="Login">Login</button>', unsafe_allow_html=True)
            submit_button = st.form_submit_button("Login")
            if submit_button and check_investor_credentials(username, password):
                st.session_state.main_step = 2
                st.experimental_rerun()
                print(f"main session state: {st.session_state.main_step}")
            
            elif submit_button and check_business_credentials(username, password):
                st.session_state.main_step = 3
                st.experimental_rerun()
                print(f"main session state: {st.session_state.main_step}")

            col1, col2 = st.columns([2, 1])
            st.write('''<style>
                [data-testid="column"] {
                    width: calc(33.3333% - 1rem) !important;
                    flex: 1 1 calc(33.3333% - 1rem) !important;
                    min-width: calc(33% - 1rem) !important;
                }
                </style>''', unsafe_allow_html=True)
            
            # col1,col2=st.columns(2)
            with col1:
                # TODO: change this url
                # st.write("[Forgot Password](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
                # st.markdown('<button class="Forgot_button">Forgot Password</button>',unsafe_allow_html=True)
                
                forgot_btn = st.form_submit_button('Forgot Password')
                if forgot_btn:
                    st.session_state.main_step = 11
                    st.experimental_rerun()

            with col2:
                # st.markdown('<button class="New_account">New Account</button>',unsafe_allow_html=True)

                new_acc_btn = st.form_submit_button("New Account")
                if new_acc_btn:
                    st.session_state.main_step = 10
                    st.experimental_rerun()

            print(f"Session: {st.session_state.main_step}")

    st.markdown('<hr>',unsafe_allow_html=True)


def create_account():
    reg_login_details_dict = {}
    user_type = st.session_state.user_type
    set_custom_css()
    logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
    # st.markdown(custom_css, unsafe_allow_html=True)
  # Center the image dynamically based on screen width
    st.markdown(
    f"""
    <style>
    .center-image {{
        display: flex;
        justify-content: left;
    }}
    </style>
    <div class="center-image">
        <img src="{logo_url}" width="100" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown('<h3 class="create_account_title">Create an account</h3>',unsafe_allow_html=True)
    if user_type == 'business':
        st.markdown('<h5 class="create_account_description">Enter your details and Start applying for Loan</h5>',unsafe_allow_html=True)
        name=st.text_input("Business Name",placeholder="Enter the name of your Business")

    elif user_type == 'investor':
        st.markdown('<h5 class="create_account_description">Enter your details and Start investing into Businesses</h5>',unsafe_allow_html=True)
        name=st.text_input("Name",placeholder="Enter your name")
    
    email=st.text_input("Email",placeholder="Enter your email")
    default_country_code = "+966"
    col1, col2 = st.columns([1,1])

    country_code = col1.selectbox("Country Code", ["+1", "+44", "+966", "+971", "+91"], index=2)

    phone_number = col2.text_input("Phone Number", placeholder="Enter your phone number")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    full_phone_number = f"{country_code} {phone_number}"

    reg_login_details_dict = {
        'business_name': name,
        'email': email,
        'phone': full_phone_number,
        'password': password,
    }

    st.session_state.reg_login_details = reg_login_details_dict

    st.markdown('<h5 class="create_account_terms">By continuing, you agree with our Terms & Conditions.</h5>',unsafe_allow_html=True)
    continue_btn = st.button("Continue")
    if continue_btn and user_type=='business':
        st.session_state.main_step = 4
        st.experimental_rerun()
    if continue_btn and user_type=='investor':
        st.session_state.main_step = 2
        st.experimental_rerun()

    st.markdown('<h4 class="account">Already have an account? <a href="YOUR_SIGNIN_PAGE_URL">Sign In</a></h4>', unsafe_allow_html=True)
    
# def Otp_page():
#     set_custom_css()
#     logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
#     # st.markdown(custom_css, unsafe_allow_html=True)
#   # Center the image dynamically based on screen width
#     st.markdown(
#     f"""
#     <style>
#     .center-image {{
#         display: flex;
#         justify-content: left;
#     }}
#     </style>
#     <div class="center-image">
#         <img src="{logo_url}" width="120" margin-bottom="30px" alt="Logo">
#     </div>
#     """,
#     unsafe_allow_html=True
# )
#     st.markdown('<h3 class="otp_header">Enter OTP</h3>',unsafe_allow_html=True)
#     # st.markdown(f'<h3 class="otp_description">Please enter the verification code we just sent to phone number{full_phone_number}</h3>',unsafe_allow_html=True)
#     st.markdown(f'<h3 class="otp_description">Please enter the verification code we just sent to phone number +966 503261064</h3>',unsafe_allow_html=True)
#     st.button("Verify") 

# def review_details():
#     set_custom_css()
#     logo_url = 'https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'

#     # Center the image dynamically based on screen width
#     st.markdown(
#         f"""
#         <style>
#         .center-image {{
#             display: flex;
#             justify-content: left;
#         }}
#         </style>
#         <div class="center-image">
#             <img src="{logo_url}" width="120" margin-bottom="30px" alt="Logo">
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#       # Key-value pairs to display
#      # Center the image dynamically based on screen width
#     st.markdown(
#         f"""
#         <style>
#         .details-item {{
#             display: flex;
#             flex-direction: column;
#             # margin-bottom: 2px;  /* Reduce the margin to reduce spacing */
#         }}
#         .Review_Keys {{
#             color: #717171;
#             font-family: Open Sans;
#             font-size: 12px;
#             font-style: normal;
#             font-weight: 400;
#             line-height: normal;
#         }}
#         .Review_Values {{
#             color: #000;
#             font-family: Open Sans;
#             font-size: 14px;
#             font-style: normal;
#             font-weight: 600;
#             line-height: normal;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown('<h3 class="review_details_header">Review details</h3>', unsafe_allow_html=True)
#     st.markdown('<h5 class="review_details_description">Please review and confirm your details to proceed</h5>', unsafe_allow_html=True)

#     # Key-value pairs to display
#     details = {
#         "Full Name": "Nur Ahmed",
#         "Phone number": "+966 55 675 8949",
#         "Employer": "NymCard",
#         "Employment title": "Manager",
#         "Salary": "SAR 30,000",
#         "Simah Score": "720",
#         "ID Number": "************",
#     }

#     # Display additional details with labels and values using a for loop
#     for key, value in details.items():
#         st.markdown(f'<div class="details-item">', unsafe_allow_html=True)
#         st.markdown(f'<h5 class="Review_Keys">{key}</h5>', unsafe_allow_html=True)
#         st.markdown(f'<h5 class="Review_Values">{value}</h5>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#     st.markdown('<button class="Review_Confirm">Confirm</button>', unsafe_allow_html=True)

def borrower_flow():
    set_custom_css()
    st.markdown('<h1 class="title">Welcome to Alraedah</h1>',unsafe_allow_html=True)

    # Apply CSS to create a blue background with white text
    st.markdown(
        """
        <style>
        body {
            background-color: #0074cc;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h4 class="borrower_description">Were here to help you achieve your financial goals and make lending and borrowing a seamless experience.</h4>',unsafe_allow_html=True)

    st.write("Please Select:")
    # Create a horizontal bar for "Sign In" and "Sign Up" buttons
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.empty()  # Create an empty column for spacing

    with col2:
        investor_button=st.button("I'm an Investor")
        borrower_button=st.button("I'm a Business")

        if investor_button:
            st.session_state.user_type = 'investor'
            st.session_state.main_step = 1
            st.session_state.login_page = True
            st.session_state.next_button_enabled = True
            st.experimental_rerun()
            # signin()
        elif borrower_button:
            st.session_state.user_type = 'business'
            st.session_state.main_step = 1
            st.session_state.login_page = True
            st.session_state.next_button_enabled = True
            st.experimental_rerun()

    with col3:
        st.empty()    

    if st.session_state.get("next_button_enabled"):
        if st.button("Next"):
            print(f"step: {st.session_state.main_step}")
        
def investor_signup():
    st.title("Investor Sign Up")
    st.image("investor_icon.png", use_column_width=True)
    st.write("Add your National ID/Iqama number")
    st.write("We need you to enter your National ID/Iqama number to verify your identity. You will only do this once.")
    if st.button("Add National ID/Iqama number"):
        pass
        # Add your code for handling National ID/Iqama number input here

def borrower_signup():
    set_custom_css()
    logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
    # st.markdown(custom_css, unsafe_allow_html=True)
  # Center the image dynamically based on screen width
    st.markdown(
    f"""
    <style>
    .center-image {{
        display: flex;
        justify-content: left;
    }}
    </style>
    <div class="center-image">
        <img src="{logo_url}" width="100" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown('<h4 class="borrowers_title">Borrower Sign Up</h4>',unsafe_allow_html=True)
    st.markdown('<h4 class="borrowers_description">Add your National ID/Iqama number</h4>',unsafe_allow_html=True)
    st.markdown('<h4 class="borrowers_small_description">We need you to enter your National ID/Iqama number to verify your identity. You will only do this once.</h4>',unsafe_allow_html=True)
    st.markdown('<button class="Iqama_button">Add National ID/Iqama number</button>', unsafe_allow_html=True)
   

if __name__ == "__main__":
    if 'login_page' not in st.session_state:
        borrower_flow()
    elif st.session_state.main_step == 1:
        signin()
    elif st.session_state.main_step == 2:
        investor_main()
    elif st.session_state.main_step == 3:
        business_overview()
    elif st.session_state.main_step == 4:
        business_main()
    elif st.session_state.main_step == 10:
        create_account()
    