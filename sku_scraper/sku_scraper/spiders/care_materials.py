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
            'polyamide', 'polyester', 'lycra', 'silk', 'cotton', 'nylon', 'spandex',
            'wool', 'leather', 'spandex', 'cashmere', 'linen', 'viscose', 'elastane',
            'textile', 'polyurethan', 'synthetic', 'acrylic', 'polyester', 'rubber',
            'vinyl', 'latex', 'lyocell', 'stainless steel', 'wood', 'lambskin',
            'metal', 'plastic', 'suede', 'poly', 'flyknit', 'snakeskin', 'acetate',
            'poylester', 'palyacryl', 'acryl', 'sheepskin', 'calfskin', 'satin', 'lamb leather', 'brass',
            'elastic', 'rim', 'fur', 'tencel', 'neoprene', 'recycled material', 'velvet',
            'faux-crocodile', 'faux-reptile', 'faux-nubuck', 'faux-suede', 'faux-leathe', 'faux-leather',
            'faux-patent', 'faux-croc', 'terylene', 'merino', 'Chlorine', 'elasthan', 'lamb skin',
            'pima cottom', 'material canvas', 'Timber', 'hypo-allergenic', 'clean with a soft',
            'harsh chemicals', 'microfiber', 'pigskin', 'do not expose', 'nubuck', 'fabric composition',
            'Linnen', 'PBT', 'pertex', 'copper', 'zinc',

            # wash
            'do not wash', 'cannot be washed', 'machine wash', 'hand wash', 'do not iron', 'wash at',
            "don't iron", 'do not bleach', "don't bleach", 'warm iron', 'gentle cycle',
            'wash dark colours separatedly', 'wash dark colors separatedly', 'specialist cleaning',
            'professional cleaning', 'dry clean', 'tumble dry', 'iron on low', 'wipe clean',
            'wash cold', 'cool wash', 'sponge clean', 'dishwasher safe', 'safe for dishwasher',
            'machine-wash', 'iron at', 'no use of dryer', 'hang dry', 'hang to dry', 'reshape whilst damp',
            'line drying', 'iron with medium', 'low temp.', 'high temp.', 'handwash', 'wash method', 'not use bleach',
            'washing', 'wash instructions', 'fine wash', 'degree wash', 'Specialist clean', 'iron low', 'cold water',
            'Wash ', 'Machine was cold', 'use softener', 'Low Iron', 'flat to dry', 'Cool Iron', 'Dry away', 'Line dry',
            'Do no bleach', 'bleach or iron', 'wring or twist', 'bleach allowed', 'cold iron', 'Wash Care',
            'Wipe with a damp cloth', 'minimal iron', 'air dry', 'to clean', 'Warm wash', 'washable by hand',
            'cold wash', 'Wipe with', 'Keep away', 'Machinewash', 'washable', 'Clean',
        ],
        'strict': [
            'rayon', 'shearling', 'mesh', 'ponte', 'composition', 'material', 'fabric', 'canvas', 'iron',
        ],
    },
    'de': {
        'relaxed': [
            # German care
            'leder', 'textil', 'kunststoff', 'wolle', 'elasthan', 'elastische', 'synthetik', 'gummi', 'weiche',
            'schutz', 'kaschmir', 'lammfell', 'polyester', 'edelstahlgehäuse', 'polyacryl', 'chiffon', 'viskose',
            'lycra', 'polyurethan', 'schwamm', 'baumwolle', 'elastan', 'polyamid', 'mohair', 'acryl', 'kalbsleder',
            'schurwolle', 'metallicgarn', 'nylon', 'viskose', 'seide', 'acetat', 'metall', 'holz', 'kuh aktion',
            'papier', 'goat action', 'Baumwollmischung', 'baumwollmischung', 'Edelstahl', 'materialzusammensetzung',
            'Kojotenpelz', 'Nicht trockenreinigen', 'Pflegeleicht', 'Nicht nassreinigen', 'Schonende Trocknung',
            'Sauerstoffbleiche', 'Normale Trocknung',
            # German wash
            'waschung', 'trockner', 'maschinenw', 'chemisch reinigen', 'trockner nicht verwenden', 'reinigen',
            'mittlerer Stufe bügeln', 'zum trocknen aufhängen', 'nicht bleichen', 'bei höchsttemperatur bügeln',
            'bei niedriger temperatur bügeln', 'trockner niedrig', 'handwäsche', 'wasinstructies', 'wassen',
            'bügeln', 'bleichen', 'dampf', 'temperatur', 'waschen', 'schonwaschgang', 'trocknen', 'normalwaschgang',
            'reinigung', 'chemische', 'abaca', 'leinen', 'wäsche', 'cold iron', 'fleckenreinigung', 'Poliestere',
            'daunen', 'federn', 'poleyster', 'alpaca', 'poylamid', 'gänsefeder', 'Waschmaschinentauglich'
        ],
        'strict': [
            'futter', 'materialien',
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
    'fa': {
        'relaxed': [
            'پلی استر', 'کتان', 'ابریشم', 'پارچه', 'الیاف مصنوعی', 'چرم', 'پلی اورتان', 'الیاف کشدار',
            'الیاف براق', 'پلی آمید-نایلن', 'الیاف نخی', 'الیاف', 'نخی', 'ویسکوز', 'پلی آمید', 'استات',
            'الیاف کش دار', 'سانتی متر', 'لاستیک', 'نخ', 'اسپاندکس', 'اکریلیک', 'نایلون', 'الاستین',

            # wash
            'قابل شستشو', 'سفید کننده', 'خشک شویی', 'خشک کن', 'اتو کشی', 'شستشو', 'اتوکشی', 'خشکشویی',
        ],
        'strict': [
            'تشکیل شده',
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
            'skind', 'syntetiske', 'tekstil', 'tencel', 'elastan', 'akryl', 'viskose', 'naturgummi',
            'uld', 'fleece bånd', 'pels', 'vaskes ved', 'vaskes', 'vask', 'rens', 'vaskeprogram',
            'bleges', 'tørretumbles', 'alpaka', 'katoen',
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
            'fjær', 'keramiske', 'kanvas', 'lær', 'mokka', 'vaskeråd', 'Bomull', 'Materiale', 'akryl', 'syntetisk',
            'pertex', 'hovedmateriale', 'neopren', 'elastane', 'lammeull', 'ull', 'semsket skinn', 'såle av gummi',
            'gummi', 'merion', 'elestan',

            # Norwegian wash
            'strykes', 'håndvaskes', 'tøymykner', 'vasking', 'vaskes', 'maskinvask', 'vasking', 'tørketrommel',
            'vaskelapp',
        ],
        'strict': [],
    },
    'pt': {
        'relaxed': [
            # Portuguese
            'composi\xe7\xe3o', 'tecido', 'algodao', 'algodão', 'Lavagem à máquina', 'Lavagem a seco', 'avagem a seco',
            'Lavagem à mão', 'lã merino', 'poliamida', 'couro', 'seda', 'poliéster', 'pele de cordeiro',
            'poliester', 'elastano', 'limpeza', 'limpo', 'secar', 'cloro', 'alvejantes', 'limpe',
            'máquina de lavar', 'poliuretano', 'borracha', 'algodåo', 'limpar a seco', 'lavagem na máquina',
            'não branquear', 'ferro', 'secagem em tambor', 'lavar à mão', 'cold iron', 'palha', 'cow action',
            'não lavar', 'não passar', 'camurça', 'terylene', 'lavável à máquina',
        ],
        'strict': [
            'lã', 'acrílico',
        ],
    },
    'fr': {
        'relaxed': [
            # french care
            'coton', 'cuir', 'synthetique', 'laine', 'sec', 'polyester', 'caoutchouc', 'nylon',
            'élasthanne', 'polyuréthane', 'soie', 'cachemire', 'acier inoxydable', 'verre',
            'zircone cubique', 'acier', 'cristal', 'silicone', 'spathes de maïs', 'lin',
            'laine mérinos', 'viscose', 'cupro', 'polyamide', 'autres matériaux', 'wool', 'fourrure', 'toile',

            "triacétate", "fibres métalliques", 'mohair', 'fer à froid', 'fer chaud', 'cuir de veau',
            'cuir injecté de caoutchouc',
            'matériau bois de cèdre', 'matériau argent massif', 'matériau acétate', 'matériau suède', 'matériau alpaga',
            'matériau pur chameau', 'material pura lana',
            "triacétate", "fibres métalliques", 'mohair', 'fer à froid', 'fer chaud', 'synthétique',
            'semelle extérieure en caoutchouc',
            "composition de tissu", 'néoprène', 'Pulire', 'lavable',
            # French wash
            'laver à', 'lavable en machine', 'lavage à la main', 'traitement au chlore interdi',
            'sèche-linge interdit', 'repasser', 'nettoyage', 'repassage', 'javel', 'nettoyage à sec uniquement',
            'daim', 'nettoyer', 'lavage', 'laver délicatement', "laver avec de l'eau", "lavage à l'eau froide",
            'ne pas laver', 'sécher en machine', 'détachage', 'Lavage', 'blanchissage', 'séchage', 'propre',
            'Laver', 'blanchiment', 'SÉCHER', 'FROID', 'LAVER', 'ESSORER', 'lavables en machine', 'Ne pas blanchir',
            'sècher en machine', 'sècher à basse température',
        ],
        'strict': [
            'matière', 'composition', 'matériau',
        ],
    },
    'es': {
        'relaxed': [
            # Spanish care
            'textil', 'goma', 'poliéster', 'algodón', 'lavable', 'fuego', 'polimaida', 'elastano', 'acrílico',

            'viscosa', 'metálico', 'caucho', 'planchar', 'secadora', 'hoja de maíz', 'lino', 'seda',
            'nailon', 'licra', 'lin', 'fibras metálicas', 'piel sintética', 'poliester', 'material cachemir',
            'material pura lana', 'material piel', 'piel de becerro', 'algodón ultrasuave', 'Ante',
            'nailon', 'licra', 'lin', 'fibras metálicas', 'piel sintética', 'poliester', 'empeine de piel',
            'empeine de ante', 'mesh', 'Empeine sintético de ante', 'sintético', 'vinil', 'poliamida',
            'polipropileno', 'lana', 'paño seco', 'funda protectora', 'No planchar', 'No lavar en seco',
            'agua fría', 'blanqueador', 'secar', 'solar directa', 'Guarda tus patines', 'Lavar a mano',
            'No blanquear', 'No usar secadora', 'paño suave', 'no exponga', 'paño limpio', 'seguro para',
            'resistente al agua', 'trapo suave', 'instrucciones de uso', 'no acnegénico', 'poliuretano', 'cachemir',

            # Chille wash
            'lavado', 'lavar', 'secado', 'lejía', 'cloro', 'cuidar', 'Limpieza en seco', 'Limpieza a máquina',
            'Limpieza a mano', 'Limpieza a máquina', 'limpieza', 'cuero', 'lavadora', 'máquina',
            'limpiar con trapo húmedo', 'secadora', 'lejía', 'esponja', 'lavadora', 'séquelo con', 'limpiar con',
            'húmedo o en seco', 'no reseca', 'no moje las', 'usar plancha', 'use plancha', 'usar jabón',
        ],
        'strict': [
            # Spanish
            'composición', 'piel', 'material', 'materiales'
        ],
    },
    'cs': {
        'relaxed': [
            'polyamid', 'hedvábí', 'bavlna', 'vlna', 'kůže', 'kašmír', 'prádlo', 'viskóza',
            'elastan', 'textilní', 'polyuretan', 'syntetický', 'akryl', 'umělé hedvábí',
            'guma', 'nerezová ocel', 'dřevo', 'cachemira', 'žerzej',

            # wash
            'v sušičce', 'pračce',
        ],
        'strict': [
            'materiál', 'materiálu'
        ],
    },
    'pl': {
        'relaxed': [
            # Polish care
            'poliamid', 'poliester', 'jedwab', 'bawełna', 'bawe?na', 'wełna', 'rzemienny', 'kaszmir', 'bielizna',
            'wiskoza', 'elastan', 'włókienniczy', 'poliuretan', 'syntetyczny', 'akryl', 'sztuczny jedwab',
            'poliester', 'gumowy', 'płyta winylowa', 'lateks', 'stal nierdzewna', 'drewno', 'polamid', 'spandeks',
            'elastane', 'elasthan', 'skóra', 'we?na.', 'materiał wewnętrzny', 'bawe?niane', 'camel hairładki',
            'ocieplenie cholewek', 'gumowa podeszwa', 'pig analin', 'podeszwa', 'tencel', 'we?na',
            'skóry', 'tkaniny', 'elastane', 'skóra', 'podeszwa', 'bawelna', 'guma', 'skóra cielęca',
            'materiał mieszanka wełny',
            'materiał nieelastyczne', 'Mieszanka bawełny',
            # Polish wash
            'chemicznie', 'prasować', 'bębnowej', 'suszarce', 'suszyć', 'bielić', 'czyszczenie', 'chemiczne', 'prać',
            'pralce', 'nie wybielać', 'chemicznych', 'len', 'machine', 'cold iron', 'zamsz', 'gumowej', 'tekstylny',
            'syntetyczny', 'polyurethane', 'bawełna', 'spandex',
        ],
        'strict': [],
    },
    'ru': {
        'relaxed': [
            'хлопок', 'полиэстер', 'эластан', 'нейлон', 'полиуретан', 'хлопок',
            'кожа', 'меринос', 'pезина', 'текстиль', 'полиамид', 'вискоза', 'полиамид',
            'водонепроницаемыми', 'ветрозащитными', 'Материал', 'шерсть', 'Кожа', 'шёлк',
            'шерсть', 'хлопок', 'лен', 'шелк', 'Чистый лен', 'кашемир', 'мериносовая шерсть',
            'Итальянская телячья замша', 'смесь', 'Акрил', 'Лайкра', 'Ацетат', 'Ангорская шесть',
            'Купро',
            # Russian wash
            'стирка', 'химчистка', 'химическая', 'bбез пара', 'темп', 'гладить', 'сушилке',
            'сушить', 'отбеливатели', 'сушка', 'Беречь от'
        ],
        'strict': [
            'состав', 'положении', 'mатериал',
        ],
    },
    'ko': {
        'relaxed': [
            # Korean care
            '폴리아미드', '코튼', '가죽', '코', '엘라스테인', '폴리에스테르', '리넨', '폴리프로필렌',  # Product Materials
            '실크', '캐시미어', '폴리우레탄', '직물', '울', '직물 면', '직물 메리노 울', '닦기', '클리닝', '습기에',
            '건조', '표백제', '세탁기', '온수', '세탁', '폴리에스터', '고무', '합성섬유',
            # Korean wash
            '세탁 및 취급 주의사항', '드라이클리닝', '물세탁 가능', '전문 세탁', '손세탁', '젖은 천', '부분 세탁',  # Washing and Handling Precautions
        ],
        'strict': [
            '제품소재', '소재', '울', '면', '유리', '금속', '브라스',
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

            'poliestere', 'gomma', 'elastan', 'ottone', 'vitello', 'acrilico', 'modacrilico', 'acciaio inossidabile',
            'zirconia cubica', 'pietra di vetro', 'acciaio', 'acetato', 'viscosa', 'nylon', 'triacetato',
            'poliammide', 'altre fibre', 'mohair', 'polyamide', 'wool', 'polyurethane', 'polyester',
            'Materiale tomaia', 'Materie tessili sintetiche', 'poliuretano', 'pvc', 'lino', 'tessuto antivento',
            'composizione di tessuto', 'polipropilene', 'elastene', 'l\'humidité',

            # Italian wash
            'lavabile in lavatrice', 'non stirare', 'non candeggiare', 'acqua fredda', 'lavaggio a secco',
            'lavaggio a mano', 'lavaggio',
            'lavare',  # Wash
            'lavatrice',  # Washing Machine
        ],
        'strict': [
            'composizione', 'materiali',
        ],
    },
    'tr': {
        'relaxed': [
            # Turkish care
            'pamuk', 'deri', 'akrilik', 'poliamit', 'viskoz', 'naylon', 'keten', 'viskon', 'elastan',
        ],
        'strict': [
            'kumaş', 'i̇çerik',
        ],
    },
    'nl': {
        'relaxed': [
            # Dutch care
            'materiaal', 'katoen', 'metalen', 'polyester', 'rubberen', 'leer', 'acryl', 'zijde', 'elast',
            'staal', 'stof', 'coton', 'wasvoorschrift', 'wassen',
            # Dutch wash
            'wasvoorschriften', 'machinewas', 'handwas', 'fijnwas', 'merino wol', 'machine wassen',
            'chemisch reinigen', 'wash', 'dry', 'wasmachine', 'wasbaar'
        ],
        'strict': [
            'lamswol',
        ],
    },
    'zh': {
        'relaxed': [
            # Chinese care
            '锦纶', '棉', '聚氨酯', '聚酯纤维', '面料', '魔术贴', '橡胶', '革', '合成', '涤纶', '粘胶纤维', '美利奴羊毛',
            '羔羊皮', '黄铜', '亚麻', '莱赛尔纤维', '铜氨', '聚酰胺', '真丝', '弹性纤维', '醋酸纤维', '金属纤维', '羊绒',
            '水貂毛皮', '聚酰胺纤维', '玻璃纤维', '原材料产地', '羊毛', '粘胶', '尼龙', '莫代尔', '氨纶', '马海毛',
            '纤维素纤维', '卢勒克斯/金属丝', '聚對苯二甲酸', '丁二酯', '莱卡纤维', '羊驼毛', '人造丝', '真皮', '裘皮', '漆皮',
            '金属',

            # Chinese wash
            '机洗', '漂白', '手洗', '干洗', '专业清洗', '可水洗', '烘乾', '浸泡', '洗衣精洗滌', '干净', '避免',
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
            'ポリカーボネート', 'カシミア', 'ラバー', 'ビスコース', 'リヨセル', 'アセテート', 'リネン', 'キュプラ', 'エラスタン',
            'ラムスキン', 'ポリアミド', 'アルパカ', 'スウェード', 'イタリアンカーフスウェード', '手入れ', '清潔', 'スエード',
            '合成繊維', 'カシミヤ',
            # Japanese wash
            '洗う', '漂白', '洗濯機', 'ドライオンリー', 'ウォッシャブル', 'ドライクリーニン', '手洗い', '洗濯可', 'タンブル乾燥',
            'で部分洗い', '拭き取',
        ],
        'strict': [
            '毛',
        ],
    },
    'ro': {
        'relaxed': [
            # Romanian wash
            'înălbitor', 'bumbac', 'centrifugare', 'chimic', 'curăţa', 'călcaţi', 'poliuretan', 'sintetic', 'textil',
            'piele',
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
    'ca': {
        'relaxed': [
        ],
        'strict': [
            'piel'
        ],
    },
    'uk': {
        'relaxed': [
            'нубуку', 'текстилю',
        ],
        'strict': [],
    },
    'id': {
        'relaxed': [
            'dicuci kering', 'pengeringan digantung', 'pemutih', 'disetrika', 'diperas', 'cuci', 'pemutih',
            'dikeringkan di mesin', 'matahari langsung', 'air chlorinated',
        ],
        'strict': [],
    },
    'he': {
        'relaxed': [
            'כותנה', 'פוליאסטר', 'ניקוי יבש', 'הלבנה', 'לכבס', 'אין לייבש', 'כביסה עדינה במכונה', 'זמש', 'אסור'
        ],
        'strict': [],
    },
    'se': {
        'relaxed': [
            'tvätt', 'skölj', 'blekmedel',
        ],
        'strict': []
    },
    'ar': {
        'relaxed': [
            'تُنظّف بشكل جاف فقط', 'تُنظّف بشكل جاف وتُكوى بالكي البخاري', 'تُغسل مع ألوان متماثلة',
            'يُنصح بعدم استخدام مبيّض في الغسيل', 'تُمسح فقط بقطعة قماش رطبة للتنظيف',
        ]
    },
    'bg': {
        'relaxed': [
            'Хастар', 'материал', 'Синтетика', 'Текстил', 'Подметка'
        ],
        'strict': []
    }
}
