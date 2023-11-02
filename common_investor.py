import streamlit as st

def set_custom_css_investor():
    custom_css = """
    <style>
    .business_title{
        color: #3498DB; /* Title color */
        font-size: 28px; /* Title font size */
        font-weight: bold; /* Bold font weight */
        text-align: center; /* Text alignment */
        margin-bottom: 20px; /* Add some spacing below the title */
    }
     .title {
        color: #3498db; /* Title color */
        font-size: 36px; /* Title font size */
        font-weight: bold; /* Bold font weight */
        text-align: center; /* Text alignment */
        margin-bottom: 20px; /* Add some spacing below the title */
    
    } 
    .st-cf {
        color: #2A6FCA !important;
        margin-left: 40px;
    }
    .st-e0 {
        color: #2A6FCA !important;
        margin-left: 40px;
    }
    .st-cp {
        background-color: #2A6FCA;
    }
  .st-emotion-cache-16idsys p{
  font-weight:bold;
  font-size:14px;
  }
#   .st-emotion-cache-16idsys p:hover{
#    color: #00FF00 !important;
#   }
  .st-cp{
  color: #00FF00 !important;
  }
  .st-emotion-cache-5rimss p{
  font-size:15px;
#   font-weight:bold;
#   text-align:center;
#   align:center;
  }
  .st-emotion-cache-1y04v0k{
  align:center;
  text-align:center;
  }
   .creds{
   color:white;
    font-weight:bold;
   }
 .stTextInput  > label {
    color:white;
    font-weight:bold;
    }
    
    # .st-emotion-cache-10trblm{
    # align:center;
    # text-align:center;
    # }
    # .modal-overlay{
    # color:white;
    # width:90%;
    # height:90%;
    # }
    .st-emotion-cache-1gulkj5{
    background:linear-gradient(to bottom, #3399ff  0%,#00ffff  100%);
    }
    .st-emotion-cache-r421ms{
    background:linear-gradient(to bottom, #3399ff  0%,#00ffff  100%);
    }
    .st-emotion-cache-10434yk{
    background:linear-gradient(to bottom, #3399ff  0%,#00ffff  100%);
    margin-left: 70px;
    }
    .div:first-child{
    overflow:auto;
    }
    # .st-emotion-cache-10trblm{
    #  color:white;
    # font-weight:bold;
    # align:center
    # text-align:center;
    # }
    # .st-emotion-cache-1aehpvj{
    # color:white;
    # font-weight:bold;
    # align:center
    # text-align:center;
    # }
    # .st-emotion-cache-1fttcpj{
    # color:white;
    # font-weight:bold;
    # align:center
    # text-align:center;
    # }
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
#     .st-emotion-cache-10oheav{
#      background:linear-gradient(to bottom, #3399ff  0%,#00ffff  100%);
#      height:100%;
#      width:100%
#    }
#    .st-emotion-cache-10oheav h2{
#    align:center;
#    text-align:center;
#    font-size:20px;
#    color:white;
#    font-weight:bold;
#    }
#    .st-emotion-cache-16idsys p{
#    align:center;
#    text-align:center;
#    color:white;
#    font-weight:bold;
#    }
#    .st-emotion-cache-fblp2m{
#    color:white;
#    }
    .stButton>button:active {
        color: #00FF00 !important;
    }
    @media (max-width: 768px) {
        .stButton>button {
            font-size: 16px;
            padding: 15px 20px;
        }
    }
    .st-emotion-cache-9ycgxx{
    color:white;
    font-weight:bold;
    # text-align:right;
    # align:right;
    }
    .st-emotion-cache-1aehpvj{
     color:white;
    font-weight:bold;
    #  text-align:right;
    # align:right;
    }
    .st-emotion-cache-1y04v0k{
     background: linear-gradient(to right, #ff00cc, #3333ff); /* Replace these colors with your desired gradient colors */
    color: white; /* Set the text color to white or any color that contrasts well with the gradient */
    align:center;
    /* Add other styling as needed */
    }
    .st-em{
    text-align:center;
    align:center;
    font-size:15px;
    font-weight:bold;
    }
    .st-gf{
    text-align:center;
    align:center;
    font-size:15px;
    font-weight:bold;
    }
    .st-emotion-cache-16idsys p{
    text-align:center;
    font-weight:bold;
    }
    h3 {
     color: #3498db !important;
     text-align:center;
    align:center;
    font-weight:bold;
    }
    .sub-title{
    text-align:center;
    align:center;
    font-weight:bold;
    }
    @media screen and (max-width: 768px) {{
        .st-emotion-cache-5rimss {{
            width: 100%;
        }}
        .st-emotion-cache-5rimss {{
            width: {value}%;
            font-size: 10px;
        }}
    }}
    @media (max-width: 768px){
    .st-emotion-cache-5rimss{
     width: 100%;
    }
    .st-emotion-cache-5rimss{
    width: {value}%;
    font-size: 10px;
    }
    }
    @media (max-width: 768px){
    .st-emotion-cache-fg4pbf {
     font-size: 12px;
    }
    }
    div[data-modal-container='true'][key='Details_Modal'] > div:first-child > div:first-child{
                             max-height: 700px; /* Adjust the maximum height as needed */
                            overflow-y: auto !important;
    }
    div[data-modal-container='true'][key='Invest_Modal'] > div:first-child > div:first-child{
        width: unset !important;
        background-color: #fff;
        padding-top: 100px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-bottom: 30px !important;
        margin-top: 10px !important;
        margin-left: -10px !important;
        margin-right: -10px !important;
        margin-bottom: 0px !important;
        z-index: 1001 !important;
        border-radius: 5px !important;
        overflow-y: auto !important;
        max-height: 500px;
    }
    div[data-modal-container='true'][key='Portfolio_Modal'] > div:first-child > div:first-child{
        width: unset !important;
        background-color: #fff;
        padding-top: 100px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-bottom: 30px !important;
        margin-top: 10px !important;
        margin-left: -10px !important;
        margin-right: -10px !important;
        margin-bottom: 0px !important;
        z-index: 1001 !important;
        border-radius: 5px !important;
        overflow-y: auto !important;
        max-height: 500px;
    }
    div[data-modal-container='true'][key='Portfolio_Modal'] > div:first-child > div:first-child::after {
    content: '';
    display: block;
    height: 50px; /* Assuming the button height is 50px, adjust it accordingly */
    }

    div[data-modal-container='true'][key='Portfolio_Modal'] > div:first-child > div:first-child:only-child::after {
        display: none;
    }
    .st-emotion-cache-rj5w3t e1f1d6gn0{
                width:90%;
                height:80%;
                top:70%;
                left:70%;
                }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
   