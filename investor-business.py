import streamlit as st
from bcommon import set_custom_css
from alraedah_investor import investor_main
from userapp import business_main, business_overview
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import ast
import random
import json

if 'main_step' not in st.session_state:
    st.session_state.main_step = 0

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header{visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def perform_logout():
    st.write("You have been logged out.")
    st.experimental_rerun
    borrower_flow()

def show_logout():
    st.markdown(
        """
        <style>
        .logout {
            background-color: #f44336;
            color: white;
            padding: 8px 20px;
            font-size: 16px;
            border: none;
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Logout", key="logout", on_click=perform_logout, help="Click to logout"):
        for key in st.session_state.keys():
            del st.session_state[key]

def check_investor_credentials(username, password, credentials_list):
    for cred in credentials_list:
        if (username, password) == (cred[0], cred[1]):
            st.session_state.investor_name = username
            st.session_state.investor_id = cred[2]
            return True
    else:
        st.error("Invalid Credentials, Please Try Again!!")

def check_business_credentials(username, password, credentials_list):
    for cred in credentials_list:
        if (username, password) == (cred[0], cred[1]):
            st.session_state.business_name = username
            st.session_state.business_id = cred[2]
            return True
    else:
        st.error("Invalid Credentials, Please Try Again!!")

def signin():
    set_custom_css()
    display_logo()
    user_type = st.session_state.user_type
    print(f"user type sigin: {user_type}")
    
    placeholder = st.empty()
    with placeholder.form("login"):
            st.markdown('<h2 class="creds">Enter your credentials</h2>', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

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

            if submit_button:
                GDRIVE_CREDS = {
                    "type": "service_account",
                    "project_id": "st-project-387317",
                    "private_key_id": "e5778cc6315dac8480eb841efa093147fa47d996",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwK8/wpxa4JRWx\n7KfObiLoebmjLrAjYpv8E+3yTHqp3X+p/xBgQYrics//LCX8sXsFG77dW4vLib0V\nw2U4uygIvi2juzQKGUpDlb9aZ2jKexuToX+UZoa+RUxZICX+J0oDylK3vqcfsPAD\nhivGzveZSmW9cuuop1PMT/nl9vjEzUjcP3YrCcoMdRCUyVj21u3Vy6Qy0zkZU+iv\nZUfQo4kqDQuQU3qSrgvHrzx/zxhLcHvYXKXcaz31Llbd9kyKo35zaq8XnNOAczpn\ncVmeFbxkcrYfu8JtyIv97lOgTHsuxIDauJ8of5I+3Ng+wMW8uo7z8KawBM8a/YFA\nQzVBP0YLAgMBAAECggEAO4oDE90Uk5WM+H331I9qYtFIyPqtcrgP6ai+oUXxqtj+\nHXDjkvRzwMZ2v1GnYPiGkBppbhxTaa2aZvGLkxnFlPbZK93H36XecGr6qc4LH2tt\nzX4mRPxFi6aWAAUacgPLQu6s+AaKKu68nyRIRT+LdJYtPlLJjE1Ix+M7nNnUB4ad\nsJgG0KiMJib4q721VoEpQCfzgNsKN2TX0pJovokNv8slULMKouul94bSfRn7WeEo\nSyVceewz2JNMmym529bcnrdkSWujLEzXrA5V8GFaNgUcc+oSDlm7maPu9uSMFTv/\nceXgCKikYqik5XOFXjy4xpOnTII9cMUi8nkEWox+AQKBgQDkGBQ0AO1WOWylNCmH\n0Wk53m8701JSOsigG3ZXz7sQYa9rL57bkAk+T4oKL4AS2F14ARo672G2jlga8MY+\nGwBII8eStqtvBgpbfFR458rQT9QmeN59xExHxlDQHq6x9BV27cBb4fr6i9+YnGG0\nGwL3FWx09BSlPgGKIHK8xITJCwKBgQDFuYEPmf08fNq7fWZHqQvU++ma7iuUSCNW\n0v3YAnWO3EIm0rvFjpXzp7t8crkkcywj6TmFtttMm7mXT5nY53C4nDiLl72d8hfr\nFCTXY1NLgucj9AsM1OZnqV0g0FgXUXPFyr4acjYT990Qf9HF/KHLZztkLuxci5jb\np7zht4+XAQKBgQCOBiw2QUmGwdTTfQpLBmqV3Nm4D5oXl4CqqM7kWHVq+thGTm2E\n20fWI6KZOwBtO4nfmhgiEEHwcOuNQtS9gQSI5rZytQlD5Sf31Q+oBPQ1By/bELHA\n78RrgKF7JU+zgH8JAXsf+zLSZNvB48W2ZodPIGja3cwpI9XDkva+cUMZBwKBgDPB\nqjHuSiaCPDNl0NcjPfCjfHPMsmWfOHjqw/2+Lw2VRE+rS/GbsE7WcjJSSXpsF3rS\n+vawddkozjz4Xjoz4wLACeEoeD8W9wHXBQnIey5B9sUnhZj3RdSOtcz4HIcGEDsP\nJhIAIX26nQhLnRqpVaTLwfUof0B+XiXpU3z2MsUBAoGBAME1VwH07HSFjsjRKK+C\n/GphuvXBpBED1hGX7YIE4mF3HCVM8WilvW+2c5cxOnIPEL/M5W69h8Wl5okojpNQ\ngQiXCEd4PAnRNUeAw7fGq9jnl0ax/wmLIXnDl3czojhpKmrKg5cNhRQw0OYjEZrG\nmAO3VDeMT0xk9E1SoTMqTiEO\n-----END PRIVATE KEY-----\n",
                    "client_email": "collection-app@st-project-387317.iam.gserviceaccount.com",
                    "client_id": "116665121729126589127",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/collection-app%40st-project-387317.iam.gserviceaccount.com",
                    "universe_domain": "googleapis.com"
                    }

                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
                creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, scope)
                client = gspread.authorize(creds)

                if user_type == 'investor':
                    investor_sheet = client.open("streamlit_data").worksheet('investor_details')
                    data = investor_sheet.get_all_records()
                    investor_data = pd.DataFrame(data)

                    st.session_state.investor_data = investor_data

                    i_credentials_list = []
                    for row in investor_data.iterrows():
                        investor_login_dict = ast.literal_eval(row[1]['investor_reg_login'])
                        investor_id = row[1]['investor_id']
                        i_credentials_list.append((investor_login_dict['investor_name'], investor_login_dict['password'], investor_id))

                    print(i_credentials_list)

                    if check_investor_credentials(username, password, i_credentials_list):
                        st.session_state.main_step = 2
                        st.experimental_rerun()
                        print(f"main session state: {st.session_state.main_step}")
                
                elif user_type == 'business':
                    business_sheet = client.open("streamlit_data").worksheet('Business_details')
                    data = business_sheet.get_all_records()
                    business_data = pd.DataFrame(data)

                    st.session_state.business_data = business_data

                    b_credentials_list = []
                    for row in business_data.iterrows():
                        business_login_dict = ast.literal_eval(row[1]['business_reg_login'])
                        business_id = row[1]['Business_id']
                        b_credentials_list.append((business_login_dict['business_name'], business_login_dict['password'], business_id))

                    print(b_credentials_list)

                    if check_business_credentials(username, password, b_credentials_list):
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

def display_logo():
    logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
    st.markdown(
        f"""
        <style>
        .center-image {{
            display: flex;
            justify-content: center;
        }}
        </style>
        <div class="center-image">
            <img src="{logo_url}" width="100" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

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
        justify-content: center;
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

    st.markdown('<h5 class="create_account_terms">By continuing, you agree with our Terms & Conditions.</h5>',unsafe_allow_html=True)
    continue_btn = st.button("Continue")

    if continue_btn and name and email and full_phone_number and password:
        if user_type=='business':
            reg_login_details_dict = {
                'business_name': name,
                'email': email,
                'phone': full_phone_number,
                'password': password,
            }

            st.session_state.reg_login_details = reg_login_details_dict
            st.session_state.main_step = 4
            st.experimental_rerun()

        if user_type=='investor':
            GDRIVE_CREDS = {
                "type": "service_account",
                "project_id": "st-project-387317",
                "private_key_id": "e5778cc6315dac8480eb841efa093147fa47d996",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwK8/wpxa4JRWx\n7KfObiLoebmjLrAjYpv8E+3yTHqp3X+p/xBgQYrics//LCX8sXsFG77dW4vLib0V\nw2U4uygIvi2juzQKGUpDlb9aZ2jKexuToX+UZoa+RUxZICX+J0oDylK3vqcfsPAD\nhivGzveZSmW9cuuop1PMT/nl9vjEzUjcP3YrCcoMdRCUyVj21u3Vy6Qy0zkZU+iv\nZUfQo4kqDQuQU3qSrgvHrzx/zxhLcHvYXKXcaz31Llbd9kyKo35zaq8XnNOAczpn\ncVmeFbxkcrYfu8JtyIv97lOgTHsuxIDauJ8of5I+3Ng+wMW8uo7z8KawBM8a/YFA\nQzVBP0YLAgMBAAECggEAO4oDE90Uk5WM+H331I9qYtFIyPqtcrgP6ai+oUXxqtj+\nHXDjkvRzwMZ2v1GnYPiGkBppbhxTaa2aZvGLkxnFlPbZK93H36XecGr6qc4LH2tt\nzX4mRPxFi6aWAAUacgPLQu6s+AaKKu68nyRIRT+LdJYtPlLJjE1Ix+M7nNnUB4ad\nsJgG0KiMJib4q721VoEpQCfzgNsKN2TX0pJovokNv8slULMKouul94bSfRn7WeEo\nSyVceewz2JNMmym529bcnrdkSWujLEzXrA5V8GFaNgUcc+oSDlm7maPu9uSMFTv/\nceXgCKikYqik5XOFXjy4xpOnTII9cMUi8nkEWox+AQKBgQDkGBQ0AO1WOWylNCmH\n0Wk53m8701JSOsigG3ZXz7sQYa9rL57bkAk+T4oKL4AS2F14ARo672G2jlga8MY+\nGwBII8eStqtvBgpbfFR458rQT9QmeN59xExHxlDQHq6x9BV27cBb4fr6i9+YnGG0\nGwL3FWx09BSlPgGKIHK8xITJCwKBgQDFuYEPmf08fNq7fWZHqQvU++ma7iuUSCNW\n0v3YAnWO3EIm0rvFjpXzp7t8crkkcywj6TmFtttMm7mXT5nY53C4nDiLl72d8hfr\nFCTXY1NLgucj9AsM1OZnqV0g0FgXUXPFyr4acjYT990Qf9HF/KHLZztkLuxci5jb\np7zht4+XAQKBgQCOBiw2QUmGwdTTfQpLBmqV3Nm4D5oXl4CqqM7kWHVq+thGTm2E\n20fWI6KZOwBtO4nfmhgiEEHwcOuNQtS9gQSI5rZytQlD5Sf31Q+oBPQ1By/bELHA\n78RrgKF7JU+zgH8JAXsf+zLSZNvB48W2ZodPIGja3cwpI9XDkva+cUMZBwKBgDPB\nqjHuSiaCPDNl0NcjPfCjfHPMsmWfOHjqw/2+Lw2VRE+rS/GbsE7WcjJSSXpsF3rS\n+vawddkozjz4Xjoz4wLACeEoeD8W9wHXBQnIey5B9sUnhZj3RdSOtcz4HIcGEDsP\nJhIAIX26nQhLnRqpVaTLwfUof0B+XiXpU3z2MsUBAoGBAME1VwH07HSFjsjRKK+C\n/GphuvXBpBED1hGX7YIE4mF3HCVM8WilvW+2c5cxOnIPEL/M5W69h8Wl5okojpNQ\ngQiXCEd4PAnRNUeAw7fGq9jnl0ax/wmLIXnDl3czojhpKmrKg5cNhRQw0OYjEZrG\nmAO3VDeMT0xk9E1SoTMqTiEO\n-----END PRIVATE KEY-----\n",
                "client_email": "collection-app@st-project-387317.iam.gserviceaccount.com",
                "client_id": "116665121729126589127",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/collection-app%40st-project-387317.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
                }

            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(GDRIVE_CREDS, scope)
            client = gspread.authorize(creds)
            investor_sheet = client.open("streamlit_data").worksheet('investor_details')
            data = investor_sheet.get_all_records()
            investor_data = pd.DataFrame(data)

            n = 6
            investor_id = ''.join(["{}".format(random.randint(1, 9)) for num in range(0, n)])

            st.session_state.investor_id = str(investor_id)
            st.session_state.investor_name = name
    
            investor_reg_login_details_dict = {
                'investor_name': name,
                'email': email,
                'phone': full_phone_number,
                'password': password,
            }

            details_dict = {
                "name": name, 
                "available_cash": "10000", 
                "committed_cash": "0", 
                "oustanding_principal": "0", 
                "account_value": "10000", 
                "interest_received": "0", 
                "Annual_returns": "0", 
                "invested_amount": "0"
            }

            new_row = {
                "investor_id": str(investor_id),
                "details_dict": json.dumps(details_dict),
                "notes_dict": json.dumps({}),
                "investor_reg_login": json.dumps(investor_reg_login_details_dict)
            }

            investor_sheet.append_row(list(new_row.values()), value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS', table_range="A1")
            
            new_investor_data = pd.DataFrame([new_row])
            merged_data = pd.concat([investor_data, new_investor_data], ignore_index = True)
            st.session_state.investor_data = merged_data

            st.session_state.reg_login_details = investor_reg_login_details_dict
            st.session_state.main_step = 2
            st.experimental_rerun()

    elif continue_btn and (not name or not email or not full_phone_number or not password):
        st.error("Please Complete All Details Before Submitting")

    st.markdown(f'<h4 class="account">Already have an account? <a href="#" onclick="signin()">Sign In</a></h4>', unsafe_allow_html=True)
 
def borrower_flow():
    display_logo()
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
        st.session_state.step_business = 0
        business_overview()
    elif st.session_state.main_step == 4:
        business_main()
    elif st.session_state.main_step == 10:
        create_account()
    