import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO

def extract_text_html(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup

def table_to_dataframe(soup_function, tag_table, id_table):
    html_table = soup_function(tag_table, id=id_table)
    df = pd.read_html(StringIO(str(html_table)), decimal=',', thousands='.')
    return df[0]


URL = r'https://www.vriconsulting.com.br/indices/inpc.php?pagina='
soup = extract_text_html(URL)


tag_a = soup.find('a', title='Última Página')
regex_last_page = re.compile(r'pagina=(\d*)')
number_last_page = re.search(regex_last_page, tag_a.get('href'))
number_last_page = int(number_last_page.group(1))

df_inpc = table_to_dataframe(soup.find, 'table', 'indiceTable')

current_page = 2
while current_page <= number_last_page:
    soup_current_page = extract_text_html(URL + str(current_page))
    df_current_page = table_to_dataframe(soup_current_page.find, 'table', 'indiceTable')
    
    df_inpc = pd.concat([df_inpc, df_current_page], ignore_index=True)
    current_page +=1

df_inpc.to_csv('tabela_inpc.csv', sep=';')


