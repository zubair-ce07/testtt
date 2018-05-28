class Utils:

    @staticmethod
    def clean_price_list (price_list):
        cleaned_price_list = []
        for prices in price_list:
            prices = prices.replace('\r\n\t', '').replace('\t', '').replace('R$', '')
            if prices.isdigit():
                cleaned_price_list.append(int(prices) * 100)

        return cleaned_price_list

    @staticmethod
    def get_price_info (price_list):
        price_list = price_list[0:int(len(price_list)/2)]
        if int(len(price_list)) > 1:
            cleaned_price_list = Utils.clean_price_list(price_list)
            return cleaned_price_list[len(cleaned_price_list)-1]
        else:
            return int(price_list[0].replace('\t','').replace('\nR$','').replace('\r','')) * 100

    @staticmethod
    def get_previous_prices (price_list):
        price_list = price_list[0:int(len(price_list)/2)]
        price_info = {}
        if int(len(price_list)) > 1:
            cleaned_price_list = Utils.clean_price_list(price_list)
            return cleaned_price_list[0:len(cleaned_price_list)-1]
        else:
            return []
    
    @staticmethod
    def get_decription_info (description_text, description_list):
        description = [description_text]
        for list_item in description_list:
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            if 'Material' not in span_text:
                description.append(f"{span_text}: {strong_text}")
            
        return description
    
    @staticmethod
    def get_care_info (description_list):
        care = []
        for list_item in description_list:
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            if 'Material' in span_text:
                care.append(f"{span_text}: {strong_text}")
        
        return care
    
    @staticmethod
    def get_color_info (description_list):
        color = ''
        for list_item in description_list:
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            if 'Cor' in span_text:
                color = strong_text
            
        return color
               
    @staticmethod
    def get_sku_info (size_list, price, color):
        color_dictionary = {}
        dictionary = {size_list[i+1]: size_list[i] for i in range(0, len(size_list), 2)}
        for key,value in dictionary.items():
            dictionary = {'color':color, 'currencey':'BRL', 'price':price, 'size':key}
            if 'sch-avaiable' not in value:
                dictionary['out-of-stock'] = True
            color_dictionary[f"{color}{key}"] = dictionary

        return color_dictionary
    
    @staticmethod
    def get_sku_info_from_drop_down (size_list, price, color):
        color_dictionary = {}
        for value in size_list:
            dictionary = {'color':color, 'currencey':'BRL', 'price':price, 'size':value, 'out-of-stock':True}
            color_dictionary[f"{color}{value}"] = dictionary
        return color_dictionary

    @staticmethod
    def is_out_of_stock (size_list):
        dictionary = {size_list[i+1]: size_list[i] for i in range(0, len(size_list), 2)}
        for key,value in dictionary.items():
            if 'sch-avaiable' in value:
                return False
        return True

