def parse_gender(response):
    description = response.css('div.description p::text').getall()
    xpath = '//span[contains(text(), "Gender")]/following-sibling::span/text()'
    gender = response.xpath(xpath).get()
    title_text = response.css('title::text').get()    

    joined_text = f"{gender} {title_text} {' '.join(description)}"

    if any(gender in joined_text.lower() for gender in ['women', 'woman', 'misses', 'female', 'feminine']):
        return 'Women'
    elif any(gender in joined_text.lower() for gender in [' men', 'man', 'male', 'masculine']):
        return 'Men'

    return 'Unisex adult'
