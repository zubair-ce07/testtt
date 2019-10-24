def get_gender(response, description):
    title_text = response.css('title::text').get()
    size_categories = response.css('#sizecat a::text').getall()
    
    joined_text = f"{title_text} {' '.join(size_categories)} {' '.join(description)}"

    if any(gender in joined_text.lower() for gender in ['women', 'woman', 'misses', 'female', 'feminine']):
        return 'Women'
    elif any(gender in joined_text.lower() for gender in [' men', 'man', 'male', 'masculine']):
        return 'Men'

    return 'Unisex adult'


def get_size(response, size_id):
    css = f'a[id$="{size_id}"]::text, #size .basesize::text'
    return response.css(css).get()


def get_color(response, color_id):
    css = f'img[id="color_{color_id}"] + div > span::text, #color .basesize::text'
    return response.css(css).get()
