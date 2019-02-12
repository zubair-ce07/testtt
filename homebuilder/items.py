from scrapy.item import Item, Field


class HouseBuilder(Item):
    builder = Field()
    community = Field()
    community_address = Field()

    city = Field()
    state = Field()
    zip_code = Field()

    latitude = Field()
    longitude = Field()
    url = Field()

    house_type = Field()
    entry_date = Field()

    phone_number = Field()
    model = Field()
    price = Field()
    hsf = Field()
    stories = Field()
    br = Field()
    ba = Field()
    half_bath = Field()
    ga = Field()

    qmi_address = Field()
    qmi_lot = Field()
