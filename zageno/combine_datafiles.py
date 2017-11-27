import sys
import json


def main(argv):
    input_fname_1, input_fname_2, input_fname_3, output_fname = argv

    combine_data = []

    with open(input_fname_1) as json_data:
        data_1 = json.load(json_data)
    with open(input_fname_2) as json_data:
        data_2 = json.load(json_data)
    with open(input_fname_3) as json_data:
        data_3 = json.load(json_data)

    for data in data_1:
        price_2 = {}
        price_3 = {}
        p_id = data['product_table']['id']
        for d2 in data_2:
            if d2['product_table']['id'] == p_id:
                price_2 = d2['price_table']
                break
        for d3 in data_3:
            if d3['product_table']['id'] == p_id:
                price_3 = d3['price_table']
                break
        if not price_2 or not price_3:
            continue

        c_data = data.copy()
        prices = c_data['price_table'] + price_2 + price_3
        for idx, price in enumerate(prices, start=1):
            if not price['size']:
                price['id'] = idx
                price['size'] = ""
        c_data['price_table'] = prices
        combine_data.append(c_data)

    with open(output_fname, 'w') as f:
        f.write('[')
        for data in combine_data[:-1]:
            json.dump(data, f)
            f.write(',\n')
        json.dump(combine_data[-1], f)
        f.write('\n]')

if __name__ == "__main__":
    main(sys.argv[1:])
