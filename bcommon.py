import streamlit as st
def set_custom_css():
    custom_css="""
    <style>
    .title{
    text-align:center;
    color: #3498db; /* Title color */
    font-family: Source Sans Pro,  sans-serif;
    font-size: 36px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    }
    .borrower_description{
    text-align:center;
    color: #3498db; /* Title color */
    font-family: Source Sans Pro,  sans-serif;
    font-size: 16px;
    font-style: normal;
    font-weight: 300;
    line-height: normal;
    }
    .Iqama_button{
    margin-top:80px;
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
    .Forgot_button, .New_account {
        background-color: #4C43CD;
        background-image: radial-gradient(93% 87% at 87% 89%, rgba(0, 0, 0, 0.23) 0%, transparent 86.18%), radial-gradient(66% 87% at 26% 20%, rgba(255, 255, 255, 0.41) 0%, rgba(255, 255, 255, 0) 69.79%, rgba(255, 255, 255, 0) 100%);
        box-shadow: 2px 19px 31px rgba(0, 0, 0, 0.2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    @media (max-width: 768px) {
        .button-container {
            flex-direction: column;
            align-items: flex-start;
        }
        .button-container hr {
            margin: 10px 0;
            width: 100%;
        }
    }
    .st-emotion-cache-5rimss p{
    margin-top:20px;
    text-align:center;
    color: #3498db; /* Title color */
    }
    .borrowers_title{
    margin-top:20px;
    color: #2A6FCA;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    }
    .borrowers_description{
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 24px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .borrowers_small_description{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
        }
    # .st-emotion-cache-1y4p8pa{
    # #  background:linear-gradient(to bottom, #3399ff  0%,#00ffff  100%);
    # #  }
    .st-emotion-cache-1y4p8pa{
    background: linear-gradient(to right,(135deg, #007bff, #00bfff), (135deg, #007bff, #00bfff); 26.5768%, rgba(151, 166, 195, 0.25) 26.5768%, rgba(151, 166, 195, 0.25) 100%);    }
    .signin_title{
     color: #3498db; /* Title color */
    text-align: center;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 20px;
    font-style: normal;
    font-weight: lighter;
    line-height: normal;
    }
    .st-emotion-cache-r421ms {
    margin-top:30px;
    }
    .st-emotion-cache-7ym5gk{
    width:100%;
    }
    .Review_Confirm{
    margin-top:80px;
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
     .stButton>button {
        display: block;
        margin: 0 auto;
        align-items: center;
        background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
        border: 0;
        border-radius: 6px;
        box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
        box-sizing: border-box;
        color: #FFFFFF;
        display: flex;
        font-family: Phantomsans, sans-serif;
        font-size: 20px;
        justify-content: center;
        line-height: 1em;
        max-width: 100%;
        min-width: 140px;
        padding: 19px 24px;
        text-decoration: none;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        white-space: nowrap;
        cursor: pointer;
    }
    .stButton>button:hover {
        color: #00FF00 !important;
    }
    .stButton>button:active {
        color: #00FF00 !important;
    }
    @media (max-width: 768px) {
        .stButton>button {
            font-size: 16px;
            padding: 15px 20px;
        }
    }
    .Role_Button_Investor{
    margin-bottom:10px;
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background: linear-gradient(144deg, #0A3463, #081E41);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
    .Role_Button_Borrower{
    # margin-top:10px;
    margin-bottom:10px;
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background: linear-gradient(144deg, #0A3463, #081E41);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
    .Login_button{
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background-color: #409083;
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
    
   .Forgot_button, .New_account {
        background-color: #4C43CD;
        background-image: radial-gradient(93% 87% at 87% 89%, rgba(0, 0, 0, 0.23) 0%, transparent 86.18%), radial-gradient(66% 87% at 26% 20%, rgba(255, 255, 255, 0.41) 0%, rgba(255, 255, 255, 0) 69.79%, rgba(255, 255, 255, 0) 100%);
        box-shadow: 2px 19px 31px rgba(0, 0, 0, 0.2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    @media (max-width: 768px) {
        .button-container {
            flex-direction: column;
            align-items: flex-start;
        }
        .button-container hr {
            margin: 10px 0;
            width: 100%;
        }
    }
    .Nafath_App{
    margin-top:80px;
    width:100%;
    border-radius:5px;
    height:40px;
    align-items: center;
    background-image: linear-gradient(144deg, #AF40FF, #5B42F3 50%, #00DDEB);
    border: 0;
    border-radius: 6px;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    box-sizing: border-box;
    color: #FFFFFF;
    }
    .create_account_title{
    margin-top:20px;
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 25px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .create_account_description{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .create_account_description{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .create_account_terms{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .account{
    text-align:center;
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .otp_header{
    margin-top:20px;
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 25px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .otp_description{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .salary_header{
    margin-top:20px;
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 24px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    }
    .salary_description{
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .review_details_header{
    margin-top:20px;
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 24px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    }
    .review_details_description{
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .st-emotion-cache-10trblm{
    margin-bottom:2px;
    }
    .Full_Name{
    color: #717171;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    }
    .Full_Name_Value{
    color: #000;
    font-family: Source Sans Pro,  sans-serif;
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    }
    </style>
    """
    st.markdown(custom_css,unsafe_allow_html=True)


def perform_logout():
    st.write("You have been logged out.")
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun
    # borrower_flow()

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
        pass
