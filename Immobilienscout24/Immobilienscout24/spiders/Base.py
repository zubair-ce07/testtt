import re


class BaseClass:
    rent_types = [
        "APARTMENT_RENT",
        "HOUSE_RENT",
        "SHORT_TERM_ACCOMMODATION",
        "FLAT_SHARE_ROOM",
        "OFFICE_RENT",
        "INDUSTRY_RENT",
        "STORE_RENT",
        "GASTRONOMY_RENT",
        "SPECIAL_PURPOSE_RENT",
        "LIVING_RENT_SITE",
        "TRADE_SITE_RENT",
        "GARAGE_RENT",
        "ASSISTED_LIVING",
        "SENIOR_CARE"
    ]
    sale_types = [
        "APARTMENT_BUY",
        "HOUSE_BUY",
        "OFFICE_BUY",
        "INDUSTRY_BUY",
        "STORE_BUY",
        "GASTRONOMY_BUY",
        "SPECIAL_PURPOSE_BUY",
        "LIVING_BUY_SITE",
        "TRADE_SITE_BUY",
        "GARAGE_BUY",
        "INVESTMENT",
        "COMPULSORY_AUCTION",
        "HOUSE_TYPE"

    ]
    business_rent_type = [
        "OFFICE_RENT",
        "INDUSTRY_RENT",
        "STORE_RENT",
        "GASTRONOMY_RENT",
        "TRADE_SITE_RENT",
        "SPECIAL_PURPOSE_RENT"
    ]

    business_sale_type = [
        "OFFICE_BUY",
        "INDUSTRY_BUY",
        "STORE_BUY",
        "GASTRONOMY_BUY",
        "TRADE_SITE_BUY",
        "SPECIAL_PURPOSE_BUY",
        "COMPULSORY_AUCTION_BUSINESS"
    ]

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return str(re.sub(r'\s+|\xa0', '', to_clean)).strip()
        to_clean = [self.clean(c) for c in to_clean]
        return [c for c in to_clean if c]
