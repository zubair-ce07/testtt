import re


class CurrencyParseException(Exception):
    pass


class CurrencyParser:
    PRICE_R = re.compile('(?:RS.|RM|PHP|RP|R\$|JPY|BRL|CNY|CAD|[$\u00a3\u00a5\uFFE5\u20ac\u20B9])?'
                         '\s*(\d[\d\.\,]*)', re.I | re.U)

    PERCENTAGE_R = re.compile('\d+\%')
    DOT_IS_THOUSANDS_R = re.compile('\.(\d{3})')
    COMMA_IS_CENTS_R = re.compile(',\d{2}$')
    _SPACE_THOUSANDS = re.compile('(\d{1,3})\s(\d{3})', re.U)

    currency_map = [
        ("MXN", "MXN"),
        ('E£', 'EGP'), ("ج.م", "EGP"),
        ("\u00A3", "GBP"), ("&POUND;", "GBP"), ("GBP", "GBP"), ("POUND", "GBP"),
        ("US$", "USD"),
        ("CA$", "CAD"), ('C$', 'CAD'),
        ("HKD", "HKD"), ("HK$", "HKD"),
        ("US$", "USD"),
        ("SGD", "SGD"), ("S$", "SGD"),
        ("AED", "AED"), ('DH$', 'AED'), ('د.إ', 'AED'), ('DHS', 'AED'),
        ("NZD", "NZD"),
        ("AUD", "AUD"), ("A$", "AUD"), ("AU$", "AUD"),
        ("\u20AC", "EUR"), ("EUR", "EUR"), ('€', 'EUR'),
        ("INR", "INR"), ("RS.", "INR"), ("\u20B9", "INR"),
        ("MYR", "MYR"), ("RM", "MYR"),
        ("PHP", "PHP"), ('₱', 'PHP'),
        ("THB", "THB"),
        ("VND", "VND"), ('Đ', 'VND'),
        ("IDR", "IDR"),
        ("CNY", "CNY"),
        ("JPY", "JPY"), ("\u00A5", "JPY"), ("\uFFE5", "JPY"), ("&YEN;", "JPY"), ("¥", "JPY"), ("円", "JPY"),
        ("CAD", "CAD"),
        ("ZAR", "ZAR"),
        ("BRL", "BRL"),
        ("\u20BD", "RUB"), ("RUB", "RUB"), ("\u042E", "RUB"),
        ("KRW", "KRW"), ("￦", "KRW"), ("원", "KRW"), ("₩", "KRW"),
        ('PKR', 'PKR'),
        ('LKR', 'LKR'),
        ("DKK", "DKK"),
        ("KR.", "DKK"), ("KR", "DKK"),
        ('ZL', 'PLN'), ("ZŁ", "PLN"), ("PLN", "PLN"),
        ("KČ", "CZK"), ("CZK", "CZK"),
        ("RON", "RON"), ("LEU", "RON"), ("LEI", "RON"),
        ("SEK", "SEK"),
        ("NOK", "NOK"),
        ("FT", "HUF"),
        ("HUF", "HUF"),
        ("CHF", "CHF"), ("SFR.", "CHF"), ('FR', 'CHF'),
        ("₺", "TRY"), ("TL", "TRY"), ('TRY', 'TRY'),
        ("USD", "USD"), ("$", "USD"),
        ("ГРН", "UAH"), ("UAH", "UAH"), ("грн", "UAH"),
        ('KWD', 'KWD'), ('K.D', 'KWD'), ("د.ك", "KWD"),
        ('ЛВ', 'BGN'), ('лв', 'BGN'), ('BGN', 'BGN'), ('LV', 'BGN'),
        ('KN', 'HRK'), ('HRK', 'HRK'),
        ('LEK', 'ALL'),
        ('DIN', 'RSD'),
        ('DEN', 'MKD'), ('ДЕН', 'MKD'),
        ('RSD', 'RSD'),
        ('KN', 'HRK'),
        ('КМ', 'BAM'),
        ('DIN', 'RSD'),
        ('ТНГ', 'KZT'), ('KZT', 'KZT'),
        ('AZ', 'AZN'),
        ('GE', 'GEL'), ('LARI', 'GEL'),
        ('SAR', 'SAR'), ('SR', 'SAR'), ('﷼', 'SAR'), ("ر.س", "SAR"),
        ('AOA', 'AOA'), ('KZ', 'AOA'),
        ('AMD', 'AMD'), ('DRAM', 'AMD'),
        ('AWG', 'AWG'),
        ('BHD', 'BHD'), ('BD', 'BHD'),
        ('ANG', 'ANG'),
        ('EGP', 'EGP'),
        ('GHS', 'GHS'),
        ('GIP', 'GIP'),
        ('IRR', 'IRR'), ('ریال', 'IRR'), ('تومان', 'IRR'),
        ('NZD', 'NZD'),
        ('ILS', 'ILS'), ('₪', 'ILS'),
        ('MAD', 'MAD'), ('د.م.', 'MAD'),
        ('TWD', 'TWD'),
        ('ТГ.', 'KZT'),
        ('IQD', 'IQD'),
        ('JOD', 'JOD'), ('دينار', 'JOD'),
        ('LBP', 'LBP'), ('ل.ل', 'LBP'),
        ('LYD', 'LYD'),
        ('MUR', 'MUR'), ('MAU', 'MUR'),
        ('MDL', 'MDL'),
        ('MNT', 'MNT'),
        ('NGN', 'NGN'),
        ('OMR', 'OMR'), ('ر.ع.', 'OMR'),
        ('QAR', 'QAR'), ('ر.ق', 'QAR'),
        ('SYP', 'SYP'),
        ('THB', 'THB'), ('฿', 'THB'),
        ('UZS', 'UZS'),
        ('KGS', 'KGS'),
        ('DZD', 'DZD'),
        ('XOF', 'XOF'),
        ('XAF', 'XAF'),
        ('XPF', 'XPF'),
        ('TND', 'TND'), ('د.ت', 'TND'),
        ('BYR', 'BYR'),
        ('ALL', 'ALL'),
        ('BAM', 'BAM'), ('KM', 'BAM'),
        ('BYN', 'BYN'), ('BR', 'BYN'),
        ('COP', 'COP'),
        ('ISK', 'ISK'),
        ('MOP', 'MOP'),
        ('MKD', 'MKD'),
        ('NIO', 'NIO'),
        ('PAB', 'PAB'), ('B/.' ,'PAB'),
        ('DOP', 'DOP'),
        ('VEF', 'VEF'), ('BS.F.', 'VEF'),
        ('HNL', 'HNL'),
        ('CRC', 'CRC'),
        ('GTQ', 'GTQ'),
        ('CLP', 'CLP'),
        ('KYD', 'KYD'),
        ('ARS', 'ARS'),
        ('PEN', 'PEN'), ('S/.', 'PEN'),
        ('KHR', 'KHR'),
        ('YRL', 'YER'),
        ('MT', 'MZN'),
        ('LD', 'LYD'),
    ]

    currency_re_map = [
        ('(?:^|\s)RM(?:$|\s|\.)', "MYR"),
        ('(?:^|\s)Q(?:$|\s|\.|\d)', "GTQ"),
        ('(?:^|\s)L(?:$|\s|\.|\d)', "HNL"),
        ('(?:^|\s)C(?:$|\s|\.|\d)', "CRC"),
        ('(?:^|\s)RP(?:$|\s|\.)', "IDR"),
        ('(?:^|\s)R(?:$|\s|\.|\d)', "ZAR"),
        ('(?:^|\s)Fr\.(?:$|\s|\.)', "CHF"),
        ('(?:^|\s)R\$(?:$|\s|\.|\d)', "BRL"),
        ('(?:^|\s)KD(?:$|\s|\.)', "KWD"),
        ('(?:^|\s)(?:Р|P)(?:уб)?\.?(?:$|\s|\.)', "RUB"),
        ('руб(.$|\d)', "RUB"),
    ]
    currency_remap = {
        ('CN', 'JPY'): 'CNY',
        ('AU', 'USD'): 'AUD',
        ('HK', 'USD'): 'HKD',
        ('CA', 'USD'): 'CAD',
        ('MX', 'USD'): 'MXN',
        ('NZ', 'USD'): 'NZD',
        ('SE', 'DKK'): 'SEK',
        ('NO', 'DKK'): 'NOK',
        ('CL', 'USD'): 'CLP',
        ('BM', 'USD'): 'BMD',
        ('TW', 'USD'): 'TWD',
        ('CO', 'USD'): 'COP',
        ('DO', 'USD'): 'DOP',
        ('SG', 'USD'): 'SGD',
        ('BY', 'RUB'): 'BYR',
        ('RO', 'HNL'): 'RON',
        ('IS', 'DKK'): 'ISK',
        ('AL', 'HNL'): 'ALL',
    }

    @staticmethod
    def float_conversion(float_sum):
        """ To make conversions of prices where it is in float form already easier."""
        return int(round(float_sum * 100))

    @staticmethod
    def conversion(money_string, is_cents=False):
        """ To make conversions of prices where currency symbol is absent easier."""
        price = float(money_string.replace(',', ''))
        return int(round(price))if is_cents else CurrencyParser.float_conversion(price)

    @staticmethod
    def lowest_price(money_string):
        return min(CurrencyParser.prices(money_string))

    @staticmethod
    def prices(money_string, is_cents=False):
        money_string = CurrencyParser.PERCENTAGE_R.sub('', money_string)

        prices = []
        for price in CurrencyParser.PRICE_R.findall(money_string):

            if CurrencyParser.DOT_IS_THOUSANDS_R.search(price):
                # The case where '.' is thousands separator.
                # There are cases when dot is both thousands and cents separator,
                # so only remove definite thousands dot.
                price = CurrencyParser.DOT_IS_THOUSANDS_R.sub('\\1', price)

            if CurrencyParser.COMMA_IS_CENTS_R.search(price):
                # the case where ',' is cents separator
                price = price.replace(',', '.')

            price = CurrencyParser.conversion(price, is_cents=is_cents)
            if price:
                prices += [price]

        if not prices:
            raise CurrencyParseException('Could not parse money string: %s' % money_string)

        return prices

    @staticmethod
    def currency(money_string):
        money_string_uc = money_string.upper()

        for currency_re, currency in CurrencyParser.currency_re_map:
            if re.search(currency_re, money_string_uc, re.U | re.I):
                return currency

        for currency_str, currency in CurrencyParser.currency_map:
            if currency_str in money_string_uc:
                return currency

        return None

    @staticmethod
    def normalize_price(money_str):
        """
        A helper function to remove spaces separating thousands in numbers.
        """
        return CurrencyParser._SPACE_THOUSANDS.sub('\\1\\2', money_str)

    @staticmethod
    def extract_prices(money_strs, locale, is_cents=False, retailer_currency=None):
        currencies = set()
        prices = []

        for money_str in money_strs:

            try:
                money_str = CurrencyParser.normalize_price(money_str)
                price = CurrencyParser.prices(money_str, is_cents=is_cents)
                prices += price
            except:
                pass

            currency = CurrencyParser.currency(money_str)
            if not currency:
                continue
            if retailer_currency != currency:
                currency = CurrencyParser.currency_remap.get((locale, currency), currency)
            currencies.add(currency)

        if len(currencies) > 1:
            raise CurrencyParseException('Multiple currencies are detected in single pricing set')

        if len(prices) < 1:
            raise CurrencyParseException('No Prices are detected')

        currency = currencies.pop() if currencies else None

        prices = list(sorted(set(prices), reverse=True))

        return prices[:-1], prices[-1], currency

    @staticmethod
    def currency_and_price(money_string):
        """ Just (currency, price) shorthand """
        return CurrencyParser.currency(money_string), CurrencyParser.lowest_price(money_string)
