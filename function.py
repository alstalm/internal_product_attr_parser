import requests
import yaml
import json
import numpy as np
import pymysql

with open ('params.yaml', 'r', encoding='UTF-8') as f:
    params = yaml.safe_load(f)

url = params['API_url']
apikey = params['apikey']
host = params['DB_host']
user = params['DB_user']
port = params['DB_port']
password = params['DB_password']
database = params['DB_database']

def get_attr_value(row):
    out = internal_product_attr_parser(AccountId = row['AccountId'], gtin=row['GTIN'], attribute=row['Attributes ID'], url=url, apikey=apikey, output='value')
    return out

def get_attr_type(row):
    out = internal_product_attr_parser(AccountId = row['AccountId'], gtin=row['GTIN'], attribute=row['Attributes ID'], url=url, apikey=apikey, output='type')
    return out


def NK_status_checker(url, apikey, gtin ):
    url = url
    headers= {}
    data = {'apikey':apikey, 'gtins':gtin}

    r = requests.request(method="GET",
                         url=url,
                         headers=headers,
                         params=data
                         )
    if r.status_code != 200:
        print('func 17: for GTIN = {} Status code = {}'.format(gtin, str(r.status_code)) )


    return (str(r.status_code))

def internal_product_attr_parser(url, apikey, AccountId, gtin, attribute, output='value'):
    # проверим есть ли такой gtin в i-p
    statusCode = NK_status_checker(url, apikey, gtin)

    if int(statusCode) != 200:
        # если нет, функция должна вернуть NaN
        returned_value = 'status code = {}'.format(statusCode)
    else:
        # иначе начинаем парсить ответ
        url = url
        headers = {}
        data = {'apikey': apikey, 'gtins': gtin}
        r = requests.request(method="GET",
                             url=url,
                             headers=headers,
                             params=data
                             )

        response = json.loads(r.text)

        # проверим, возможны ли экземпляры. если gtin - российский то извлечем единственный массив атрибутов
        if str(gtin)[:2] == '46':
            attributes = response['result'][0]['good_attrs']


        else:
            # gtin - импортный. значит идем в базу в ИНН аккаунта
            if AccountId == '***':
                # изменения примерены для всех AccountId
                attributes = response['result'][0]['good_attrs']
            else:
                # изменения применены для некоторых AccountId
                query = "SELECT ITN FROM Pro_Accounts pa WHERE AccountId = " + str(AccountId)

                ''' СОЗДАДИМ ОБЪЕКТ ПОДКЛЮЧЕНИЯ'''
                con = pymysql.connect(host=host, user=user, port=port, password=password, database=database)

                with con:
                    cur = con.cursor()
                    cur.execute(query)
                    DBresponse = cur.fetchone()
                    if DBresponse != None:
                        ITN = DBresponse[0]
                    else:
                        print('такого AccountId {} в БД не найдено'.format(AccountId))
                        ITN = np.NaN


                # извлечем единственный массив атрибутов, где producer_inn = ITN
                for good in range(len(response['result'])):
                    producer_inn = response['result'][good]['producer_inn']
                    if producer_inn == ITN:
                        attributes = response['result'][good]['good_attrs']
                        print('func 94: attributes = {}'.format(attributes))
                    else:
                        attributes = None
                        print('func 97: attributes = {}'.format(attributes))
            # теперь из полученного массива атрибутов начнем парсинг значений и типов


        if attributes == None:
            # если AccounId не был найден то не стали искать и  attributes а значит и выходное значение тоже возвращаем пустым
            returned_value = np.NaN
            print('func 104: returned_value ={}'.format(returned_value))
        else:
            # если  gtin российсикй или AccounId благополучно найден, то
            print('func 107: сработал else')
            for i in range(len(attributes)):
                print('func 109: зашли в цикл')
                attrId = attributes[i]['attr_id']

                attr_value, attr_value_type = np.NaN, np.NaN

                if int(attrId) == attribute:

                    attr_value = attributes[i]['attr_value']
                    attr_value_type = attributes[i]['attr_value_type']
                    break

            if output == 'value':
                returned_value = attr_value
            elif output == 'type':
                returned_value = attr_value_type
            else:
                returned_value = 'не определено: тип или значение'

    return returned_value


if __name__ == '__main__':

    '''  ЗАДАИМ ПАРАМЕТРЫ '''
    with open('params.yaml', 'r', encoding='UTF-8') as f:
        params = yaml.safe_load(f)


    url = 'https://api.staging.catalog.crpt.ru/v3/internal-product'
    apikey = params['apikey']
    gtin = params['gtins']
    attribute = 13797
    payload = {'apikey': apikey, 'gtins': gtin}


    ''' ЗАПРОСИМ JSON'''
    result = internal_product_attr_parser(url=url, apikey=apikey, gtin=gtin, attribute=attribute, output='value')
    print('result =', result)
