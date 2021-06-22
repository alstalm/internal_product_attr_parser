import requests
import yaml
import json
import numpy as np

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

def internal_product_attr_parser(url, apikey, gtin, attribute, output='value'):
    statusCode = NK_status_checker(url, apikey, gtin)

    if int(statusCode) != 200:
        returned_value = np.NaN
    else:

        url = url
        headers= {}
        data = {'apikey':apikey, 'gtins':gtin}

        r = requests.request(method="GET",
                             url=url,
                             headers=headers,
                             params=data
                             )

        response = json.loads(r.text)
        attributes = response['result'][0]['good_attrs']

        for i in range(len(attributes)):
            attrId = response['result'][0]['good_attrs'][i]['attr_id']

            attr_value, attr_value_type = np.NaN, np.NaN

            if int(attrId) == attribute:
                attrId = attrId
                attr_value = response['result'][0]['good_attrs'][i]['attr_value']
                attr_value_type = response['result'][0]['good_attrs'][i]['attr_value_type']
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
