def parse_gender(response):
    title_text = response.css('title::text').get()
    size_categories = response.css('#sizecat a::text').getall()

    description = response.css('span[itemprop="description"] p::text').getall()
    joined_text = f"{title_text} {' '.join(size_categories)} {' '.join(description)}"

    if any(gender in joined_text.lower() for gender in ['women', 'woman', 'misses', 'female', 'feminine']):
        return 'Women'
    elif any(gender in joined_text.lower() for gender in [' men', 'man', 'male', 'masculine']):
        return 'Men'

    return 'Unisex adult'
