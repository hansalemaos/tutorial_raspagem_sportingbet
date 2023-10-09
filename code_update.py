import re
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

add_printer(1)


def obter_dataframe(query="*"):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=True,
        )
    return df


driver = Driver(uc=True)
driver.get("https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/102838,102361,102155")
# para rodar para sempre:
while True:
    try:
        df = obter_dataframe(query='ms-event')
        df = df.dropna(subset='aa_innerText' ).aa_innerText.apply(lambda x: pd.Series([q for q in re.split(r'[\n\r]', x) if not re.match(r'^\d+$', q)]))[[2, 0, 1, 4, 5, 6]].rename( columns={0: 'team1_nome', 1: 'team2_nome', 2: 'data', 4: 'team1', 5: 'empate', 6: 'team2'}).dropna().assign(team1=lambda q:q.team1.str.replace(',', '.'),team2=lambda q:q.team2.str.replace(',', '.'),empate=lambda q:q.empate.str.replace(',', '.')).astype({'team1': 'Float64', 'empate': 'Float64', 'team2': 'Float64'})
        print(df)
    except Exception as baba:
        print(baba)
