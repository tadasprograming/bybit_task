import json


'''data_file = open('BTCUSD_kline.json', 'r')
test_json = json.loads(data_file.read())
print(type(test_json))'''

with open('BTCUSD_kline.json') as user_file:
  parsed_json = json.load(user_file)

print(type(parsed_json['open_price'][0]))
