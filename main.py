# pip install pyyaml
# pip install pandas
# pip install requests
# pip install openpyxl
# pip install PyMySQL

import pandas as pd
pd.options.display.max_colwidth = 150
import yaml
from function import  NK_status_checker
from function import  get_attr_value
from function import  get_attr_type
from function import internal_product_attr_parser

'''  ЗАДАИМ ПАРАМЕТРЫ '''
with open ('params.yaml', 'r', encoding='UTF-8') as f:
    params = yaml.safe_load(f)

url = params['API_url']
apikey = params['apikey']
input_folder = params['input_folder']
input_file = params['input_file']
input_path = input_folder + input_file
sheet_name = params['sheet_name']

output_file = params['output_file']
output_folder = params['output_folder']
full_output_path = output_folder + output_file

x = NK_status_checker(url=url, apikey=apikey, gtin=4640103830058 )
if int(x) == 200:
    print('main 26: предварительная проверка сервера. status code =', x)
else:
    print('main : предварительная проверка сервера. status code =', x)

# Press the green button in the gutter to run the script.

df_full = pd.DataFrame()

df = pd.read_excel(input_path, sheet_name=sheet_name)

for row in range(len(df)):
    current_df = pd.DataFrame()
    #print('current row = ', row)
    AccountId = df.loc[row, 'NK_MainAccountId']
    GTIN = df.loc[row, 'NK_GTIN']
    AttrId = df.loc[row, 'NK_AttrId']
    print('current row = {} and  current GTIN = {}'.format(row,GTIN))
    try:
        NK_value, NK_type = internal_product_attr_parser(AccountId = AccountId, gtin = GTIN, attribute = AttrId, url=url, apikey=apikey)
        current_df.loc[row, 'GTIN'] = GTIN
        current_df.loc[row, 'AccountId'] = AccountId
        current_df.loc[row, 'AttrId'] = AttrId
        current_df.loc[row, 'NK_value'] = NK_value
        current_df.loc[row, 'NK_type'] = NK_type
        #print('  NK_value =', NK_value)
        #print('  NK_type =', NK_type)
        #print('m57: current_df = \n', current_df.to_string())

        if len(df_full) == 0:

            df_full = current_df.copy()
            #print('m62: в первый раз df_full = \n', df_full.to_string())
        else:
            df_full = pd.concat([df_full, current_df], axis=0)
            #print('m65: df_full = \n', df_full.to_string())
    except:
        print('m67: для строки {} сработал except \n'.format(row))
        df_full = df_full



try:
    df_full.to_excel(full_output_path, index=True, sheet_name='sheet_1')
    print('файл успешно записался!')
except PermissionError:
    print('\nфайл не доступен для записи\n')





    #attrId, attr_value, attr_value_type = NK_json_receiver(url=url, apikey=apikey, gtin=gtin, attribute=attribute)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
