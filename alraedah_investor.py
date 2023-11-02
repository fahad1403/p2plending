import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, ColumnsAutoSizeMode
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from streamlit_modal import Modal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from common_investor import set_custom_css_investor
import json
import random
from datetime import datetime
from bcommon import show_logout

st.set_page_config(layout="wide")
investor_account_df = {}
business_df = {}
investor_all_dicts = {}
notes_df = {}
notes_dict = {}
sheet = None
business_sheet = None

def summary():
    with st.spinner("Loading Summary"):
        global investor_account_df
        global business_df
        global investor_all_dicts
        global sheet
        global business_sheet
        global notes_df
        global notes_dict

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
        sheet = client.open("streamlit_data").worksheet('investor_details')

        # data = sheet.get_all_records()
        # df = pd.DataFrame(data)
        df = st.session_state.investor_data

        investor_id = st.session_state.investor_id
        investor_name = st.session_state.investor_name

        print(f"\n\ninvestor df: {df}\n\n")

        print(f"\n\ninvestor id: {investor_id}\n\n")

        investor = df[df['investor_id'] == investor_id]
        print(f"\n\ninvestor: {investor}\n\n")

        investor_data = df[df['investor_id'] == investor_id].iloc[0]
        details_dict_str = investor_data['details_dict']
        details_dict = json.loads(details_dict_str)
        investor_account_df = details_dict
        investor_all_dicts = investor_data

        notes_dict_str = investor_all_dicts['notes_dict']
        notes_dict = json.loads(notes_dict_str)
        notes_data = {
            'Loan Id': [note['loan_id'] for note in notes_dict.values()],
            'Note Id': list(notes_dict.keys()),
            'Paid Status': [note['status'] for note in notes_dict.values()]
        }

        notes_df = pd.DataFrame(notes_data)

        business_sheet = client.open("streamlit_data").worksheet('Business_details')
        business_data = business_sheet.get_all_records()
        business_df = pd.DataFrame(business_data)
        # business_df = st.session_state.business_data

        business_notes_dict = {
            'Available Cash': int(details_dict['available_cash']),
            'Committed Cash': int(details_dict['committed_cash']),
            'Outstanding Principal': int(details_dict['oustanding_principal']),
            'Account Value': int(details_dict['account_value']),
        }

        account_no = st.session_state.investor_id
        annualized_returns = int(details_dict['Annual_returns'])
        interest_received = int(details_dict['interest_received'])
        invested_amount = int(details_dict['invested_amount'])
        total = float(invested_amount) + float(interest_received)

        st.markdown(f'<h1 class="title" style="font-weight: lighter; font-size: 28px; margin-bottom: 10px;">Welcome {investor_name} !</h1>',unsafe_allow_html=True)

        card_container = st.container()

        with card_container:
            st.markdown(
                f"""
                <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                    <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                        <h3 style='font-size: 16px; color: gray; padding: -10px; font-weight:bold; margin-left:0px;'>My Account #{account_no}</h3>
                        <ul style='list-style-type:none; padding: 0;'>
                            {''.join(f"<li style='font-size: 14px;  margin-bottom: 7px; margin-left:5px;'>{key}</li>" for key in business_notes_dict.keys())}
                        </ul>
                    </div>
                    <div style='flex: 1; color: #4d8ec3; font-family: Arial'>
                        <h3 style='font-size: 16px; color: gray; padding-left: 18px; margin-top:0px;'>Details</h3>
                        <ul style='list-style-type:none; padding: 0;'>
                            {''.join(f"<li style='font-size: 14px;  margin-bottom: 7px; margin-left: 60px;'>SAR {value}</li>" for value in business_notes_dict.values())}
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.text("")
        
        account_val_card_container = st.container()
        with account_val_card_container:
            st.markdown(
                f"""
                <div style='background-color: #EAF1FA; padding: 10px; border-radius: 10px; display: flex;'>
                    <div style='flex: 1; color: #2A6FCA; font-family: Arial; font-size: 12px'>
                        <ul style='list-style-type:none; padding: 0;'>
                            <li style='font-size: 24px;  margin-bottom: 0px; padding: 0; font-weight:bold; margin-left:5px;'>SAR {business_notes_dict.get('Available Cash'):.2f}</li>
                            <li style='font-size: 14px;  margin-bottom: 8px; color: #000000; margin-left:0px;'>Adjusted Account Value</li>
                            <li style='font-size: 12px;  margin-bottom: 4px; color: #717171; margin-left:0px;'>Available cash: SAR {business_notes_dict.get('Available Cash')}</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.text("")

        returns_card_container = st.container()
        with returns_card_container:
            st.markdown(
                f"""
                <div style="width: 100%; height: 100%; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 8px; border: 1px #F2F0EB solid; flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 12px; display: inline-flex">
                    <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: flex">
                        <div style="text-align: center; color: #2A6FCA; font-size: 24px; font-family: Arial; font-weight: 700; word-wrap: break-word; margin-left:0px;">{annualized_returns}%</div>
                        <div style="width: 311px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-left:0px;">Adjusted Net Annualized Returns </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.text("")

        interest_received_container = st.container()
        with interest_received_container:
            st.markdown(
                f"""
                <div style="width: 100%; height: 100%; padding-left: 16px; padding-right: 16px; padding-top: 12px; padding-bottom: 12px; border-radius: 8px; border: 1px #F2F0EB solid; flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 16px; display: inline-flex">
                    <div style="padding-bottom: 12px; border-bottom: 1px #F2F0EB solid; flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 12px; display: flex">
                        <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: flex">
                            <div style="text-align: center; color: #2A6FCA; font-size: 24px; font-family: Arial; font-weight: 700; word-wrap: break-word; margin-left:0px;">SAR {interest_received:.2f}</div>
                            <div style="width: 311px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-left:0px;">Interest received</div>
                        </div>
                        <div style="width: 311px; justify-content: space-between; align-items: center; display: inline-flex">
                            <div style="width: 210px; height: 24px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-left:0px;">Total Payments (Principal + Interest):</div>
                            <div style="width: 83px; height: 24px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 600; word-wrap: break-word">SAR {total:.2f}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("My notes in a glance"):
                st.dataframe(notes_df)
            # with st.expander("Payments"):
            #     st.write("Details")


def portfolio_details():
    with st.spinner("Loading Details"):
        pie_chart = px.pie(
            values=[10, 20, 30, 20, 5, 15],
            names=[
                "Weighted Average Rate",
                "Accured Interest",
                "Payment to Date",
                "Principal",
                "Interest",
                "Late fees received"
            ],
            hole=0.4,
        )

        # Update the pie chart layout
        pie_chart.update_traces(marker=dict(colors=['rgba(126, 200, 227, 0.7)', 
                                                    'rgba(65, 134, 224, 0.7)', 
                                                    'rgba(44, 103, 184, 0.7)', 
                                                    'rgba(63, 63, 191, 0.7)', 
                                                    'rgba(83, 32, 126, 0.7)', 
                                                    'rgba(122, 59, 123, 0.7)']))

        pie_chart.update_layout(
            title_text="Composition (SAR)",
            title_x=0.3,
            title_y=0.95,
            font=dict(family="Arial", size=12),
            legend=dict(orientation="h"),
        )

        notes_dict = {
            'Not yet issued': 0,
            'Issued & Current': 0,
            'In grace period': 0,
            'Late 16-30 days': 0,
            'Late 31-120 days': 0,
            'Fully paid': 1878,
            'Default': 0
        }

        card_container = st.container()

        with card_container:
            st.markdown(
                f"""
                <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                    <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px; margin-left:-20px;'>
                        <h3 style='font-size: 16px; color: gray; padding: 20px; margin-left:-60px;'>STATUS</h3>
                        <ul style='list-style-type:none; padding: 0;'>
                            {''.join(f"<li style='font-size: 14px; margin-left:25px;'>{key}</li>" for key in notes_dict.keys())}
                        </ul>
                    </div>
                    <div style='flex: 1; color: #4d8ec3; font-family: Arial'; margin-right:-20px;>
                        <h3 style='font-size: 16px; color: gray; padding-left: 18px; margin-top:13px; margin-left:28px;'>PRINCIPAL</h3>
                        <ul style='list-style-type:none; padding-right: -15px; font-size: 2px;'>
                            {''.join(f"<li style='font-size: 14px; margin-left:70px;'>SAR {value:.2f}</li>" for value in notes_dict.values())}
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.text("")

        st.text("")
        st.plotly_chart(pie_chart, use_container_width=True)


def display_note_details(note_id, note_details):
    st.markdown(
        f"""
        <div style="width: 100%; height: 100%; padding-bottom: 12px; padding-left: 12px; padding-right: 12px; border-bottom: 1px #F2F0EB solid; justify-content: space-between; align-items: flex-start; display: inline-flex">
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Note ID</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">{note_id}</div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Portfolio</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">None</div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Investment</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">SAR {note_details.get("loan_amount")}</div>
            </div>
        </div>

        <div style="width: 100%; height: 100%; padding-bottom: 12px; padding-left: 12px; padding-right: 12px; border-bottom: 1px #F2F0EB solid; justify-content: space-between; align-items: flex-start; display: inline-flex">
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Interest rate</div>
                <div style="width: 95px; justify-content: flex-start; align-items: center; gap: 8px; display: inline-flex">
                    <div style="justify-content: flex-start; align-items: flex-start; gap: 8px; display: flex">
                        <div style="text-align: center; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">{int(note_details.get("interest")):.2f}%</div>
                    </div>
                </div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Term</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">{note_details.get("term")}</div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word">Outstanding Principal</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word">SAR 0</div>
            </div>
        </div>

        <div style="width: 100%; height: 100%; padding-bottom: 12px; padding-left: 12px; padding-right: 12px; border-bottom: 1px #F2F0EB solid; justify-content: space-between; align-items: flex-start; display: inline-flex">
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-bottom:4px;">Accrued <br/>Interest</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-bottom:8px;">SAR {note_details.get("interest")}</div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word; ">Payments received</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-bottom:8px;">SAR {note_details.get("payments_to_date")}</div>
            </div>
            <div style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 4px; display: inline-flex">
                <div style="width: 95px; height: 32px; color: #717171; font-size: 12px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-bottom:4px;">Payments <br/>due date</div>
                <div style="width: 95px; color: black; font-size: 14px; font-family: Arial; font-weight: 400; word-wrap: break-word; margin-bottom:-20px;">04/22/23</div>
            </div>
        </div>

        """,
        unsafe_allow_html=True,
    )

    note_details_dict_1 = {
        'Note issuance date': note_details.get("note_issue_date"),
        'Note amount': f'SAR {note_details.get("note_amount")}',
        'Loan amount': f'SAR {note_details.get("loan_amunt")}',
        'Rate': f'{note_details.get("interest")}%',
        'Term': note_details.get("term"),
        'Status': note_details.get("status"),
        'Recent credit score': note_details.get("simah_score"),
    }

    card_container_1 = st.container()

    with card_container_1:
        st.markdown(
            f"""
            <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px; margin-left:-20px;'>
                    <h3 style='font-size: 16px; color: gray; padding: 20px; margin-left:-30px;'>Loan Summary</h3>
                    <ul style='list-style-type:none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px; margin-left:25px; margin-bottom: 7px;'>{key}</li>" for key in note_details_dict_1.keys())}
                    </ul>
                </div>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial'; margin-right:-20px;>
                    <ul style='list-style-type:none; padding-right: -15px; font-size: 2px; margin-top:65px;'>
                        {''.join(f"<li style='font-size: 14px; margin-left:70px; margin-bottom: 7px;'>{value}</li>" for value in note_details_dict_1.values())}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.text("")

    st.text("")
    note_details_dict_2 = {
        'Last payment received': f'SAR {note_details.get("last_payment_received")}',
        'Payments to date': f'SAR {note_details.get("payments_to_date")}',
        'Principal': f'SAR {note_details.get("principal")}',
        'Rate': f"{note_details.get('interest')}%",
        'Late fees': f'SAR {note_details.get("late_fees")}',
    }

    card_container_2 = st.container()

    with card_container_2:
        st.markdown(
            f"""
            <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex;'>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px; margin-left:-20px;'>
                    <h3 style='font-size: 16px; color: gray; padding: 20px; margin-left:3.5px;'>Received Payments</h3>
                    <ul style='list-style-type:none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px; margin-left:25px; margin-bottom: 7px;'>{key}</li>" for key in note_details_dict_2.keys())}
                    </ul>
                </div>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial'; margin-right:-20px;>
                    <ul style='list-style-type:none; padding-right: -15px; font-size: 2px; margin-top:65px;'>
                        {''.join(f"<li style='font-size: 14px; margin-left:70px; margin-bottom: 7px;'>{value}</li>" for value in note_details_dict_2.values())}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def portfolio_notes():
    global notes_dict
    df = notes_df
    with st.spinner("Loading Details"):
        options_builder = GridOptionsBuilder.from_dataframe(df)
        options_builder.configure_column('Note Id')
        options_builder.configure_selection(selection_mode="single", use_checkbox=True)
        # options_builder.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
        grid_options = options_builder.build()
        
        grid = AgGrid(df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, gridOptions = grid_options, allow_unsafe_jscode=True, fit_columns_on_grid_load=True, theme='alpine')
        sel_row = grid["selected_rows"]
        modal = Modal(key="Portfolio_Modal",title="")
        if sel_row:
            selected_index = sel_row[0]['_selectedRowNodeInfo']['nodeRowIndex']
            note_id = sel_row[0]['Note Id']
            # st.write(f"<b>Status: </b>{sel_row[0]['Status']}",unsafe_allow_html=True)
            open_modal = st.button("View Details")
            if open_modal:
                modal.open()

            if modal.is_open():
                with modal.container():
                    st.text("")
                    st.text("")
                    display_note_details(note_id, notes_dict.get(note_id))

                    st.text("")

def portfolio_ps():
    global investor_account_df
    with st.spinner("Loading Portfolio"):
        data = {
            'Name': ['Consolidated'],
            'Investments': investor_account_df['invested_amount'],
            'Committed Cash': investor_account_df['committed_cash'],
        }

        df = pd.DataFrame(data)

        options_builder = GridOptionsBuilder.from_dataframe(df)
        # options_builder.configure_default_column(width=150, resizable=True)
        # options_builder.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
        grid_options = options_builder.build()

        grid = AgGrid(df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, gridOptions = grid_options, allow_unsafe_jscode=True, fit_columns_on_grid_load=True, theme='alpine')


def portfolio():
    tab1, tab2, tab3 = st.tabs(
        ["Details", "  Notes  ", "Portfolios"]
    )

    with tab1:
        portfolio_details()
    with tab2:
        portfolio_notes()
    with tab3:
        portfolio_ps()


def load_invest_details(name, rate, term, loan_required):
    st.markdown('<h3 style="text-align: center; font-weight: lighter">Invest</h3>', unsafe_allow_html=True)

    selected_amount = st.slider('Select Amount to Invest', 50, 10000, 50, 50)
    st.markdown(f'<h5 style="text-align: center; font-weight: lighter; font-size: 20px;">Selected amount: SAR {selected_amount}</h5>', unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('<h3 style="text-align: center;">Investment Details</h3>', unsafe_allow_html=True)
    
    # funded = 0
    # if selected_amount == 50:
    #     funded = "0%"
    # else:
    funded = f'{round((selected_amount/int(loan_required))*100,2)}%'

    summary_dict = {
        'Name': name,
        'Required Loan': loan_required,
        'Rate': rate,
        'Amount': selected_amount,
        'Term': term,
        "% Funded": funded,
    }

    st.markdown(
            f"""
            <div style='background-color: #f4f4f4; padding: 10px; border-radius: 10px; display: flex; margin-bottom: 20px;'>
                <div style='flex: 1; color: #4d8ec3; font-family: Arial; font-size: 12px'>
                    <h3 style='font-size: 16px; color: gray; padding-left: -10px; padding-top: 20px; padding-bottom: 20px;'>Summary</h3>
                    <ul style='list-style-type:none; padding: 0;'>
                        {''.join(f"<li style='font-size: 14px'>{key}</li>" for key in summary_dict.keys())}
                    </ul>
                </div>
                <div style='flex: 1; color: #6f8ec3; font-family: Arial'>
                    <h3 style='font-size: 16px; color: gray; padding-left: 18px; margin-top:13px;'>Details</h3>
                    <ul style='list-style-type:none; padding-right: -15px; font-size: 2px;'>
                        {''.join(f"<li style='font-size: 14px'>{value}</li>" for value in summary_dict.values())}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_amount, funded

def invest_in_business(investor_id, name, rate, term, selected_amount, required, funded, selected_index, modal):
    ## display congratulations screen
    ## use business details sheet and update the investment part
    ## update capital and investment for investor sheet
    global investor_all_dicts
    global business_df
    global sheet
    global business_sheet

    investor_id = int(investor_id)

    print(f"\n\nInvestor_all_dicts: {investor_all_dicts}\n\n")
    # investor_all_dicts_json = json.loads(investor_all_dicts['investor_id'][investor_id])
    investor_all_dicts_df = pd.DataFrame([investor_all_dicts])
    investor_all_dicts_df['details_dict']  = investor_all_dicts_df['details_dict'].apply(lambda x: json.loads(x))
    print(f"\n\nDeatils: {investor_all_dicts_df['details_dict'] }")
    investor_all_dicts_dict = dict(zip(investor_all_dicts_df['investor_id'], investor_all_dicts_df['details_dict'] ))
    print(f"\n\nInvestor all dicts: {investor_all_dicts_dict}")
    investor_all_dicts_json = investor_all_dicts_dict.get(investor_id)

    print(f"\n\nPrevious history: {investor_all_dicts_json}\n\n")

    available_cash = investor_all_dicts_json.get("available_cash")
    committed_cash = investor_all_dicts_json.get("committed_cash")
    invested_amount = investor_all_dicts_json.get("invested_amount")

    available_cash_update = int(available_cash) - int(selected_amount)
    committed_cash_update = int(committed_cash) + int(selected_amount)
    invested_amount_update = int(invested_amount) + int(selected_amount)

    keys_to_update = ['available_cash', 'committed_cash', 'account_value', 'invested_amount']
    new_values = {'available_cash': available_cash_update, 'committed_cash': committed_cash_update, 'account_value': available_cash_update, 'invested_amount': invested_amount_update}
    print(f"\n\nNew history: {new_values}\n\n")
    investor_all_dicts_json.update((key, new_values[key]) for key in keys_to_update if key in investor_all_dicts_json)
    
    st.markdown('<h1 class="title">Investment successful</h1>',unsafe_allow_html=True)
    st.write(f"You have reserved SAR {float(selected_amount)} for loan. If the loan is fully funded, your account ending in 4431 will be deducted for the amount")
    
    investor_investment_in_business = json.loads(business_df['investor_investments'][selected_index])
    print(f"\n\nBefore update: {investor_investment_in_business}\n\n")
    if investor_id in investor_investment_in_business.keys():
        investor_invested_dict = investor_investment_in_business[investor_id]
        amount_funded = investor_invested_dict.get("amount_funded")
        amount_funded_update = int(amount_funded) + int(selected_amount)
        investor_invested_dict['amount_funded'] = amount_funded_update

        investor_investment_in_business.update(investor_invested_dict)

    else:
        ## use investor_id here
        n = 6
        loan_id = ''.join(["{}".format(random.randint(1, 9)) for num in range(0, n)])
        current_date = datetime.now()

        formatted_date = current_date.strftime("%m/%d/%Y")

        new_investment = {
                                investor_id: {
                                        "investor_name": st.session_state.investor_name,
                                        "loan_id": str(loan_id),
                                        "interest_rate": str(rate),
                                        "term": str(term),
                                        "simah": "695-699",
                                        "total_required": str(required),
                                        "amount_funded": str(selected_amount),
                                        "Date Invested": formatted_date,
                                }
                            }
            
        investor_investment_in_business.update(new_investment)

    print(f"\n\After update: {investor_investment_in_business}\n\n")

    business_update = json.dumps(investor_investment_in_business)
    business_df.at[selected_index, 'investor_investments'] = business_update
    # business_sheet.update([business_df.columns.values.tolist()] + business_df.values.tolist())

    investor_update = json.dumps(investor_all_dicts_json)
    investor_all_dicts_df.at[selected_index, 'details_dict'] = investor_update
    print(f"\n\nBusiness Df: {business_df}\n\n")
    print(f"\n\nInvestor Df: {investor_all_dicts_df}\n\n")
    # sheet.update([investor_all_dicts.columns.values.tolist()] + investor_all_dicts.values.tolist())

    if st.button("Done"):
        modal.close()

    st.text("")
    st.text("")
        

def invest():
    global business_df
    data = business_df

    business_names = []
    interest_rates = []
    terms = []
    simah_scores = []
    loan_required = []

    for i in range(0, len(data)):
        business_details = data['business_details'][i]
        investor_investments = data['investor_investments'][i]

        business_names.append(json.loads(business_details)['business_name'])
        interest_rates.append(json.loads(business_details)['rate'])
        terms.append(json.loads(business_details)['term'])
        simah_scores.append(json.loads(business_details)['simah'])
        loan_required.append(json.loads(business_details)['loan_required'])
        
    data = {
        f'Name': business_names,
        'Rate': interest_rates,
        'Term': terms,
        'Simah': simah_scores,
        'Required': loan_required,
    }

    df = pd.DataFrame(data)
    
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column('Simah')
    options_builder.configure_selection(selection_mode="single", use_checkbox=True)
    # options_builder.configure_default_column(width=150, resizable=True)
    # options_builder.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
    grid_options = options_builder.build()
    
    grid = AgGrid(df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, gridOptions = grid_options, allow_unsafe_jscode=True, fit_columns_on_grid_load=True, theme='alpine')
    sel_row = grid["selected_rows"]
    modal = Modal(key="Invest_Modal",title="")
    if sel_row:
        open_modal = st.button("View Details", key="invest")
        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                selected_index = sel_row[0]['_selectedRowNodeInfo']['nodeRowIndex']
                name = sel_row[0]['Name']
                rate = sel_row[0]['Rate']
                term = sel_row[0]['Term']
                loan_required = sel_row[0]['Required']
                st.text("")
                st.text("")
                selected_amount, funded = load_invest_details(name, rate, term, loan_required)
                # investor_id = "561374"
                investor_id = st.session_state.investor_id

                if st.button("Confirm Investment"):
                    invest_in_business(investor_id, name, rate, term, selected_amount, loan_required, funded, selected_index, modal)
                    # modal.close()

                st.text("")
                st.text("")

        # st.write(f"<b>Rate: </b>{sel_row[0]['Rate']}",unsafe_allow_html=True)

def investor_main():
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
    set_custom_css_investor()
    st.markdown(
        """
        <style>
        .st-cf {
            color: #2A6FCA !important;
            margin-left: 40px;
        }
        .st-c0 {
            color: #2A6FCA !important;
            margin-left: 40px;
        }
        .st-e0 {
            color: #2A6FCA !important;
        }
        .st-cp {
            background-color: #2A6FCA;
        }
        .st-ee:hover {
            background-color: #2A6FCA;
        }
        """,
        unsafe_allow_html=True,
    )

    # .st-e2 {
    #         background-color: #2A6FCA;
    #     }
    
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
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    show_logout()
    
    tab1, tab2, tab3 = st.tabs(
        ["Summary", "Portfolio", "Invest"]
    )

    with tab1:
        summary()
    with tab2:
        portfolio()
    with tab3:
        invest()

if __name__ == '__main__':
    investor_main()
