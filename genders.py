from enum import Enum


class Gender(Enum):
    MEN = 'men'
    WOMEN = 'women'
    GIRLS = 'girls'
    BOYS = 'boys'
    KIDS = 'unisex-kids'
    ADULTS = 'unisex-adults'


GENDER_MAP = {
    'fa': {
        'زنانه': Gender.WOMEN.value,
        'خانم ها': Gender.WOMEN.value,
        'خانم': Gender.WOMEN.value,
        'زنان': Gender.WOMEN.value,
        'آقایان': Gender.MEN.value,
        'مردان': Gender.MEN.value,
        'مردانه': Gender.MEN.value,
        'نوجوان': Gender.KIDS.value,
        'کودکان': Gender.KIDS.value,
        'کودک': Gender.KIDS.value,
        'بچه گانه': Gender.KIDS.value,
        'بچه': Gender.KIDS.value,
        'پسرانه': Gender.BOYS.value,
        'دخترانه': Gender.GIRLS.value,
        'نوزاد': Gender.KIDS.value,
    },
    'ru': {
        'девочкам': Gender.GIRLS.value,
        'мальчикам': Gender.BOYS.value,
        'женской': Gender.WOMEN.value,
        'zhenskaja': Gender.WOMEN.value,
        'девушка': Gender.GIRLS.value,
        'девочек': Gender.GIRLS.value,
        'девочки': Gender.GIRLS.value,
        'мальчика': Gender.BOYS.value,
        'мальчиков': Gender.BOYS.value,
        'женщины': Gender.WOMEN.value,
        'мужчины': Gender.MEN.value,
        'muzhskaja': Gender.MEN.value,
        'дети': Gender.KIDS.value,
        'малыши': Gender.KIDS.value,
        'него': Gender.MEN.value,
        'мужская': Gender.MEN.value,
        'мальчики': Gender.BOYS.value,
        'детское': Gender.KIDS.value,
        'женская': Gender.WOMEN.value,
        'женские': Gender.WOMEN.value,
        'женщинам': Gender.WOMEN.value,
        'мужские': Gender.MEN.value,
        'мужчинам': Gender.MEN.value,
        'новорожденных': Gender.KIDS.value,
        'детские': Gender.KIDS.value,
        'мужской': Gender.MEN.value,
        'женский': Gender.WOMEN.value,
        'женщина': Gender.WOMEN.value,
        'неё': Gender.WOMEN.value,
        'мужчина': Gender.MEN.value,
        'детям': Gender.KIDS.value,
        'женщин': Gender.WOMEN.value,
        'юноши': Gender.BOYS.value,
        'мужчин': Gender.MEN.value,
        'девушки': Gender.GIRLS.value,
        'мальчки': Gender.BOYS.value,
        'маленьких': Gender.KIDS.value,
        'мамам': Gender.WOMEN.value,
        'мужское': Gender.MEN.value,
        'новорожденные': Gender.KIDS.value,
        'детская': Gender.KIDS.value,
        'детский': Gender.KIDS.value,
        'мини': Gender.KIDS.value,
        'женское': Gender.WOMEN.value,
        'Бюстгаль': Gender.WOMEN.value
    },
    'de': {
        'kinderschmuck': Gender.KIDS.value,
        'kindermütze': Gender.KIDS.value,
        'mädchen': Gender.GIRLS.value,
        'umstandsmode': Gender.WOMEN.value,
        'damen': Gender.WOMEN.value,
        'damenjacke': Gender.WOMEN.value,
        'damenshirt': Gender.WOMEN.value,
        'umhängetaschen': Gender.WOMEN.value,
        'kinder': Gender.KIDS.value,
        'knaben': Gender.BOYS.value,
        'maedchen': Gender.GIRLS.value,
        'handtaschen': Gender.WOMEN.value,
        'shopper': Gender.WOMEN.value,
        'jungen': Gender.BOYS.value,
        'madchen': Gender.GIRLS.value,
        'haar': Gender.WOMEN.value,
        'herren': Gender.MEN.value,
        'frauen': Gender.WOMEN.value,
        'männer': Gender.MEN.value,
        'jungs': Gender.BOYS.value,
        'blusen': Gender.WOMEN.value,
        'junge': Gender.BOYS.value,
        'schwangerschaft': Gender.WOMEN.value,
        'umstands': Gender.WOMEN.value,
        'frau': Gender.WOMEN.value,
        'mann': Gender.MEN.value,
        'neugeborene': Gender.KIDS.value,
        'damenschuhe': Gender.WOMEN.value,
        'herrenschuhe': Gender.MEN.value,
        'ihn': Gender.MEN.value,
        'herrenhose': Gender.MEN.value,
        'ihr': Gender.WOMEN.value,
        'jungenmodell': Gender.BOYS.value,
        'mädels': Gender.GIRLS.value,
        'mädchenherzen': Gender.GIRLS.value,
        'tochter': Gender.GIRLS.value,
        'mädchenkeid': Gender.GIRLS.value,
        'her': ''  # We're putting this here because it coincides with the english word her
    },
    'ja': {
        'メン': Gender.MEN.value,
        'ｍen': Gender.MEN.value,
        'キッズ・ベビ': Gender.KIDS.value,
        'ウィメン': Gender.WOMEN.value,
        'レディース': Gender.WOMEN.value,
        '女性': Gender.WOMEN.value,
        'レディ': Gender.WOMEN.value,
        'マタニティ': Gender.WOMEN.value,
        'おとこ': Gender.MEN.value,
        '男性': Gender.MEN.value,
        '男性用': Gender.MEN.value,
        'メンズ': Gender.MEN.value,
        '赤ちゃん': Gender.KIDS.value,
        '子供': Gender.KIDS.value,
        'キッド': Gender.KIDS.value,
        '子供たち': Gender.KIDS.value,
        'ユニセックス': Gender.KIDS.value,
        'ガールズ': Gender.GIRLS.value,
        'ボーイズ': Gender.BOYS.value,
        'キッズ': Gender.KIDS.value,
        'ボーイ': Gender.BOYS.value,
        '男の子': Gender.BOYS.value,
        '女の子': Gender.GIRLS.value,
        '女の': Gender.GIRLS.value,
        'ガール': Gender.GIRLS.value,
        'レディス': Gender.WOMEN.value,
        'ウィメンズ': Gender.WOMEN.value,
        'ベビーシュ': Gender.KIDS.value,
        'ウイメン': Gender.WOMEN.value,
        'ブイイー': Gender.BOYS.value,
        'ベビー': Gender.KIDS.value,
        '女': Gender.WOMEN.value
    },
    'it': {
        'donna': Gender.WOMEN.value,
        'donne': Gender.WOMEN.value,
        'uomo': Gender.MEN.value,
        'uomini': Gender.MEN.value,
        'bambino': Gender.BOYS.value,
        'bambina': Gender.GIRLS.value,
        'ragazza': Gender.GIRLS.value,
        'ragazzo': Gender.BOYS.value,
        'neonato': Gender.KIDS.value,
        'lui': Gender.MEN.value,
        'lei': Gender.WOMEN.value,
        'neonate': Gender.GIRLS.value,
        'ragazze': Gender.GIRLS.value,
        'ragazzi': Gender.BOYS.value,
        'ragazzini': Gender.BOYS.value,
        'bimba': Gender.GIRLS.value,
        'bimbo': Gender.BOYS.value,
        'premaman': Gender.WOMEN.value,
        'neonata': Gender.GIRLS.value,
        'bambine': Gender.GIRLS.value,
        'neonati': Gender.KIDS.value,
        'bambini': Gender.KIDS.value,
        'regali per lei': Gender.WOMEN.value
    },
    'pl': {
        'ona': Gender.WOMEN.value,
        'on': Gender.MEN.value,
        'męskie': Gender.MEN.value,
        'dziewczynka': Gender.GIRLS.value,
        'dziewcząt': Gender.GIRLS.value,
        'chłopiec': Gender.BOYS.value,
        'dziecko': Gender.KIDS.value,
        'kobiety': Gender.WOMEN.value,
        'mężczyźni': Gender.MEN.value,
        'mężczyżni': Gender.MEN.value,
        'dziewczynki': Gender.GIRLS.value,
        'dziewczynek': Gender.GIRLS.value,
        'chłopcy': Gender.BOYS.value,
        'chlopieca': Gender.BOYS.value,
        'chlopiec': Gender.BOYS.value,
        'chlopcow': Gender.BOYS.value,
        'chłopaków': Gender.BOYS.value,
        'niemowlęta': Gender.KIDS.value,
        'niemowlęt': Gender.KIDS.value,
        'niemowlę': Gender.KIDS.value,
        'kobieta': Gender.WOMEN.value,
        'kobiet': Gender.WOMEN.value,
        'mężczyźna': Gender.MEN.value,
        'dziewczęce': Gender.GIRLS.value,
        'chłopięce': Gender.BOYS.value,
        'mężczyzna': Gender.MEN.value,
        'mężczyzn': Gender.MEN.value,
        'dzieci': Gender.KIDS.value,
        'dziecięce': Gender.KIDS.value,
        'damskie': Gender.WOMEN.value,
        'stanik': Gender.WOMEN.value,
        'staniczek': Gender.WOMEN.value,
        'damska': Gender.WOMEN.value,
        'damski': Gender.WOMEN.value,
        'męski': Gender.MEN.value,
        'męska': Gender.MEN.value,
        'dziewczęca': Gender.GIRLS.value,
        'juniorskie': Gender.KIDS.value,
        'dorosły': Gender.ADULTS.value,
    },
    'cs': {
        'dívky': Gender.GIRLS.value,
        'dívka': Gender.GIRLS.value,
        'chlapec': Gender.BOYS.value,
        'dítě': Gender.KIDS.value,
        'holčičky': Gender.GIRLS.value,
    },
    'ro': {
        'femei': Gender.WOMEN.value,
        'bărbaţi': Gender.MEN.value,
        'bărbați': Gender.MEN.value,
        'fete': Gender.GIRLS.value,
        'băieţi': Gender.BOYS.value,
        'copii': Gender.KIDS.value,
        'barbati': Gender.MEN.value,
        'fetite': Gender.GIRLS.value,
        'baieti': Gender.BOYS.value,
        'baietei': Gender.BOYS.value,
        'bărbat': Gender.MEN.value,
        'fetiţe': Gender.GIRLS.value,
        'fată': Gender.GIRLS.value,
        'băiat': Gender.BOYS.value,
        'bebeluşi': Gender.KIDS.value,
    },
    'fr': {
        'elle': Gender.WOMEN.value,
        'lui': Gender.MEN.value,
        'homme': Gender.MEN.value,
        'femme': Gender.WOMEN.value,
        'garçon': Gender.BOYS.value,
        'bébé': Gender.KIDS.value,
        'garcon': Gender.BOYS.value,
        'filles': Gender.GIRLS.value,
        'chicas': Gender.GIRLS.value,
        'niñas': Gender.GIRLS.value,
        'ninas': Gender.GIRLS.value,
        'niña': Gender.GIRLS.value,
        'nina': Gender.GIRLS.value,
        'bambine': Gender.GIRLS.value,
        'ragazze': Gender.GIRLS.value,
        'ragazzi': Gender.BOYS.value,
        'kinder': Gender.KIDS.value,
        'bebé': Gender.KIDS.value,
        'bebe': Gender.KIDS.value,
        'niños': Gender.KIDS.value,
        'ninos': Gender.KIDS.value,
        'neonati': Gender.KIDS.value,
        'bambini': Gender.KIDS.value,
        'maternité': Gender.WOMEN.value,
        'maternite': Gender.WOMEN.value,
        'maquillage': Gender.WOMEN.value,
        'maman': Gender.WOMEN.value,
        'naissance': Gender.KIDS.value,
        'adulte': Gender.ADULTS.value,
        'enfant': Gender.KIDS.value,
        'femmes': Gender.WOMEN.value,
        'hommes': Gender.MEN.value,
        'garcons': Gender.BOYS.value,
        'garçons': Gender.BOYS.value,
        'fille': Gender.GIRLS.value,
        'pour elle': Gender.WOMEN.value,
        'mum': Gender.WOMEN.value,
    },
    'es': {
        'él': Gender.MEN.value,
        'mujeres': Gender.WOMEN.value,
        'hombres': Gender.MEN.value,
        'ella': Gender.WOMEN.value,
        'nino': Gender.BOYS.value,
        'niño': Gender.BOYS.value,
        'nina': Gender.GIRLS.value,
        'niña': Gender.GIRLS.value,
        'mujer': Gender.WOMEN.value,
        'hombre': Gender.MEN.value,
        'dama': Gender.WOMEN.value,
        'caballero': Gender.MEN.value,
        'damen': Gender.WOMEN.value,
        'lingerie': Gender.WOMEN.value,
        'haar': Gender.WOMEN.value,
        'femmes': Gender.WOMEN.value,
        'herren': Gender.MEN.value,
        'hommes': Gender.MEN.value,
        'herrer': Gender.MEN.value,
        'masculino': Gender.MEN.value,
        'hem': Gender.MEN.value,
        'jungen': Gender.BOYS.value,
        'garcons': Gender.BOYS.value,
        'garçons': Gender.BOYS.value,
        'mädchen': Gender.GIRLS.value,
        'fille': Gender.GIRLS.value,
        'bambine': Gender.GIRLS.value,
        'ragazze': Gender.GIRLS.value,
        'ragazzi': Gender.BOYS.value,
        'kinder': Gender.KIDS.value,
        'neonati': Gender.KIDS.value,
        'bambini': Gender.KIDS.value,
        'maternidad': Gender.WOMEN.value,
        'nia': Gender.GIRLS.value,
        'nio': Gender.BOYS.value,
        'femenino': Gender.WOMEN.value,
        'infantil': Gender.KIDS.value,
        'belleza': Gender.WOMEN.value,
        'chico': Gender.BOYS.value,
        'chica': Gender.GIRLS.value,
        'chicos': Gender.BOYS.value,
        'chicas': Gender.GIRLS.value,
        'ninas': Gender.GIRLS.value,
        'niños': Gender.KIDS.value,
        'ninos': Gender.KIDS.value,
        'niñas': Gender.GIRLS.value,
        'bebé': Gender.KIDS.value,
        'bebe': Gender.KIDS.value,
        'bebes': Gender.KIDS.value,
        'ellas': Gender.WOMEN.value,
        'ellos': Gender.MEN.value,
        'caballeros': Gender.MEN.value,
        'para ella': Gender.WOMEN.value,
        'damas': Gender.WOMEN.value,
        'blusa': Gender.WOMEN.value,
        'recién nacido': Gender.KIDS.value,
    },
    'hr': {
        'žene': Gender.WOMEN.value,
        'muškarci': Gender.MEN.value
    },
    'hu': {
        'női': Gender.WOMEN.value,
        'férfi': Gender.MEN.value,
        'lány': Gender.GIRLS.value,
        'fiú': Gender.BOYS.value,
        'gyerek': Gender.KIDS.value,
        'uniszex': Gender.ADULTS.value,
        'gyermek': Gender.KIDS.value,
        'lányka': Gender.GIRLS.value,
    },
    'tr': {
        'erkek bebek': Gender.BOYS.value,
        'kız çocuk': Gender.GIRLS.value,
        'kiz çocuk': Gender.GIRLS.value,
        'kız bebek': Gender.GIRLS.value,
        'erkek çocuk': Gender.BOYS.value,
        'genç erkek': Gender.BOYS.value,
        'genç kız': Gender.GIRLS.value,
        'kadın': Gender.WOMEN.value,
        'erkek': Gender.MEN.value,
        'kadin': Gender.WOMEN.value,
        'yenidoğan': Gender.KIDS.value,
        'kız': Gender.GIRLS.value,
        'çocuk': Gender.KIDS.value,
        'bebek': Gender.KIDS.value,
    },
    'sv': {
        'kvinnor': Gender.WOMEN.value,
        'män': Gender.MEN.value,
        'barn': Gender.KIDS.value,
        'kvinna': Gender.WOMEN.value,
        'dam': Gender.WOMEN.value,
        'herr': Gender.MEN.value,
        'flicka': Gender.GIRLS.value,
        'henne': Gender.WOMEN.value,
        'skönhet': Gender.WOMEN.value,
        'flickor': Gender.GIRLS.value,
        'pojkar': Gender.BOYS.value,
        'flick': Gender.GIRLS.value,
        'pojk': Gender.BOYS.value,
        'tjej': Gender.GIRLS.value,
        'kille': Gender.BOYS.value,
    },
    'no': {
        'kvinner': Gender.WOMEN.value,
        'menn': Gender.MEN.value,
        'barn': Gender.KIDS.value,
        'dame': Gender.WOMEN.value,
        'herre': Gender.MEN.value,
        'pike': Gender.GIRLS.value,
        'jente': Gender.GIRLS.value,
        'gutt': Gender.BOYS.value,
        'henne': Gender.WOMEN.value,
        'skjønnhet': Gender.WOMEN.value,
        'jenter': Gender.GIRLS.value,
        'gutte': Gender.BOYS.value,
        'gutter': Gender.BOYS.value,
        'kvinne': Gender.WOMEN.value,
        'mann': Gender.MEN.value,
        'herrer': Gender.MEN.value,
    },
    'da': {
        'børn': Gender.KIDS.value,
        'kvinder': Gender.WOMEN.value,
        'damer': Gender.WOMEN.value,
        'mænd': Gender.MEN.value,
        'kvinde': Gender.WOMEN.value,
        'herre': Gender.MEN.value,
        'dame': Gender.WOMEN.value,
        'hende': Gender.WOMEN.value,
        'herr': Gender.MEN.value,
        'pige': Gender.GIRLS.value,
        'pigen': Gender.GIRLS.value,
        'dreng': Gender.BOYS.value,
        'skønhed': Gender.WOMEN.value,
        'damen': Gender.WOMEN.value,
        'lingerie': Gender.WOMEN.value,
        'haar': Gender.WOMEN.value,
        'femmes': Gender.WOMEN.value,
        'herren': Gender.MEN.value,
        'hommes': Gender.MEN.value,
        'herrer': Gender.MEN.value,
        'hem': Gender.MEN.value,
        'him': Gender.MEN.value,
        'drenge': Gender.BOYS.value,
        'jungen': Gender.BOYS.value,
        'chicos': Gender.BOYS.value,
        'garcons': Gender.BOYS.value,
        'garçons': Gender.BOYS.value,
        'mädchen': Gender.GIRLS.value,
        'chicas': Gender.GIRLS.value,
        'niñas': Gender.GIRLS.value,
        'ninas': Gender.GIRLS.value,
        'fille': Gender.GIRLS.value,
        'bambine': Gender.GIRLS.value,
        'ragazze': Gender.GIRLS.value,
        'ragazzi': Gender.BOYS.value,
        'kinder': Gender.KIDS.value,
        'bebé': Gender.KIDS.value,
        'bebe': Gender.KIDS.value,
        'niños': Gender.KIDS.value,
        'ninos': Gender.KIDS.value,
        'neonati': Gender.KIDS.value,
        'bambini': Gender.KIDS.value,
        'mand': Gender.MEN.value
    },
    'fi': {
        'lapset': Gender.KIDS.value,
        'naiset': Gender.WOMEN.value,
        'miehet': Gender.MEN.value,
        'naisille': Gender.WOMEN.value,
        'tytöt': Gender.GIRLS.value,
        'pojat': Gender.BOYS.value,
        'kauneus': Gender.WOMEN.value,
    },
    'zh': {
        '女士': Gender.WOMEN.value,
        '女子': Gender.WOMEN.value,
        '男士': Gender.MEN.value,
        '男子': Gender.MEN.value,
        '男裝': Gender.MEN.value,
        '女童': Gender.GIRLS.value,
        '婴儿': Gender.KIDS.value,
        '女装': Gender.WOMEN.value,
        '孕妇装': Gender.WOMEN.value,
        '男装': Gender.MEN.value,
        '男孩': Gender.BOYS.value,
        '男幼': Gender.BOYS.value,
        '女孩': Gender.GIRLS.value,
        '女幼': Gender.GIRLS.value,
        '女': Gender.WOMEN.value,
        '女式': Gender.WOMEN.value,
        '男童': Gender.BOYS.value,
        '童装': Gender.KIDS.value,
        '童裝': Gender.KIDS.value,
        '嬰幼兒': Gender.KIDS.value,
        '婴': Gender.KIDS.value,
        '儿童': Gender.KIDS.value,
        '男女童': Gender.KIDS.value,
        '男': Gender.MEN.value,
        '男女': Gender.ADULTS.value,
    },
    'nl': {
        'vrouwen': Gender.WOMEN.value,
        'dames': Gender.WOMEN.value,
        'damer': Gender.WOMEN.value,
        'heren': Gender.MEN.value,
        'mannen': Gender.MEN.value,
        'herenjack': Gender.MEN.value,
        'meiden': Gender.GIRLS.value,
        'meisjes': Gender.GIRLS.value,
        'piger': Gender.GIRLS.value,
        'pige': Gender.GIRLS.value,
        'jongens': Gender.BOYS.value,
        'dame': Gender.WOMEN.value,
        'manne': Gender.MEN.value,
        'jongen': Gender.BOYS.value,
        'kinderen': Gender.KIDS.value,
        'damen': Gender.WOMEN.value,
        'femmes': Gender.WOMEN.value,
        'herren': Gender.MEN.value,
        'hommes': Gender.MEN.value,
        'herrer': Gender.MEN.value,
        'jungen': Gender.BOYS.value,
        'chicos': Gender.BOYS.value,
        'garcons': Gender.BOYS.value,
        'garçons': Gender.BOYS.value,
        'mädchen': Gender.GIRLS.value,
        'chicas': Gender.GIRLS.value,
        'niñas': Gender.GIRLS.value,
        'ninas': Gender.GIRLS.value,
        'fille': Gender.GIRLS.value,
        'bambine': Gender.GIRLS.value,
        'ragazze': Gender.GIRLS.value,
        'ragazzi': Gender.BOYS.value,
        'kinder': Gender.KIDS.value,
        'bebé': Gender.KIDS.value,
        'bebe': Gender.KIDS.value,
        'niños': Gender.KIDS.value,
        'ninos': Gender.KIDS.value,
        'neonati': Gender.KIDS.value,
        'bambini': Gender.KIDS.value,
        'mammae': Gender.WOMEN.value,
        'meisje': Gender.GIRLS.value,
        'meisjen': Gender.GIRLS.value,
    },
    'pt': {
        'ele': Gender.MEN.value,
        'ela': Gender.WOMEN.value,
        'feminina': Gender.WOMEN.value,
        'masculina': Gender.MEN.value,
        'menina': Gender.GIRLS.value,
        'meninas': Gender.GIRLS.value,
        'menino': Gender.BOYS.value,
        'meninos': Gender.BOYS.value,
        'beleza': Gender.WOMEN.value,
        'feminino': Gender.WOMEN.value,
        'mulher': Gender.WOMEN.value,
        'homem': Gender.MEN.value,
        'rapaz': Gender.BOYS.value,
        'criança': Gender.KIDS.value,
        'senhora': Gender.WOMEN.value,
        'masculin': Gender.MEN.value,
        'masculino': Gender.MEN.value,
        'pai': Gender.MEN.value,
        'rapariga': Gender.GIRLS.value,
        'bebé': Gender.KIDS.value,
        'crianças': Gender.KIDS.value,
        'infantil': Gender.KIDS.value,
    },
    'en': {
        'menswear': Gender.MEN.value,
        'dads': Gender.MEN.value,
        'dad': Gender.MEN.value,
        'mom': Gender.WOMEN.value,
        'womans': Gender.WOMEN.value,
        'mans': Gender.MEN.value,
        'lady': Gender.WOMEN.value,
        'shopbyproductladies': Gender.WOMEN.value,
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
        'ballerina': Gender.WOMEN.value,
        'aerie': Gender.WOMEN.value,
        'bra': Gender.WOMEN.value,
        'bridal': Gender.WOMEN.value,
        'necklace': Gender.WOMEN.value,
        'him': Gender.MEN.value,
        'women': Gender.WOMEN.value,
        'kids': Gender.KIDS.value,
        'girl': Gender.GIRLS.value,
        'boy': Gender.BOYS.value,
        'lingerie': Gender.WOMEN.value,
        'infant': Gender.KIDS.value,
        'infants': Gender.KIDS.value,
        'enfant': Gender.KIDS.value,
        'man': Gender.MEN.value,
        'newborn': Gender.KIDS.value,
        'forher': Gender.WOMEN.value,
        'child': Gender.KIDS.value,
        'children': Gender.KIDS.value,
        'childrens': Gender.KIDS.value,
        'childrenswear': Gender.KIDS.value,
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
        'junior': Gender.KIDS.value,
        'kid': Gender.KIDS.value,
        'baby': Gender.KIDS.value,
        'her': Gender.WOMEN.value,
        'teen': Gender.KIDS.value,
        'enfants': Gender.KIDS.value,
        'for her': Gender.WOMEN.value,
        'feminine': Gender.WOMEN.value,
        'gents': Gender.MEN.value,
        'unisex': Gender.ADULTS.value,
    },
    'bg': {
        'жени': Gender.WOMEN.value,
        'мъже': Gender.MEN.value,
        'деца': Gender.KIDS.value,
        'момичета': Gender.GIRLS.value,
        'момчета': Gender.BOYS.value,
    },
    'cn': {
        '女': Gender.WOMEN.value,
        '男': Gender.MEN.value,
        '男童': Gender.BOYS.value,
        '女童': Gender.GIRLS.value,
        '学步': Gender.KIDS.value,
        '儿童': Gender.KIDS.value,
        '婴儿': Gender.KIDS.value,
        '女装': Gender.WOMEN.value,
        '孕产妇': Gender.WOMEN.value,
        '男装': Gender.MEN.value,
        '女婴': Gender.GIRLS.value,
        '男婴': Gender.BOYS.value,
        '童装': Gender.KIDS.value,
        '宝宝': Gender.KIDS.value,
        '子': Gender.KIDS.value,
        '为她': Gender.WOMEN.value
    },
    'ko': {
        '여성': Gender.WOMEN.value,
        '여자': Gender.WOMEN.value,
        '남자': Gender.MEN.value,
        '소녀': Gender.GIRLS.value,
        '걸': Gender.GIRLS.value,
        '여자애들': Gender.GIRLS.value,
        '소년': Gender.BOYS.value,
        '보이': Gender.BOYS.value,
        '소년들': Gender.BOYS.value,
        '남학생': Gender.BOYS.value,
        '남성': Gender.MEN.value,
        '여아': Gender.GIRLS.value,
        '아동': Gender.KIDS.value,
    },
    'sk': {
        'dámy': Gender.WOMEN.value,
        'páni': Gender.MEN.value,
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
        'bayi': Gender.KIDS.value,
        'laki': Gender.BOYS.value,
        'perempuan': Gender.GIRLS.value,
        'hamil': Gender.WOMEN.value
    },
    'uk': {
        'hемовлята': Gender.KIDS.value,
        'дитячі': Gender.KIDS.value,
        'дівчаток': Gender.GIRLS.value,
        'чоловічі': Gender.MEN.value,
        'чоловічий': Gender.MEN.value,
        'чоловiчi': Gender.MEN.value,
        'дівчата': Gender.GIRLS.value,
        'хлопчики': Gender.BOYS.value,
        'хлопчиків': Gender.BOYS.value,
        'хлопчикiв': Gender.BOYS.value,
        'мамам': Gender.WOMEN.value,
        'жіночі': Gender.WOMEN.value,
        'жіноча': Gender.WOMEN.value,
        'жіночий': Gender.WOMEN.value,
    },
    'el': {
        'γυναικεια': Gender.WOMEN.value,
        'αντρικα': Gender.MEN.value
    },
    'he': {
        'נשים': Gender.WOMEN.value,
        'גברים': Gender.MEN.value,
        'בנות': Gender.GIRLS.value,
        'בנים': Gender.BOYS.value,
        'בייבי': Gender.KIDS.value,
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
