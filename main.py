import streamlit as st
import pandas as pd
import openai_helper

def main():
    col1, col2 = st.columns([3,2])

    financial_data_df = pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

    with col1:
        st.title("Financial Data Extraction System  Using OpenAI API")    
        extraction_option = st.radio("Choose extraction method:", ["Paste news article", "Enter website URL"])
        
        if extraction_option == "Paste news article":
            news_article = st.text_area("Paste your financial news article here", height=300)
            if st.button("Extract from Paste"):
                financial_data_df = openai_helper.extract_financial_data(news_article)
        
        elif extraction_option == "Enter website URL":
            url = st.text_input("Enter website URL")
            if st.button("Extract"):
                financial_data_df = openai_helper.extract_financial_data_from_url(url)

    with col2:
        st.markdown("<br/>" * 5, unsafe_allow_html=True)  # Creates 5 lines of vertical space
        st.dataframe(
            financial_data_df,
            column_config={
                "Measure": st.column_config.Column(width=150),
                "Value": st.column_config.Column(width=150)
            },
            hide_index=True
        )

if __name__ == "__main__":
    main()
