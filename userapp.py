import streamlit as st
from common_business import set_custom_css
from ekyb_flow import ekyb_main
from common_investor import set_custom_css_investor
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PIL import Image
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import json

def monthly_repayment_page():
    set_custom_css()
    loan_amount, term, rate = int(st.session_state.get('loan_amount_data')), int(st.session_state.get('term_data')), st.session_state.get('rate_data')
    rate = float(rate.split('%')[0])
    print(f"rate: {rate}")
    st.markdown('<h1 class="title">Monthly Repayment</h1>',unsafe_allow_html=True)
   
    monthly_payment = loan_amount / term
    st.markdown(
    f'<div style="text-align: center;">Monthly Repayment: <span style="font-weight: bold;">SAR {monthly_payment:.2f}</span></div>',
    unsafe_allow_html=True
)

    summary_card = st.empty()
    
    summary_data = {
    "Loan Amount": loan_amount,
    "Term": term,
    "Rate": rate,
    "Fees": loan_amount * (rate / 100),
    "Total Amount": loan_amount + (loan_amount * (rate / 100))
    }
    
    st.markdown(
            f"""
            <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                    <h3 style='font-size: 16px; color: gray; padding-left: 10px; padding-top: 20px; padding-bottom: 20px;'>Summary</h3>
                    <ul style='list-style-type:none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px; margin-left: 10px;'>{key}</li>" for key in summary_data.keys())}
                    </ul>
                </div>
                <div style='flex: 1; color: #6f8ec3; font-family: Arial'>
                    <h3 style='font-size: 16px; color: gray; margin-left: 80px; margin-top:13px;'>Details</h3>
                    <ul style='list-style-type:none; padding-right: -15px; font-size: 2px;'>
                        {''.join(f"<li style='font-size: 14px; margin-left: 80px;'>{value}</li>" for value in summary_data.values())}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.session_state.step_business += 1

    if st.button("Confirm Application", key="confirm_button"):
        print(st.session_state.step_business)

def add_repayment_method_page():
    repayment_dict = {}
    set_custom_css()
    st.markdown('<h1 class="title">Add Repayment Method</h1>',unsafe_allow_html=True)
    st.markdown('<span style="text-align:center;">We accept any debit/credit card</span>',unsafe_allow_html=True)
    with st.form("repayment_form"):
        card_number = st.text_input("Card Number", placeholder="0000 0000 0000 0000")
        exp_input = st.text_input("Expiration (MM//YY)",placeholder="MM/YY")
        cvv_input = st.text_input("CVV", placeholder="123", type="password")
        confirm = st.form_submit_button("Confirm Details")

        if confirm and card_number and exp_input and cvv_input:
            st.session_state.step_business += 1
            repayment_dict['card_number'] = card_number
            repayment_dict['expiration'] = exp_input
            repayment_dict['cvv'] = cvv_input
            st.session_state['gsheet_data']['repayment'] = repayment_dict
            print(f"\nUpdated dict: {st.session_state['gsheet_data']}")
            st.experimental_rerun()

        elif confirm and (not card_number or not exp_input or not cvv_input):
            st.error("Please Complete All Details Before Submitting")

def add_receive_funds_page():
    set_custom_css()
    st.markdown('<h1 class="title">How would you like to receive funds?</h1>',unsafe_allow_html=True)

   # Check the screen width to determine the layout
    if st.sidebar:
        # On wider screens, you can use a 2-column layout
        card1, card2 = st.columns([1,1])

        with card1:
            st.markdown(
                '<div style="background-color: #f2f2f2; padding: 5px; border-radius: 5px; text-align: center;margin-bottom:10px;justify-content: space-between; column-gap:5px">'
                # f'<img src="bank.png" width="30" alt="Bank account">'
                '<i class="fas fa-university fa-3x"></i>' 
                # <!-- Font Awesome bank icon -->'
                '<p><strong>Bank account</strong></p>'
                '<p>Get started</p>'
                '</div>',
                unsafe_allow_html=True
            )
            print('image is being load from card 1 make changes her')
            # Add vertical space between the columns
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        with card2:
            st.markdown(
                '<div style="background-color: #f2f2f2; padding: 5px; border-radius: 5px; text-align: center;margin-top:20px;justify-content: space-between; column-gap:5px">'
                '<i class="fas fa-credit-card fa-3x"></i>'
                '<p><strong>Virtual Card</strong></p>'
                '<p>Get started</p>'
                '</div>',
                unsafe_allow_html=True
            )
            print('image is being load from card 2 make changes her')
            st.session_state.step_business += 1
            if st.button("Add Bank Account"):
                # bank_account_details_page()
                print('add bank account button clicked')
    else:
        st.markdown(
            '<div style="background-color: #f2f2f2; padding: 10px; border-radius: 5px; text-align: center;">'
            f'<img src="bank.png" width="60" alt="Bank account">'
            '<p><strong>Bank account</strong></p>'
            '<p>Get started</p>'
            '</div>',
            unsafe_allow_html=True
        )
        print('image is being load from mobile screen make changes her')

        # st.image("atm-card.png", width=60)  # Replace "credit_card_logo.png" with the actual image URL

        st.markdown(
            '<div style="background-color: #f2f2f2; padding: 10px; border-radius: 5px; text-align: center;">'
             f'<img src="images/atm-card.png" width="60" alt="Bank account">'
            '<p><strong>Virtual Card</strong></p>'
            '<p>Get started</p>'
            '</div>',
            unsafe_allow_html=True
        )
        print('image is being load from mobile screen make changes her')
        if st.button("Add Bank Account"):
            bank_account_details_page()
            print('add bank account button clicked')

def save_data_to_sheet():
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
    sheet = client.open("streamlit_data").worksheet('Business_details')

    data = sheet.get_all_records()
    business_df = pd.DataFrame(data)

    n = 6
    business_id = ''.join(["{}".format(random.randint(1, 9)) for num in range(0, n)])
    new_row = {
        "Business_id": str(business_id),
        "business_details": json.dumps(st.session_state['gsheet_data']),
        "investor_investments": json.dumps({}),
        "business_reg_login": json.dumps(st.session_state['reg_login_details'])
    }

    print(f"final dict: {new_row}")

    new_row_df = pd.DataFrame(new_row, index=[0])

    new_data = pd.concat([new_row_df, business_df], ignore_index=True)
    updated_records = new_data.to_dict(orient='records')

    sheet.clear()
    sheet.update([new_data.columns.values.tolist()] + [[i for i in row.values()] for row in updated_records])

    # sheet.update([new_data.columns.values.tolist()] + new_data.values.tolist())

# Function to display bank account details page
def bank_account_details_page():
    receive_funds = {}
    set_custom_css()
    st.markdown('<h1 class="title">Bank Account Details</h1>',unsafe_allow_html=True)
    st.write("Please enter your bank account details")

    with st.form("bank_details_form"):
    # Create a form with text input fields
        bank_name = st.text_input("Bank Name", placeholder = "Al Rajhi")
        account_number = st.text_input("Account Number", placeholder = "0000 0000 0000 0000")
        iban = st.text_input("IBAN", placeholder = "GB29NWBK60161331926819")
        swift_code = st.text_input("Swift Code", placeholder = "CHASUS33")
        account_name = st.text_input("Account Name", placeholder = "John Doe")
        confirm = st.form_submit_button("Confirm Details")

        if confirm and bank_name and account_number and iban and swift_code and account_name:
            receive_funds['bank_name'] = bank_name
            receive_funds['account_no'] = account_number
            receive_funds['iban_no'] = iban
            receive_funds['swift_code'] = swift_code
            receive_funds['account_name'] = account_name
            st.session_state.step_business +=1
            print('Bank account added')
            st.session_state['gsheet_data']['bank_account'] = receive_funds
            save_data_to_sheet()
            st.experimental_rerun()

        elif confirm and (not bank_name or not account_number or not iban or not swift_code or not account_name):
            st.error("Please Complete All Details Before Submitting")
      
def consumer_page():
    st.session_state['gsheet_data'] = {}
    amount_details_dict = {}

    set_custom_css()
    st.markdown('<h1 class="title">Congratulations!</h1>',unsafe_allow_html=True)
    st.markdown('<span style="text-align:center;color:black;">You are preapproved for up to 35,000 SAR</span>',unsafe_allow_html=True)
    loan_amount = st.slider("Loan Amount (SAR)", 500, 35000, 500, 100, key="loan_amount")
    
    st.markdown(f'<span style="text-align:center;">Selected Loan Amount:</span> <span style="font-weight:bold;">{loan_amount} SAR</span>', unsafe_allow_html=True)

    term = st.slider("Term", min_value=12, max_value=36, step=6, format="%d months", key="term")
    
    st.markdown(f'<span style="text-align:center;">Selected Loan Term:</span> <span style="font-weight:bold;">{term} Months</span>', unsafe_allow_html=True)

    loan_purpose = st.selectbox("Loan Purpose", ["Business Expansion", "Other"])

    rate_card = st.empty()

    get_rate_button = st.button("Get Rate")

    accept_rate_button = None

    rate = '6.1%'
    if get_rate_button:
        rate_card.markdown(
            '<div style="background-color: #f2f2f2; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between;">'
            f'<div id="rate_text" style="font-size: 18px; font-weight: bold;">Rate: {rate}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.session_state.loan_amount_data = loan_amount
        st.session_state.term_data = term
        st.session_state.rate_data = rate

        if loan_amount and term:
            accept_rate_button = st.button("Accept Rate")
            amount_details_dict['business_name'] = 'Alraedah'
            amount_details_dict['loan_required'] = loan_amount
            amount_details_dict['term'] = term
            amount_details_dict['rate'] = rate
            amount_details_dict['repayment'] = {}
            amount_details_dict['bank_account'] = {}

            print(f"Amount details dict: {amount_details_dict}")

            st.session_state['gsheet_data'] = amount_details_dict

            st.session_state.step_business += 1

    if accept_rate_button:
        print(f"step: {st.session_state.step_business}")

def bank_account_added():
    print(f"Dictionary: {st.session_state['gsheet_data']}")

    logo_url='https://objectstorage.me-jeddah-1.oraclecloud.com/n/idcsprod/b/me-jeddah-idcs-1-9E6C09D36371AB1B7C12FA52FA120B95980D070A43765EF7F2A2F0B0F82948E6/o/images/202109131530/1631547034999/Alraedah-Logo-Landscape-2.jpg'
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
        <img src="{logo_url}" width="150" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

    # Center an image
    # image = st.image("right-tick.jpg", use_column_width=True)
    image=Image.open('images/right-tick.jpg')
    new_width=100
    new_height=100
    image=image.resize((new_width,new_height))
    st.image(image,use_column_width=True)
    centered_text = '''
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 10vh;">
        <span style="text-align: center; font-weight: bold;">Congratulations!</span>
        <span style="text-align: center;">Funds will be transferred to your bank account within 3-5 working days</span>
    </div>
    '''
    st.markdown(centered_text, unsafe_allow_html=True)

def business_overview():
    set_custom_css_investor()
    st.markdown('<h4 class="business_title">Welcome  Nymcard</h4>',unsafe_allow_html=True)
    st.markdown("<h5 style='color: #3498DB;'> Summary</h5>", unsafe_allow_html=True)
    notes_dict = {
                'Loan Applied': 10000,
                'Term':24,
                'Invesment Recieved': 8000,
                'Invesment Pending': 2000,
            }

    account_no = 12345

    card_container = st.container()

    with card_container:
        st.markdown(
            f"""
            <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                    <h3 style='font-size: 16px; color: gray; padding: -10px; font-weight:bold; margin-left:0px;'>My Account #{account_no}</h3>
                    <ul style='list-style-type:none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>{key}</li>" for key in notes_dict.keys())}
                    </ul>
                </div>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial'>
                    <h3 style='font-size: 16px; color: gray; margin-left: 70px; margin-top: 0px;'>Details</h3>
                    <ul style='list-style-type: none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px; margin-bottom: 7px; margin-left: 60px;'>{'SAR ' if key != 'Term' else ''}{value}{' Months' if key == 'Term' else ''}</li>" for key, value in notes_dict.items())}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.text("")
    active_product_summary_df = pd.DataFrame({
            "Loan ID": ["25732","25782","29012"],
            "Investor Name": ["Khalid Ghaifi","Markram","Starc"],
            "Investment Received": ["4000 SAR","2000 SAR","2000 SAR"],
            "Date Invested": ["16/9/2023","20/10/2023","14/10/2023"],
        })

    active_product_summary_df['Date Invested'] = pd.to_datetime(active_product_summary_df['Date Invested'], format='%d/%m/%Y')

    active_product_summary_df = active_product_summary_df.sort_values(by='Date Invested', ascending=False)

    active_product_summary_df = active_product_summary_df.reset_index(drop=True)

    with st.container():
        st.markdown("<h4 style='color: #3498DB;'>Loan Summary</h4>", unsafe_allow_html=True)
        st.dataframe(active_product_summary_df)
        # Iterate through the DataFrame rows and create expanders
        for index, row in active_product_summary_df.iterrows():
            loan_id = row["Loan ID"]
            investor_name = row["Investor Name"]
            investment_received = row["Investment Received"]
            date_invested = row["Date Invested"].strftime("%d/%m/%Y")

            terms = [12, 9, 6]

            with st.expander(f"Loan ID: {loan_id}"):
                investment_received = int(investment_received.replace(" SAR", "").replace(",", ""))
                term = terms[index]  # Get the corresponding term for this row
                monthly_payment = investment_received / term

                date_invested = datetime.strptime(date_invested, "%d/%m/%Y")
                expected_payment_dates = [date_invested + relativedelta(months=i) for i in range(term)]

                st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px; display: flex; margin-left:-40px;'>
                    <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                        <h3 style='font-size: 16px; color: gray; padding: -10px; font-weight:bold; margin-left:0px;'>Loan Details</h3>
                        <ul style='list-style-type:none; padding: 0;'>
                            <li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>Investor Name: {investor_name}</li>
                            <li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>Date Invested: {date_invested}</li>
                            <li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>Loan Received: {investment_received}</li>
                            <li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>Monthly Payment: SAR {monthly_payment:.2f}</li>
                            <li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>Loan Term: {term} months </li>
                        </ul>
                    </div>  
                </div>
                """,
                unsafe_allow_html=True,
            )

                st.text("")
                st.text("")

                st.markdown(
                    f"""
                    <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px; display: flex; margin-left:-40px;'>
                        <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                            <h3 style='font-size: 16px; color: gray; padding: -10px; font-weight:bold; margin-left:0px;'>Monthly Payment</h3>
                            <ul style='list-style-type:none; padding: 0;'>
                                <ul style='list-style-type:none; padding: 0;'>
                                {''.join(f"<li style='font-size: 14px; margin-bottom: 7px;'>SAR {monthly_payment:.2f}</li>" for _ in range(term))}
                            </ul>
                        </div>
                        <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                            <h3 style='font-size: 16px; color: gray; margin-left: 60px; margin-top: 0px; margin-bottom: 20px'>Due Date</h3>
                            <ul style='list-style-type:none; padding: 0;'>
                                {''.join(f"<li style='font-size: 14px; margin-bottom: 7px; margin-left: 60px;'>{date.strftime('%d/%m/%Y')}" for date in expected_payment_dates)}
                            </ul>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.text("")

def business_main():
    hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    if 'step_business' not in st.session_state:
        st.session_state.step_business = 1
    
    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step_business == 1:
        ekyb_main()
        # st.session_state.step_business += 1
    elif st.session_state.step_business == 2:
        consumer_page()
    elif st.session_state.step_business == 3:
        monthly_repayment_page()
    elif st.session_state.step_business == 4:
        add_repayment_method_page()
    elif st.session_state.step_business == 5:
        add_receive_funds_page()
    elif st.session_state.step_business == 6:
        bank_account_details_page()
    elif st.session_state.step_business == 7:
        bank_account_added()

if __name__=='__main__':
    business_main()
