# pip install pyyaml
# pip install pandas
# pip install requests
# pip install openpyxl

import requests
import pandas as pd
pd.options.display.max_colwidth = 150
from requests.auth import HTTPBasicAuth
import yaml
from function import  NK_status_checker
from function import internal_product_attr_parser

'''  ЗАДАИМ ПАРАМЕТРЫ '''
with open ('params.yaml', 'r', encoding='UTF-8') as f:
    params = yaml.safe_load(f)


url = params['url']
apikey = params['apikey']
gtins = params['gtins']
payload = {'apikey':apikey, 'gtins':gtins}


x = NK_status_checker(url=url, apikey=apikey, gtin=4640103830058 )
if int(x) == 200:
    print('main 26: предварительная проверка сервера. status code =', x)
else:
    print('main : предварительная проверка сервера. status code =', x)



# Press the green button in the gutter to run the script.

def get_attr_value(row):
    out = internal_product_attr_parser(gtin=row['GTIN'], attribute=row['Attributes ID'], url=url, apikey=apikey, output='value')
    return out

def get_attr_type(row):
    out = internal_product_attr_parser(gtin=row['GTIN'], attribute=row['Attributes ID'], url=url, apikey=apikey, output='type')
    return out


if __name__ == '__main__':
    df = pd.read_excel('D:/CRPT/2021.06_июнь/СВЕРКА РАСХОЖДЕНИЙ/тестирование парсера internal-product/объединенный.xlsx')
    print(df.to_string())

    df['NK_value'] = df.apply(get_attr_value, axis=1, result_type='expand')
    df['NK_type'] = df.apply(get_attr_type, axis=1, result_type='expand')
    print(df.to_string())




    #attrId, attr_value, attr_value_type = NK_json_receiver(url=url, apikey=apikey, gtin=gtin, attribute=attribute)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
