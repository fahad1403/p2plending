import streamlit as st

def set_custom_css():

    custom_css = """
    <style>
    .title {
    color: #3498db; /* Title color */
    font-size: 36px; /* Title font size */
    font-weight: bold; /* Bold font weight */
    text-align: center; /* Text alignment */
    margin-bottom: 20px; /* Add some spacing below the title */
} 
# img,svg{
# height:10px;
# }
.description{
text-align:center;
font-size:15px;
align-items:center;
font-weight:bold;
# color: #1e488f;
}
.st-bp{
# width:30px;
# height:10px;
# background: #2A6FCA;
# color: #1e488f;
}
# .st-dj {
#     background: linear-gradient(to right,(135deg, #007bff, #00bfff), (135deg, #007bff, #00bfff); 26.5768%, rgba(151, 166, 195, 0.25) 26.5768%, rgba(151, 166, 195, 0.25) 100%);
# }
.st-emotion-cache-5rimss p{
text-align:center;
}
# .st-dn{
# background-color:#2A6FCA;
# }
.st-emotion-cache-1vzeuhh{
background: #2A6FCA;
}
.st-emotion-cache-10y5sf6{
    color: rgb(0, 0, 220);
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
            margin-top:20px;
            font-size: 16px;
            padding: 15px 20px;
        }
    }
    .st-emotion-cache-7ym5gk {
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
     @media (max-width: 768px) {
        .st-emotion-cache-7ym5gk{
            margin-top:20px;
            font-size: 16px;
            padding: 15px 20px;
        }
    }
}

</style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
   