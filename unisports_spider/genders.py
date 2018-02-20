from enum import Enum


class Gender(Enum):
    MEN = 'men'
    WOMEN = 'women'
    GIRLS = 'girls'
    BOYS = 'boys'
    KIDS = 'unisex-kids'
    ADULTS = 'unisex-adults'

GENDER_MAP = {
    'ru': {
        'девочкам': Gender.GIRLS.value,
        'мальчикам': Gender.BOYS.value,
        'женской': Gender.WOMEN.value,
        'девушка': Gender.GIRLS.value,  # Girl
        'девочек': Gender.GIRLS.value,  # girls
        'девочки': Gender.GIRLS.value,  # girls
        'мальчика': Gender.BOYS.value,  # boy
        'мальчиков': Gender.BOYS.value,  # boys
        'женщины': Gender.WOMEN.value,  # women
        'мужчины': Gender.MEN.value,   # men
        'дети': Gender.KIDS.value,     # children
        'малыши': Gender.KIDS.value,   # kids
        'него': Gender.MEN.value,      # him
        'мужская': Gender.MEN.value,   # man's
        'мальчики': Gender.BOYS.value,  # boys
        'детское': Gender.KIDS.value,  # children's
        'женская': Gender.WOMEN.value,  # female
        'женские': Gender.WOMEN.value,  # female
        'женщинам': Gender.WOMEN.value,# women
        'мужские': Gender.MEN.value,   # men's
        'мужчинам': Gender.MEN.value,  # men
        'новорожденных': Gender.KIDS.value,  # newborns
        'детские': Gender.KIDS.value,  # children's
        'мужской': Gender.MEN.value,   # male
        'женский': Gender.WOMEN.value,  # feminine
        'женщина': Gender.WOMEN.value,  # female
        'неё': Gender.WOMEN.value,     # her
        'мужчина': Gender.MEN.value,   # Man
        'детям': Gender.KIDS.value,    # children
        'женщин': Gender.WOMEN.value,  # women
        'юноши': Gender.BOYS.value,    # young men
        'мужчин': Gender.MEN.value,    # men
        'девушки': Gender.GIRLS.value,  # girls
        'мальчки': Gender.BOYS.value,  # boys
        'маленьких': Gender.KIDS.value,  # small
        'мамам': Gender.WOMEN.value,    # mothers
        'мужское': Gender.MEN.value,    # male
        'новорожденные': Gender.KIDS.value,  # newborns
        'мини': Gender.KIDS.value     # mini
    },
    'de': {
        'mädchen': Gender.GIRLS.value,   # girl
        'umstandsmode': Gender.WOMEN.value,  # maternity wear
        'damen': Gender.WOMEN.value,   # Ladies
        'kinder': Gender.KIDS.value,    # children
        'knaben': Gender.BOYS.value,    # boys
        'maedchen': Gender.GIRLS.value,  # girl
        'handtaschen': Gender.WOMEN.value,   # handbags
        'shopper': Gender.WOMEN.value,
        'jungen': Gender.BOYS.value,   # boys
        'madchen': Gender.GIRLS.value,     # girl
        'haar': Gender.WOMEN.value,      # her
        'herren': Gender.MEN.value,      # Men's
        'frauen': Gender.WOMEN.value,  # women
        'männer': Gender.MEN.value,    # men
        'jungs': Gender.BOYS.value,    # guys
        'blusen': Gender.WOMEN.value,
        'junge': Gender.BOYS.value,     # boy
        'schwangerschaft': Gender.WOMEN.value,   # pregnancy
        'umstands': Gender.WOMEN.value,   # maternity
        'frau': Gender.WOMEN.value,     # Mrs
        'mann': Gender.MEN.value,        # man
        'neugeborene': Gender.KIDS.value,  # newborn
        'damenschuhe': Gender.WOMEN.value,  # women's shoes
        'herrenschuhe': Gender.MEN.value,   # men's shoes
        'ihn': Gender.MEN.value,        # him
        'ihr': Gender.WOMEN.value       #her
    },
    'ja': {
        'メン': Gender.MEN.value,     # men
        'キッズ・ベビ': Gender.KIDS.value,  # Kids · Baby
        'ウィメン': Gender.WOMEN.value,     # Women
        'レディース': Gender.WOMEN.value,   # women
        '女性': Gender.WOMEN.value,   # female
        'レディ': Gender.WOMEN.value,   # Lady
        'マタニティ': Gender.WOMEN.value,  # Maternity
        'おとこ': Gender.MEN.value,    # man
        '男性': Gender.MEN.value,     # male
        '男性用': Gender.MEN.value,   # Male use
        'メンズ': Gender.MEN.value,     # mens
        '赤ちゃん': Gender.KIDS.value,   # baby
        '子供': Gender.KIDS.value,    # children
        'キッド': Gender.KIDS.value,   # Kid
        '子供たち': Gender.KIDS.value,  # The kids
        'ユニセックス': Gender.KIDS.value,  # unisex
        'ガールズ': Gender.GIRLS.value,    # Girls
        'ボーイズ': Gender.BOYS.value,    # Boys
        'キッズ': Gender.KIDS.value,     # Kids
        'ボーイ': Gender.BOYS.value,    # A boy
        '男の子': Gender.BOYS.value,    # boy
        '女の子': Gender.GIRLS.value,   # girl
        'ガール': Gender.GIRLS.value,    # Girl
        'レディス': Gender.WOMEN.value,  # Ladies
        'ウィメンズ': Gender.WOMEN.value,  # Women's
    },
    'it': {
        'donna': Gender.WOMEN.value,  # woman
        'donne': Gender.WOMEN.value,   #women
        'uomo': Gender.MEN.value,     # man
        'uomini': Gender.MEN.value,   #men
        'bambino': Gender.BOYS.value,  # child
        'bambina': Gender.GIRLS.value,  # child
        'ragazza': Gender.GIRLS.value,  # girl
        'ragazzo': Gender.BOYS.value,  # boy
        'neonato': Gender.KIDS.value,  # newborn
        'lui': Gender.MEN.value,         # he
        'lei': Gender.WOMEN.value,      # she
        'neonate': Gender.GIRLS.value,  # baby
        'ragazze': Gender.GIRLS.value,  # girls
        'ragazzi': Gender.BOYS.value,  # boys
        'bimba': Gender.GIRLS.value,  # infant
        'bimbo': Gender.BOYS.value,   # baby
        'intimo': Gender.WOMEN.value,  # intimate
        'premaman': Gender.WOMEN.value,  # Maternity
        'neonata': Gender.KIDS.value,   # baby girl
        'bambine': Gender.GIRLS.value,  # girls
        'neonati': Gender.KIDS.value,  # baby
        'bambini': Gender.KIDS.value,  # children
    },
    'pl': {
        'ona': Gender.WOMEN.value,  # she
        'on': Gender.MEN.value,     # he
        'dziewczynka': Gender.GIRLS.value,  # girl
        'chłopiec': Gender.BOYS.value,    # boy
        'dziecko': Gender.KIDS.value,     # child
        'kobiety': Gender.WOMEN.value,   # women
        'mężczyźni': Gender.MEN.value,   # men
        'dziewczynki': Gender.GIRLS.value,  # girl
        'dziewczynek': Gender.GIRLS.value,   # girls
        'chłopcy': Gender.BOYS.value,     # boys
        'chlopieca': Gender.BOYS.value,   # boy
        'chlopcow': Gender.BOYS.value,   # Boys
        'niemowlęta': Gender.KIDS.value,  # babies
        'niemowlę': Gender.KIDS.value,   # baby
        'kobieta': Gender.WOMEN.value,    # women
        'mężczyźna': Gender.MEN.value,    # man
        'dziewczęce': Gender.GIRLS.value,  # girls
        'chłopięce': Gender.BOYS.value,    # boys
        'mężczyzna': Gender.MEN.value,   # man
        'dzieci': Gender.KIDS.value,    # children
    },
    'cs': {
        'dívka': Gender.GIRLS.value,  # girl
        'chlapec': Gender.BOYS.value,  # boy
        'dítě': Gender.KIDS.value,    # child
    },
    'ro': {
        'femei': Gender.WOMEN.value,  # women
        'bărbaţi': Gender.MEN.value,   # men
        'fete': Gender.GIRLS.value,    # girls
        'băieţi': Gender.BOYS.value,    # boys
        'copii': Gender.KIDS.value,    # children
        'barbati': Gender.MEN.value,   # men
        'fetite': Gender.GIRLS.value,  # little girls
        'baieti': Gender.BOYS.value,  # boys
        'baietei': Gender.BOYS.value,  # boys
        'bărbat': Gender.MEN.value,    # man
        'fetiţe': Gender.GIRLS.value,  # little girls
        'fată': Gender.GIRLS.value,     # girl
        'băiat': Gender.BOYS.value,    # boy
        'bebeluşi': Gender.KIDS.value,  # baby
    },
    'fr': {
        'elle': Gender.WOMEN.value,
        'lui': Gender.MEN.value,
        'enfant': Gender.KIDS.value,  # new_entry
        'homme': Gender.MEN.value,   # man
        'femme': Gender.WOMEN.value,  # man
        'garçon': Gender.BOYS.value,  # boy
        'bébé': Gender.KIDS.value,   # baby
        'garcon': Gender.BOYS.value,  # boy
        'filles': Gender.GIRLS.value,  # girls
        'chicas': Gender.GIRLS.value,  # girls
        'niñas': Gender.GIRLS.value,  # little girls
        'ninas': Gender.GIRLS.value,  # girls
        'bambine': Gender.GIRLS.value,  # girls
        'ragazze': Gender.GIRLS.value,  # girls
        'ragazzi': Gender.BOYS.value,   # boys
        'kinder': Gender.KIDS.value,   # children
        'bebé': Gender.KIDS.value,     # baby
        'bebe': Gender.KIDS.value,     # baby
        'niños': Gender.KIDS.value,   # children
        'ninos': Gender.KIDS.value,   # children
        'neonati': Gender.KIDS.value,  # Baby
        'bambini': Gender.KIDS.value,   # children
        'maternité': Gender.WOMEN.value,  # maternity
        'maternite': Gender.WOMEN.value,  # maternity
        'maquillage': Gender.WOMEN.value,  # makeup
        'maman': Gender.WOMEN.value,    # mom
        'naissance': Gender.KIDS.value,  # birth
        'adulte': Gender.ADULTS.value,   # adult
        'enfant': Gender.KIDS.value,    # child
        'femmes': Gender.WOMEN.value,  # women
        'hommes': Gender.MEN.value,     # men
        'garcons': Gender.BOYS.value,   # boys
        'garçons': Gender.BOYS.value,   # boys
        'fille': Gender.GIRLS.value,    # girl
    },
    'es': {
        'él': Gender.MEN.value,
        'ella': Gender.WOMEN.value,
        'nino': Gender.BOYS.value,  # boy
        'niño': Gender.BOYS.value,   # boy
        'nina': Gender.GIRLS.value,  # girl
        'niña': Gender.GIRLS.value,   # girl
        'mujer': Gender.WOMEN.value,  # woman
        'hombre': Gender.MEN.value,   # man
        'dama': Gender.WOMEN.value,   # Lady
        'caballero': Gender.MEN.value,  # gentleman
        'baño': Gender.WOMEN.value,    # bath
        'damen': Gender.WOMEN.value,   # Ladies
        'lingerie': Gender.WOMEN.value,  # lingerie
        'haar': Gender.WOMEN.value,  # her
        'femmes': Gender.WOMEN.value,  # women
        'herren': Gender.MEN.value,   # Men's
        'hommes': Gender.MEN.value,  # men
        'herrer': Gender.MEN.value,  # gentlemen
        'hem': Gender.MEN.value,     # him
        'jungen': Gender.BOYS.value,  # boys
        'garcons': Gender.BOYS.value,  # boys
        'garçons': Gender.BOYS.value,  # boys
        'mädchen': Gender.GIRLS.value,  # girl
        'fille': Gender.GIRLS.value,  # girl
        'bambine': Gender.GIRLS.value,  # girls
        'ragazze': Gender.GIRLS.value,  # girls
        'ragazzi': Gender.BOYS.value,   # boys
        'kinder': Gender.KIDS.value,   # children
        'neonati': Gender.KIDS.value,  # Baby
        'bambini': Gender.KIDS.value,  # children
        'maternidad': Gender.WOMEN.value,  # maternity
        'nia': Gender.GIRLS.value,   # no translation
        'nio': Gender.BOYS.value,    # child
        'femenino': Gender.WOMEN.value,  # female
        'infantil': Gender.KIDS.value,  # childish
        'belleza': Gender.WOMEN.value,  # beauty
        'chicos': Gender.BOYS.value,   # Boys
        'chicas': Gender.GIRLS.value,  # girls
        'ninas': Gender.GIRLS.value,   # little girls
        'niños': Gender.KIDS.value,    # children
        'ninos': Gender.KIDS.value,    # children
        'niñas': Gender.GIRLS.value,  # little girls
        'bebé': Gender.KIDS.value,  # baby
        'bebe': Gender.KIDS.value,  # baby
        'bebes': Gender.KIDS.value,  # baby
    },
    'hu': {
        'női': Gender.WOMEN.value,  # female
        'férfi': Gender.MEN.value,  # man
        'lány': Gender.GIRLS.value,  # girl
        'fiú': Gender.BOYS.value,   # boy
        'gyerek': Gender.KIDS.value,  # Child
        'uniszex': Gender.ADULTS.value,  # unisex
        'gyermek': Gender.KIDS.value,  # child
    },
    'tr': {
        'kadın': Gender.WOMEN.value,  # woman
        'erkek': Gender.MEN.value,    # male
        'kadin': Gender.WOMEN.value,  # woman
        'yenidoğan': Gender.KIDS.value,  # newborn
        'kız': Gender.GIRLS.value,    # girl
        'çocuk': Gender.KIDS.value,   # child
        'bebek': Gender.KIDS.value,  # baby
    },
    'sv': {
        'kvinnor': Gender.WOMEN.value,  # women
        'män': Gender.MEN.value,    # men
        'barn': Gender.KIDS.value,   # children
        'kvinna': Gender.WOMEN.value,  # men...
        'dam': Gender.WOMEN.value,  # Lady
        'herr': Gender.MEN.value,    # Mr.
        'flicka': Gender.GIRLS.value,  # girl
        'henne': Gender.WOMEN.value,   # her
        'skönhet': Gender.WOMEN.value,  # beauty
        'flickor': Gender.GIRLS.value,  # girls
        'pojkar': Gender.BOYS.value,   # boys
        'flick': Gender.GIRLS.value,  # Baby
        'pojk': Gender.BOYS.value,    # boy
        'tjej': Gender.GIRLS.value,  # girl
        'kille': Gender.BOYS.value,  # boy
    },
    'no': {
        'kvinner': Gender.WOMEN.value,  # women
        'menn': Gender.MEN.value,    # men
        'barn': Gender.KIDS.value,   # children
        'dame': Gender.WOMEN.value,  # lady
        'herre': Gender.MEN.value,  # master
        'jente': Gender.GIRLS.value,  # girl
        'gutt': Gender.BOYS.value,   # boy
        'henne': Gender.WOMEN.value,  # her
        'skjønnhet': Gender.WOMEN.value,   # beauty
        'jenter': Gender.GIRLS.value,  # girls
        'gutter': Gender.BOYS.value,   # boys
        'kvinne': Gender.WOMEN.value,  # woman
        'mann': Gender.MEN.value,   # man
        'herrer': Gender.MEN.value,  # gentlemen
    },
    'da': {
        'kvinder': Gender.WOMEN.value,  # women
        'børn': Gender.KIDS.value,  # new_entry
        'mænd': Gender.MEN.value,    # men
        'kvinde': Gender.WOMEN.value,  # woman
        'herre': Gender.MEN.value,  # master
        'dame': Gender.WOMEN.value,  # Lady
        'hende': Gender.WOMEN.value,  # her
        'herr': Gender.MEN.value,   # Mr.
        'pige': Gender.GIRLS.value,  # girl
        'dreng': Gender.BOYS.value,  # boy
        'skønhed': Gender.WOMEN.value,  # beauty
        'damen': Gender.WOMEN.value,  # ady
        'lingerie': Gender.WOMEN.value,
        'her': Gender.WOMEN.value,  # her
        'haar': Gender.WOMEN.value,  # her
        'femmes': Gender.WOMEN.value,  # women
        'herren': Gender.MEN.value,  # Men's
        'hommes': Gender.MEN.value,  # men
        'herrer': Gender.MEN.value,  # gentlemen
        'hem': Gender.MEN.value,   # him
        'him': Gender.MEN.value,  # him
        'jungen': Gender.BOYS.value,  # boys
        'chicos': Gender.BOYS.value,  # Boys
        'garcons': Gender.BOYS.value,  # boys
        'garçons': Gender.BOYS.value,  # boys
        'mädchen': Gender.GIRLS.value,  # girl
        'chicas': Gender.GIRLS.value,  # girls
        'niñas': Gender.GIRLS.value,  # little girls
        'ninas': Gender.GIRLS.value,  # girls
        'fille': Gender.GIRLS.value,   # girl
        'bambine': Gender.GIRLS.value,  # girls
        'ragazze': Gender.GIRLS.value,  # girls
        'ragazzi': Gender.BOYS.value,    # boys
        'kinder': Gender.KIDS.value,   # children
        'bebé': Gender.KIDS.value,   # baby
        'bebe': Gender.KIDS.value,   # baby
        'niños': Gender.KIDS.value,  # children
        'ninos': Gender.KIDS.value,  # children
        'neonati': Gender.KIDS.value,  # Baby
        'bambini': Gender.KIDS.value,  # children
        'mand': Gender.MEN.value   # male
    },
    'fi': {
        'naiset': Gender.WOMEN.value,  # ladies
        'lapset': Gender.KIDS.value,  # new_entry
        'miehet': Gender.MEN.value,   # gentlemen
        'naisille': Gender.WOMEN.value,  # for women
        'tytöt': Gender.GIRLS.value,   # the girls
        'pojat': Gender.BOYS.value,    # the boys
        'kauneus': Gender.WOMEN.value,   # beauty
    },
    'zh': {
        '女士': Gender.WOMEN.value,  # Ms
        '男士': Gender.MEN.value,  # Men
        '女童': Gender.GIRLS.value,  # Girls
        '婴儿': Gender.KIDS.value,  # baby
        '女装': Gender.WOMEN.value,   # Women
        '孕妇装': Gender.WOMEN.value,  # Maternity wear
        '男装': Gender.MEN.value,   # Men's
        '男孩': Gender.BOYS.value,   # boy
        '男幼': Gender.BOYS.value,  # Male young
        '女孩': Gender.GIRLS.value,  # Male youth
        '女幼': Gender.GIRLS.value,  # Young girl
        '女': Gender.WOMEN.value,   # Female
        '女式': Gender.WOMEN.value,  # Women
        '男童': Gender.BOYS.value  # Boy
    },
    'nl': {
        'dames': Gender.WOMEN.value,  # Women
        'vrouwen': Gender.WOMEN.value,  # new_entry
        'heren': Gender.MEN.value,  # Gentlemen
        'meisjes': Gender.GIRLS.value,   # girls
        'jongens': Gender.BOYS.value,    # boys
        'dame': Gender.WOMEN.value,  # Lady
        'manne': Gender.MEN.value,   # men
        'jongen': Gender.BOYS.value,  # boy
        'kinderen': Gender.KIDS.value,  # children
        'damen': Gender.WOMEN.value,   # Ladies
        'femmes': Gender.WOMEN.value,   # women
        'herren': Gender.MEN.value,    # Men's
        'hommes': Gender.MEN.value,    # men
        'herrer': Gender.MEN.value,   # gentlemen
        'jungen': Gender.BOYS.value,  # boys
        'chicos': Gender.BOYS.value,  # Boys
        'garcons': Gender.BOYS.value,  # boys
        'garçons': Gender.BOYS.value,  # boys
        'mädchen': Gender.GIRLS.value,  # girl
        'chicas': Gender.GIRLS.value,  # girls
        'niñas': Gender.GIRLS.value,  # little girls
        'ninas': Gender.GIRLS.value,  # girls
        'fille': Gender.GIRLS.value,   # girl
        'bambine': Gender.GIRLS.value,  # girls
        'ragazze': Gender.GIRLS.value,  # girls
        'ragazzi': Gender.BOYS.value,   # boys
        'kinder': Gender.KIDS.value,    # children
        'bebé': Gender.KIDS.value,     # baby
        'bebe': Gender.KIDS.value,      # baby
        'niños': Gender.KIDS.value,   # children
        'ninos': Gender.KIDS.value,   # children
        'neonati': Gender.KIDS.value,  # Baby
        'bambini': Gender.KIDS.value,   # children
        'mammae': Gender.WOMEN.value,  # mom and
        'meisje': Gender.GIRLS.value,  # girl
        'meisjen': Gender.GIRLS.value,  # girls
        'haar': Gender.WOMEN.value,  # her
        'hem': Gender.MEN.value,   # him
    },
    'pt': {
        'ele': Gender.MEN.value,
        'ela': Gender.WOMEN.value,
        'feminina': Gender.WOMEN.value,  # feminine
        'masculina': Gender.MEN.value,   # masculine
        'menina': Gender.GIRLS.value,     # girl
        'meninas': Gender.GIRLS.value,     # girls
        'menino': Gender.BOYS.value,     # boy
        'meninos': Gender.BOYS.value,     # boys
        'beleza': Gender.WOMEN.value,    # beauty
        'feminino': Gender.WOMEN.value,  # female
        'mulher': Gender.WOMEN.value,   # woman
        'homem': Gender.MEN.value,      # men
        'rapaz': Gender.BOYS.value,     # boy
        'criança': Gender.KIDS.value,     # child
        'senhora': Gender.WOMEN.value,   # Mrs
        'masculin': Gender.MEN.value,   # male
        'masculino': Gender.MEN.value,   # male
        'pai': Gender.MEN.value,     # dad
        'rapariga': Gender.GIRLS.value,  # girl
        'bebé': Gender.KIDS.value,   # baby
        'crianças': Gender.KIDS.value,  # children
        'infantil': Gender.KIDS.value,   # childlike
        'unissex': Gender.KIDS.value,    # unisex
    },
    'en': {
        'womans': Gender.WOMEN.value,
        'mans': Gender.MEN.value,
        'lady': Gender.WOMEN.value,
        'shopbyproductladies': Gender.WOMEN.value,
        'trf': Gender.WOMEN.value,
        'male': Gender.MEN.value,
        'female': Gender.WOMEN.value,
        'babys': Gender.KIDS.value,
        'beauty': Gender.WOMEN.value,
        'babies': Gender.KIDS.value,
        'clutches': Gender.WOMEN.value,
        'kidswear': Gender.KIDS.value,
        'boyfriend': Gender.WOMEN.value,
        'womens': Gender.WOMEN.value,
        'mens': Gender.MEN.value,
        'maternity': Gender.WOMEN.value,
        'toddler': Gender.KIDS.value,
        'toddlers': Gender.KIDS.value,
        'ballerinas': Gender.WOMEN.value,
        'beachwear': Gender.WOMEN.value,
        'aerie': Gender.WOMEN.value,
        'bra': Gender.WOMEN.value,
        'him': Gender.MEN.value,
        'women': Gender.WOMEN.value,
        'kids': Gender.KIDS.value,
        'girl': Gender.GIRLS.value,
        'boy': Gender.BOYS.value,
        'lingerie': Gender.WOMEN.value,
        'infant': Gender.KIDS.value,
        'enfant': Gender.KIDS.value,
        'mixed': Gender.KIDS.value,
        'man': Gender.MEN.value,
        'newborn': Gender.KIDS.value,
        'forher': Gender.WOMEN.value,
        'children': Gender.KIDS.value,
        'plussize': Gender.WOMEN.value,
        'woman': Gender.WOMEN.value,
        'boys': Gender.BOYS.value,
        'girls': Gender.GIRLS.value,
        'ladies': Gender.WOMEN.value,
        'men': Gender.MEN.value,
        'babygirl': Gender.GIRLS.value,
        'babyboy': Gender.BOYS.value,
        'kidsgirls': Gender.GIRLS.value,
        'kidsboys': Gender.BOYS.value,
        'bride': Gender.WOMEN.value,
        'guys': Gender.BOYS.value,
        'junior': Gender.BOYS.value,
        'kid': Gender.BOYS.value,
        'baby': Gender.BOYS.value,
        'her': Gender.WOMEN.value,
        'teen': Gender.KIDS.value
    },
    'bg': {
        'жени': Gender.WOMEN.value,   # women
        'мъже': Gender.MEN.value,    # men
        'деца': Gender.KIDS.value,   # children
    },
    'cn': {
        '女': Gender.WOMEN.value,  # Female
        '男': Gender.MEN.value,   # male
        '男童': Gender.BOYS.value,  # Boy
        '女童': Gender.GIRLS.value,  # Girls
        '学步': Gender.KIDS.value,   # Toddler
        '儿童': Gender.KIDS.value,   # child
        '婴儿': Gender.KIDS.value,   # baby
        '女装': Gender.WOMEN.value,  # Women
        '孕产妇': Gender.WOMEN.value,  # pregnant woman
        '男装': Gender.MEN.value,   # Men's
        '女婴': Gender.GIRLS.value,  # Baby girl
        '男婴': Gender.BOYS.value,   # Baby boy
        '童装': Gender.KIDS.value,   # Children's wear
        '宝宝': Gender.KIDS.value,   # baby
        '子': Gender.KIDS.value,  # child
    },
    'ko': {
        '여성': Gender.WOMEN.value,  # female
        '남성': Gender.MEN.value,   # male
        '여아': Gender.GIRLS.value,  # Girl
        '아동': Gender.KIDS.value,   # child
    },
    'sk': {
        'ladies': Gender.WOMEN.value,
        'men': Gender.MEN.value,
        'babygirl': Gender.GIRLS.value,
        'babyboy': Gender.BOYS.value,
        'women': Gender.WOMEN.value,
        'woman': Gender.WOMEN.value,
        'boyfriend': Gender.WOMEN.value,
        'boy': Gender.BOYS.value,
        'girl': Gender.GIRLS.value,
        'kid': Gender.KIDS.value,
        'baby': Gender.KIDS.value,
        'enfant': Gender.KIDS.value,
        'man': Gender.MEN.value
    },
    'id': {
        'bayi': Gender.KIDS.value,   # baby
        'laki': Gender.BOYS.value,   # men
        'perempuan': Gender.GIRLS.value,  # women
        'hamil': Gender.WOMEN.value     # pregnant
    },
    'uk': {
        'hемовлята': Gender.KIDS.value,  # babies
        'дівчата': Gender.GIRLS.value,   # girls
        'хлопчики': Gender.BOYS.value,   # boys
        'мамам': Gender.WOMEN.value      # mothers
    }
}


def get_gender_map(lang, gender_map, use_en_map=True):
    #  All gender maps from now onwards are in dictionary format rather than
    #  the list of tuples format that was being used before

    if isinstance(gender_map, list):
        gender_map = {gender_str: gender for gender_str, gender in gender_map}

    gender_map_en = GENDER_MAP.get("en")
    gender_map_extended = add_gender_maps(gender_map_en, gender_map)
    if lang == "en":
        return gender_map_extended

    gender_map_locale = GENDER_MAP.get(lang)
    if not gender_map_locale:
        return gender_map_extended

    gender_map_locale_extended = add_gender_maps(gender_map_locale, gender_map)
    if not use_en_map:
        return gender_map_locale_extended

    return add_gender_maps(gender_map_en, gender_map_locale_extended)


def add_gender_maps(gender_map1, gender_map2):
    gender_map = gender_map1.copy()
    gender_map.update(gender_map2)
    return gender_map
