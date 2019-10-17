def parse_gender(response):
    title_text = response.css('title::text').get()
    categories = response.css('span.category::text').get().split('/')
    description = response.css('div#short_description_content p::text').getall()

    joined_text = f"{title_text} {' '.join(categories)} {' '.join(description)}"

    if any(gender in joined_text.lower() for gender in ['women', 'woman', 'misses', 'female', 'feminine']):
        return 'Women'
    elif any(gender in joined_text.lower() for gender in [' men', 'man', 'male', 'masculine']):
        return 'Men'

    return 'Unisex adult'
