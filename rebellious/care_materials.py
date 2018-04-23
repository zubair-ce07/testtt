"""
{
    'relaxed' : will be checked directly,
    'strict': will be checked with the restriction of '%' in the string
}
"""

locale_care_materials = {
    'en': {
        'relaxed': [
            # care
            'fabric', 'rim', 'fur',
            'polyamide', 'polyester', 'lycra', 'silk', 'cotton', 'nylon', 'spandex',
            'wool', 'leather', 'spandex', 'cashmere', 'linen', 'viscose', 'elastane',
            'textile', 'polyurethan', 'synthetic', 'acrylic', 'polyester', 'rubber',
            'vinyl', 'latex', 'lyocell', 'stainless steel', 'wood', 'lambskin',
            'metal', 'plastic', 'suede', 'poly', 'flyknit', 'snakeskin',
            'poylester', 'palyacryl', 'acryl', 'sheepskin', 'calfskin', 'satin', 'lamb leather', 'brass',
            'elastic',
            # wash
            'do not wash', 'wash', 'cannot be washed', 'machine wash', 'hand wash', 'do not iron',
            "don't iron", 'do not bleach', "don't bleach", 'warm iron', 'gentle cycle',
            'wash dark colours separatedly', 'wash dark colors separatedly', 'specialist cleaning',
            'professional cleaning', 'dry clean', 'tumble dry', 'iron on low', 'wipe clean',
            'wash cold', 'cool wash', 'sponge clean', 'dishwasher safe', 'safe for dishwasher',
            'machine-wash', 'iron at', 'no use of dryer', 'hang dry', 'hang to dry', 'reshape whilst damp',
            'line drying', 'iron with medium', 'low temp.', 'high temp.', 'handwash', 'wash method', 'not use bleach',
            'washing', 'wash instructions',
        ],
        'strict': [
            'rayon', 'shearling', 'mesh', 'ponte', 'composition',
        ],
    },
    'de': {
        'relaxed': [
            # German care
            'leder', 'textil', 'kunststoff', 'wolle', 'elasthan', 'elastische', 'synthetik', 'gummi', 'weiche',
            'schutz', 'kaschmir', 'lammfell', 'polyester', 'edelstahlgehäuse', 'polyacryl', 'chiffon', 'viskose',
            'lycra', 'polyurethan', 'schwamm',
            # German wash
            'waschung', 'trockner', 'maschinenw', 'chemisch reinigen', 'trockner nicht verwenden',
            'mittlerer Stufe bügeln', 'zum trocknen aufhängen', 'nicht bleichen', 'bei höchsttemperatur bügeln',
            'bei niedriger temperatur bügeln', 'trockner niedrig', 'handwäsche', 'wasinstructies', 'wassen',
            'bügeln', 'bleichen', 'dampf', 'temperatur', 'waschen', 'schonwaschgang', 'trocknen', 'normalwaschgang',
            'reinigung', 'chemische',
        ],
        'strict': [
            'futter',
        ],
    },
    'sv': {
        'relaxed': [
            # Swedish care
            'akryl', 'fjädrar', 'fjäder', 'bomull', 'cupro', 'elastan', 'jute', 'gummi', 'kashmir',
            'läder', 'linne', 'lurex', 'lykra', 'lyocel', 'metallfiber', 'mocka', 'modal',
            'neopren', 'nyull', 'papperstrå', 'päls', 'polyamid', 'polyetser', 'polyolefin', 'polyster',
            'polypropen', 'polyuretan', 'pvc', 'silikon', 'skinn', 'syntetiskt hår', 'polyuréthane',
            'ull', 'viskos',
            # Swedish wash
            'endast tvätt', 'handtvätt', 'kemtvätt', 'maskintvätt', 'tvättas separat', 'skontvätt',
        ],
        'strict': [
            'acetat', 'ankdun', 'siden', 'rami',
        ],
    },
    'fi': {
        'relaxed': [
            # Finnish (often trimmed to match more cases) care
            'akryylia', 'angoraa', 'elastaan', 'höyheniä', 'kashmirista', 'lykraa', 'mohair',
            'nahkaa', 'nahasta', 'nailon', 'pellava', 'polyolefiinia', 'polyamiidia', 'polyeserist',
            'polypropeenist', 'polyuretaania', 'silkkiä', 'synteettiä', 'tekstiiliä', 'tencellistä',
            'villaa', 'villasta', 'viskoos',
            # Finnish wash
            'käsinpesua', 'konepesu', 'pesuohje', 'pesulämpötila',
        ],
        'strict': [
            'raionia', 'raffiaa', 'paperia', 'mokasta', 'modaal',
        ],
    },
    'da': {
        'relaxed': [
            # Danish care
            'bast', 'bomuld', 'canvas', 'gedhår', 'fjer', 'hør', 'lammelæder', 'lammeuld',
            'læder', 'lino', 'kunstpels', 'merino', 'polyacryl', 'poliéster', 'polyrethan',
            'skind', 'syntetiske', 'tekstil', 'tencel',
            # Danish wash
            'håndvask', 'maskinvask', 'maskinevaskes', 'stryges', 'vaskeanvisning',
        ],
        'strict': [
            'ruskind', 'papirstrå', 'andefjer', 'algodón', 'andedun',
        ],
    },
    'no': {
        'relaxed': [
            # Norwegian (not matched in Danish/Sweden) care
            'fjær', 'keramiske', 'kanvas', 'lær', 'mokka', 'vaskeråd',
            # Norwegian wash
            'strykes',
        ],
        'strict': [],
    },
    'pt': {
        'relaxed': [
            # Portuguese
            'composi\xe7\xe3o', 'tecido', 'algodao', 'algodão',
        ],
        'strict': [],
    },
    'fr': {
        'relaxed': [
            # french care
            'coton', 'cuir', 'synthetique', 'laine', 'sec', 'polyester', 'caoutchouc', 'nylon',
            'élasthanne', 'polyuréthane',
            # French wash
            'laver à', 'lavable en machine', 'lavage à la main', 'traitement au chlore interdi',
            'sèche-linge interdit', 'repasser', 'nettoyage', 'repassage', 'javel', 'nettoyage à sec uniquement',
            'daim', 'nettoyer', 'lavage',
        ],
        'strict': [
            'matière', 'composition',
        ],
    },
    'es': {
        'relaxed': [
            # Spanish care
            'textil', 'goma', 'poliéster', 'algodón', 'lavable', 'fuego', 'polimaida', 'elastano', 'acrílico',
            'viscosa', 'metálico', 'caucho',
            # Chille wash
            'lavado', 'lavar', 'secado', 'lejía', 'cloro', 'cuidar',
        ],
        'strict': [
            # Spanish
            'composición',
        ],
    },
    'cs': {
        'relaxed': [
            'polyamid', 'hedvábí', 'bavlna', 'vlna', 'kůže', 'kašmír', 'prádlo', 'viskóza',
            'elastan', 'textilní', 'polyuretan', 'syntetický', 'akryl', 'umělé hedvábí',
            'guma', 'nerezová ocel', 'dřevo', 'cachemira',
        ],
        'strict': [],
    },
    'pl': {
        'relaxed': [
            # Polish care
            'poliamid', 'poliester', 'jedwab', 'bawełna', 'wełna', 'rzemienny', 'kaszmir', 'bielizna',
            'wiskoza', 'elastan', 'włókienniczy', 'poliuretan', 'syntetyczny', 'akryl', 'sztuczny jedwab',
            'poliester', 'gumowy', 'płyta winylowa', 'lateks', 'stal nierdzewna', 'drewno', 'polamid', 'spandeks',
            'elastane',
            # Polish wash
            'chemicznie', 'prasować', 'bębnowej', 'suszarce', 'suszyć', 'bielić', 'czyszczenie', 'chemiczne', 'prać',
            'pralce',
        ],
        'strict': [],
    },
    'ru': {
        'relaxed': [
            'хлопок', 'полиэстер', 'эластан', 'нейлон', 'полиуретан', 'хлопок',
            'кожа', 'меринос', 'pезина', 'текстиль',
            # Russian wash
            'стирка', 'химчистка', 'химическая', 'bбез пара', 'темп', 'гладить', 'сушилке',
            'сушить', 'отбеливатели',
        ],
        'strict': [
            'состав', 'положении', 'mатериал',
        ],
    },
    'ko': {
        'relaxed': [
            # Korean care
            '폴리아미드', '코튼', '가죽', '코', '엘라스테인', '폴리에스테르', '리넨', '폴리프로필렌',  # Product Materials
            # Korean wash
            '세탁 및 취급 주의사항',  # Washing and Handling Precautions
        ],
        'strict': [
            '제품소재', '소재',
        ],
    },
    'hu': {
        'relaxed': [
            # Hungarian care
            'viszkóz', 'pamut', 'poliészter', 'elasztán', 'poliuretán', 'gumi', 'szintetikus',
            # Hungarian wash
            'Mosás',
        ],
        'strict': [],
    },
    'it': {
        'relaxed': [
            # Italian care
            'seta', 'lana', 'capretto', 'scamosciato', 'cashmere', 'cachemire', 'pelle', 'suola', 'cotone',
            'poliestere', 'gomma', 'elastan',
            # Italian wash
            'lavabile in lavatrice',
            'lavare',  # Wash
            'lavatrice',  # Washing Machine
        ],
        'strict': [
            'composizione',
        ],
    },
    'tr': {
        'relaxed': [
            # Turkish care
            'pamuk', 'deri', 'akrilik', 'poliamit', 'viskoz', 'naylon',
        ],
        'strict': [],
    },
    'nl': {
        'relaxed': [
            # Dutch care
            'materiaal', 'katoen', 'metalen', 'polyester', 'rubberen', 'leer', 'acryl', 'zijde',
            # Dutch wash
            'wasvoorschriften', 'machinewas',
        ],
        'strict': [],
    },
    'zh': {
        'relaxed': [
            # Chinese care
            '锦纶', '棉', '聚氨酯', '聚酯纤维', '面料', '魔术贴', '橡胶', '革', '合成',
            # Chinese wash
            '机洗', '漂白', '手洗', '干洗',
        ],
        'strict': [
            '材质', '材质成分',
        ],
    },
    'ja': {
        'relaxed': [
            # Japanese care
            'コットン', 'ナイロン', '革', 'ポリウレタン', 'ポリエステル', 'ポリプロピレン', '麻', 'ポリ塩化ビニル', '綿', 'ライクラ',
            'ウール', 'シルク', 'ドライのみ', 'スワロフスキー', 'ロジウム', 'レザー', 'ステンレス', '合金', '樹脂', 'ニッケル',
            'プラスチック', '亜鉛', 'アルミニウム', 'レーヨン', 'アクリル', '金メッキ', '真鍮', '絹', 'ウレタン', 'ゴム', '鉄',
            'ポリカーボネート',
            # Japanese wash
            '洗う', '漂白', '洗濯機', 'ドライオンリー', 'ウォッシャブル',
        ],
        'strict': [
            '毛',
        ],
    },
    'ro': {
        'relaxed': [
            # Romanian wash
            'înălbitor', 'bumbac', 'centrifugare', 'chimic', 'curăţa', 'călcaţi',
        ],
        'strict': [],
    },
    'sk': {
        'relaxed': [
            # Slovak wash
            'čistenie', 'chemické', 'žehliť', 'sušiče', 'sušiť', 'chemicky', 'teplota',
        ],
        'strict': [],
    },
    'lt': {
        'relaxed': [
            # Lithuanian
            'poliuretaninis', 'medvilnė', 'kaučiukas', 'cheminiu', 'balinti', 'džiovinti', 'temperatūra',
        ],
        'strict': [],
    },
    'lv': {
        'relaxed': [
            # Latvian
            'kokvilna', 'mazgāšanas', 'žāvētājā',
        ],
        'strict': [],
    },
}
