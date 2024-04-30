import openai
from secret_key import openai_key
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

client = openai.OpenAI(api_key=openai_key)

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user","content": prompt}],
    )
    content = response.choices[0].message.content
    
    print(content)
    
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })

def extract_financial_data_from_url(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        financial_data_df = extract_financial_data(text)
        return financial_data_df
    else:
        return None
    
def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============
    '''
