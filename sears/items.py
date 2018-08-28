# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class ProductItem(Item):

    url = Field(type="str")
    referer_url = Field(default="", type="str")

    # 2-letter country codes (e.g. "US,FR,DE")
    country_code = Field(type="str", default=None)

    # unique identifier of Product-color variation in Webshop
    identifier = Field(type="str")
    old_identifier = Field(type="str")

    # merchant SKU
    sku = Field(type="str")

    # base of sku that is independent of color
    # (e.g. 41371610LP(red), 41371610QW(blue) --> base_sku = 41371610)
    # should be available on overview page to merge categories
    base_sku = Field(type="str")

    title = Field(type="str")
    brand = Field(type="str")
    description_text = Field(default="", type="str", delimiter="<br>")  # leave as list

    # binary product availability
    available = Field(default=True)

    # prices
    full_price_text = Field(default="", type="str")     # full/original price
    old_price_text = Field(default="", type="str")      # full/original price alternative
    new_price_text = Field(default="", type="str")      # current/discounted price
    currency = Field()                                  # 3-letter currency

    # local language description fields
    language_code = Field(type="str")

    # genders
    gender_names = Field(type="list")   # list of local gender names
    gender_identifiers = Field(type="list")  # (language independent) identifiers for mapping

    # color
    color_name = Field(type="str")  # color in local language, e.g. "sky blue"
    color_code = Field(type="str")  # color code as specified by retailer, if available (e.g. "W57")

    # categories
    category_names = Field(type="list")  # #list of categories in local language
    category_identifiers = Field(type="list")   # (language independent) identifiers for mapping

    # list of image urls to be downloaded, in high quality
    image_urls = Field(type="list")

    # sub directory for images and thumbnails (defaults to webshop, if not given).
    # format without slashes (e.g. "TheIconic")
    image_subdir = Field(type="str")

    # dictionay with additional info
    # format: {"attribute":"value", "attr2":"value2"}
    additional_info_dict = Field(type="dict")
    additional_attributes = Field(type="dict", export=True)

    # Info for size and availability collections
    # will be array of SizeItem objects
    size_infos = Field(type="list")

    # Set this flag to True, if prices should be taken from SizeItem
    # instead of ProductItem
    use_size_level_prices = Field(default=False)

    """
    ADVANCED FIELDS
    """
    # timestamp of request download -> will be added automatically
    timestamp = Field()

    # database ids (will be determined in pipeline where needed, if missing)
    product_id = Field()

    # product-specific keywords (sometimes in meta)
    keywords = Field(type="set", remove_duplicates=True)

    # Unique Product Code
    # TODO: Deprecate UPC field (merged into GTIN)
    upc = Field(type="str")

    # Will be calculated from convert_prices Pipeline
    old_price_value = Field(default=None)
    new_price_value = Field(default=None)
    full_price_value = Field(default=None)

    # level of category (e.g. 0=Clothes/Accessories, 1=shoes, 2=high heels
    category_levels = Field(type="list")
    # list of parent_identifiers
    # (each category can only have one parent), optional
    category_parents = Field(type="list")

    # RGB color code, if available
    rgb = Field(default="", type="str")
    material = Field(default="", type="str", delimiter=" ")
    pattern = Field(default="", type="str", delimiter=" ")
    measurements = Field(default="", type="str", delimiter=" ")

    # season of item in any language
    season = Field(type="str")

    # for market places such as Amazon, Google Shopping, Ebay
    third_party_vendor = Field(type="str")

    # uses spider.spider_info.webshop_code as default
    # (which uses spider name as default)
    webshop = Field(type="str")

    product_stock = Field()

    # For images pipeline, array in same order as image_urls
    image_descriptions = Field(type="list")

    # Boolean Flags for pipeline processing options -> will be set automatically by pipeline if NONE set
    update_details = Field(default=False)       # save product details (title, description, etc)
    save_price = Field(default=False)           # save prices
    save_availability = Field(default=False)    # save availability by size
    add_category_and_gender = Field(default=False)  # merge categories and genders in backend, by BASE_SKU

    # fill in currency from registered country, to double-check prices

    # Global Trade Identifier Number (GTIN, EAN, UPC, UPN, etc.), can be comma-separated list
    gtin = Field(type="list")

    # image_raw_data = Field(type="list")

    # fields for indicating that there is a price range by size,
    # ALL OPTIONAL, only for special cases where price range cannot be determined from sizes
    # use_size_level_prices: Set this flag to True, if price RANGE and to activate the following two fields

    # if price range, this value indicates the maximum. If left empty, then will be calculated from sizes
    max_original_price_value = Field(default=None)
    # if price range, this value indicates the maximum. If left empty, then will be calculated from sizes
    max_current_price_value = Field(default=None)

    # internal fields
    _item_id = Field()      # increasing item number for reference in CSV file
    _response = Field()      # response is added automatically by a middleware. Used for debug and log messages
    _original_price_value = Field()  # numeric value of original price
    _current_price_value = Field()  # numeric value of current (discounted) price
    _discount = Field()        # numeric value of discount in percent

    def __init__(self, *args, **kwargs):
        """Initialize the fields of types list, dict and set
           with default values if not given in kwargs
        """
        super(Item, self).__init__(*args, **kwargs)

        required_types = {'list': list, 'dict': dict, 'set': set}
        for field_name in self.fields:

            # skip if already initialized by super
            if field_name in self._values:
                continue

            field_type = required_types.get(
                self.fields[field_name].get('type')
            )
            if field_type:
                self.__setitem__(field_name, field_type())


# For size and availability
class SizeItem(Item):
    # Those prices will only be used if use_size_level_prices=True on
    # ProductItem
    size_original_price_text = Field(default="", type="str")
    size_current_price_text = Field(default="", type="str")

    # identifier for SKU-model + size
    size_identifier = Field(type="str")
    size_name = Field(type="str")
    # sometimes retailers provide several size descriptions
    alternative_size_name = Field(type="str")
    stock = Field()
    size_gtin = Field(type="str", default=None, export=True)

    # Only for pipeline use; the price values will be calculated from
    # price_text automatically in price pipeline
    size_original_price_value = Field(default="")
    size_current_price_value = Field(default="")
