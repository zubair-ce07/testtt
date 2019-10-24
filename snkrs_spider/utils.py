def get_gender(response, category, description):
    title_text = response.css('title::text').get()    
    joined_text = f"{title_text} {' '.join(category)} {' '.join(description)}"

    if any(gender in joined_text.lower() for gender in ['women', 'woman', 'misses', 'female', 'feminine']):
        return 'Women'
    elif any(gender in joined_text.lower() for gender in [' men', 'man', 'male', 'masculine']):
        return 'Men'

    return 'Unisex adult'
