def parse_gender(gender_text):
    FEMALE_KEYWORDS = ['women', 'woman', 'misses', 'female', 'feminine']
    MALE_KEYWORDS = [' men', 'man', 'male', 'masculine']    

    if any(gender in gender_text.lower() for gender in FEMALE_KEYWORDS):
        return 'Women'
    elif any(gender in gender_text.lower() for gender in MALE_KEYWORDS):
        return 'Men'

    return 'Unisex adult'
