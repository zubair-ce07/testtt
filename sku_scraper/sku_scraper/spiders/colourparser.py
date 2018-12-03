import re

import unittest
from pygtrie import StringTrie

# from skuscraper.utils.colours import COLOURS, STOP_WORDS

COLOURS = {
    'en': [
        'Air Force blue', 'Alice blue', 'Alizarin crimson', 'Almond', 'Amaranth', 'Inkblue',
        'Amber', 'American rose', 'Amethyst', 'Android Green', 'Anti-flash white',
        'Antique brass', 'Antique fuchsia', 'Antique white', 'Ao', 'Apple green',
        'Apricot', 'Aqua', 'Aquamarine', 'Army green', 'Arylide yellow', 'Ash grey',
        'Asparagus', 'Atomic tangerine', 'Auburn', 'Aureolin', 'AuroMetalSaurus',
        'Azure', 'Azure mist/web', 'Baby blue', 'Baby blue eyes',
        'Baby pink', 'Ball Blue', 'Banana Mania', 'Banana yellow', 'Battleship grey',
        'Bazaar', 'Beau blue', 'Beaver', 'Beige', 'Bisque', 'Bistre', 'Bittersweet',
        'Black', 'Blanched Almond', 'Bleu de France', 'Blizzard Blue', 'Blond', 'Blonde',
        'Blue', 'Blue Bell', 'Blue Gray', 'Blue green', 'Blue purple', 'Blue violet',
        'Blush', 'Bole', 'Bondi blue', 'Bone', 'Boston University Red',
        'Bottle green', 'Boysenberry', 'Brandeis blue', 'Brass', 'Brick red',
        'Bright cerulean', 'Bright green', 'Bright lavender', 'Bright maroon',
        'Bright pink', 'Bright turquoise', 'Bright ube', 'Brilliant lavender',
        'Brilliant rose', 'Brink pink', 'British racing green', 'Bronze', 'Brown',
        'Bubble gum', 'Bubbles', 'Buff', 'Bulgarian rose', 'Burgundy', 'Burlywood',
        'Burnt orange', 'Burnt sienna', 'Burnt umber', 'Byzantine', 'Byzantium',
        'CG Blue', 'CG Red', 'Cadet', 'Cadet blue', 'Cadet grey', 'Cadmium green',
        'Cadmium orange', 'Cadmium red', 'Cadmium yellow', 'Caf\xe9 au lait',
        'Caf\xe9 noir', 'Cal Poly Pomona green', 'Cambridge Blue', 'Camel',
        'Camouflage green', 'Canary', 'Canary yellow', 'Candy apple red',
        'Candy pink', 'Capri', 'Caput mortuum', 'Cardinal', 'Caribbean green',
        'Carmine', 'Carmine pink', 'Carmine red', 'Carnation pink', 'Carnelian',
        'Carolina blue', 'Carrot orange', 'Celadon', 'Celeste', 'Celestial blue',
        'Cerise', 'Cerise pink', 'Cerulean', 'Cerulean blue', 'Chamoisee',
        'Champagne', 'Charcoal', 'Chartreuse', 'Cherry', 'Cherry blossom pink',
        'Chestnut', 'Chocolate', 'Chrome yellow', 'Cinereous', 'Cinnabar',
        'Cinnamon', 'Citrine', 'Classic rose', 'Cobalt', 'Cocoa brown',
        'Coffee', 'Columbia blue', 'Cool black', 'Cool grey', 'Copper',
        'Copper rose', 'Coquelicot', 'Coral', 'Coral pink', 'Coral red', 'Cordovan',
        'Corn', 'Cornell Red', 'Cornflower', 'Cornflower blue', 'Cornsilk',
        'Cosmic latte', 'Cotton candy', 'Cream', 'Crimson', 'Crimson Red',
        'Crimson glory', 'Cyan', 'Daffodil', 'Dandelion', 'Dark blue', 'Dark brown',
        'Dark byzantium', 'Dark candy apple red', 'Dark cerulean', 'Dark chestnut',
        'Dark coral', 'Dark cyan', 'Dark electric blue', 'Dark goldenrod',
        'Dark gray', 'Dark green', 'Dark jungle green', 'Dark khaki', 'Dark lava',
        'Dark lavender', 'Dark magenta', 'Dark midnight blue', 'Dark olive green',
        'Dark orange', 'Dark orchid', 'Dark pastel blue', 'Dark pastel green',
        'Dark pastel purple', 'Dark pastel red', 'Dark pink', 'Dark powder blue',
        'Dark raspberry', 'Dark red', 'Dark salmon', 'Dark scarlet', 'Dark sea green',
        'Dark sienna', 'Dark slate blue', 'Dark slate gray', 'Dark spring green',
        'Dark tan', 'Dark tangerine', 'Dark taupe', 'Dark terra cotta',
        'Dark turquoise', 'Dark violet', 'Dartmouth green', 'Davy grey', 'Debian red',
        'Deep carmine', 'Deep carmine pink', 'Deep carrot orange', 'Deep cerise',
        'Deep champagne', 'Deep chestnut', 'Deep coffee', 'Deep fuchsia',
        'Deep jungle green', 'Deep lilac', 'Deep magenta', 'Deep peach', 'Deep pink',
        'Deep saffron', 'Deep sky blue', 'Desert', 'Desert sand', 'Dim gray',
        'Dodger blue', 'Dogwood rose', 'Dollar bill', 'Drab', 'Duke blue',
        'Earth yellow', 'Ecru', 'Eggplant', 'Eggshell', 'Egyptian blue',
        'Electric blue', 'Electric crimson', 'Electric cyan', 'Electric green',
        'Electric indigo', 'Electric lavender', 'Electric lime', 'Electric purple',
        'Electric ultramarine', 'Electric violet', 'Electric yellow', 'Emerald',
        'Eton blue', 'Fallow', 'Falu red', 'Famous', 'Fandango', 'Fashion fuchsia',
        'Fawn', 'Feldgrau', 'Fern', 'Fern green', 'Ferrari Red', 'Field drab',
        'Fire engine red', 'Firebrick', 'Flame', 'Flamingo pink', 'Flavescent',
        'Flax', 'Floral white', 'Fluorescent orange', 'Fluorescent pink',
        'Fluorescent yellow', 'Folly', 'Forest green', 'French beige', 'French blue',
        'French lilac', 'French rose', 'Fuchsia', 'Fuchsia pink', 'Fulvous',
        'Fuzzy Wuzzy', 'Gainsboro', 'Gamboge', 'Ghost white', 'Ginger', 'Glaucous',
        'Glitter', 'Gold', 'Golden brown', 'Golden poppy', 'Golden yellow',
        'Goldenrod', 'Granny Smith Apple', 'Gray', 'Grey', 'Gray asparagus', 'Green',
        'Green Blue', 'Green yellow', 'Grullo', 'Guppie green', 'Halay\xe0 \xfabe',
        'Han blue', 'Han purple', 'Hansa yellow', 'Harlequin', 'Harvard crimson',
        'Harvest Gold', 'Heart Gold', 'Heather Grey', 'Heliotrope', 'Hollywood cerise', 'Honeydew',
        'Hooker green', 'Hot magenta', 'Hot pink', 'Hunter green', 'Icterine',
        'Inchworm', 'India green', 'Indian red', 'Indian yellow', 'Indigo',
        'International Klein Blue', 'International orange', 'Iris', 'Isabelline',
        'Islamic green', 'Ivory', 'Jade', 'Jasmine', 'Jasper', 'Jazzberry jam',
        'Jonquil', 'June bud', 'Jungle green', 'KU Crimson', 'Kelly green',
        'Khaki', 'La Salle Green', 'Languid lavender', 'Lapis lazuli',
        'Laser Lemon', 'Laurel green', 'Lava', 'Lavender', 'Lavender blue',
        'Lavender blush', 'Lavender gray', 'Lavender indigo', 'Lavender magenta',
        'Lavender mist', 'Lavender pink', 'Lavender purple', 'Lavender rose',
        'Lawn green', 'Lemon', 'Lemon Yellow', 'Lemon chiffon', 'Lemon lime',
        'Light Crimson', 'Light Thulian pink', 'Light apricot', 'Light blue',
        'Light brown', 'Light carmine pink', 'Light coral', 'Light cornflower blue',
        'Light cyan', 'Light fuchsia pink', 'Light goldenrod yellow', 'Light gray',
        'Light green', 'Light khaki', 'Light pastel purple', 'Light pink',
        'Light salmon', 'Light salmon pink', 'Light sea green', 'Light sky blue',
        'Light slate gray', 'Light taupe', 'Light yellow', 'Lilac', 'Lime',
        'Lime green', 'Lincoln green', 'Linen', 'Lion', 'Liver', 'Lust', 'MSU Green',
        'Macaroni and Cheese', 'Magenta', 'Magic mint', 'Magnolia', 'Mahogany',
        'Maize', 'Majorelle Blue', 'Malachite', 'Manatee', 'Mango Tango', 'Mantis',
        'Maroon', 'Mauve', 'Mauve taupe', 'Mauvelous', 'Maya blue', 'Meat brown',
        'Medium Persian blue', 'Medium aquamarine', 'Medium blue',
        'Medium candy apple red', 'Medium carmine', 'Medium champagne',
        'Medium electric blue', 'Medium jungle green', 'Medium lavender magenta',
        'Medium orchid', 'Medium purple', 'Medium red violet', 'Medium sea green',
        'Medium slate blue', 'Medium spring bud', 'Medium spring green', 'Medium taupe',
        'Medium teal blue', 'Medium turquoise', 'Medium violet red', 'Melon',
        'Midnight blue', 'Midnight green', 'Mikado yellow', 'Mint', 'Mint cream',
        'Mint green', 'Misty rose', 'Moccasin', 'Mode beige', 'Moonstone blue',
        'Mordant red 19', 'Moss green', 'Mountain Meadow', 'Mountbatten pink',
        'Mulberry', 'Multi', 'Multicoloured', 'Munsell', 'Mustard', 'Myrtle', 'Nadeshiko pink',
        'Napier green', 'Naples yellow', 'Navajo white', 'Navy', 'Navy blue', 'Neon Carrot',
        'Neon fuchsia', 'Neon green', 'Non-photo blue', 'North Texas Green', 'Ocean Boat Blue',
        'Ochre', 'Office green', 'Old gold', 'Old lace', 'Old lavender', 'Old mauve',
        'Old rose', 'Olive', 'Olive Drab', 'Olive Green', 'Olivine', 'Onyx',
        'Opera mauve', 'Orange', 'Orange Yellow', 'Orange peel', 'Orange red',
        'Orchid', 'Otter brown', 'Outer Space', 'Outrageous Orange', 'Oxford Blue',
        'Pacific Blue', 'Pakistan green', 'Palatinate blue', 'Palatinate purple',
        'Pale aqua', 'Pale blue', 'Pale brown', 'Pale carmine', 'Pale cerulean',
        'Pale chestnut', 'Pale copper', 'Pale cornflower blue', 'Pale gold',
        'Pale goldenrod', 'Pale green', 'Pale lavender', 'Pale magenta', 'Pale pink',
        'Pale plum', 'Pale red violet', 'Pale robin egg blue', 'Pale silver',
        'Pale spring bud', 'Pale taupe', 'Pale violet red', 'Pansy purple',
        'Papaya whip', 'Paris Green', 'Pastel blue', 'Pastel brown', 'Pastel gray',
        'Pastel green', 'Pastel magenta', 'Pastel orange', 'Pastel pink',
        'Pastel purple', 'Pastel red', 'Pastel violet', 'Pastel yellow', 'Patriarch',
        'Payne grey', 'Peach', 'Peach puff', 'Peach yellow', 'Pear', 'Pearl',
        'Pearl Aqua', 'Peridot', 'Periwinkle', 'Persian blue', 'Persian indigo',
        'Persian orange', 'Persian pink', 'Persian plum', 'Persian red',
        'Persian rose', 'Phlox', 'Phthalo blue', 'Phthalo green', 'Piggy pink',
        'Pine green', 'Pink', 'Pink Flamingo', 'Pink Sherbet', 'Pink pearl',
        'Pistachio', 'Platinum', 'Plum', 'Portland Orange', 'Powder blue',
        'Princeton orange', 'Prussian blue', 'Psychedelic purple', 'Puce', 'Pumpkin',
        'Purple', 'Purple Heart', "Purple Mountain's Majesty",
        'Purple mountain majesty', 'Purple pizzazz', 'Purple taupe', 'Rackley',
        'Radical Red', 'Raspberry', 'Raspberry glace', 'Raspberry pink',
        'Raspberry rose', 'Raw Sienna', 'Razzle dazzle rose', 'Razzmatazz', 'Red',
        'Red Orange', 'Red brown', 'Red violet', 'Rich black', 'Rich carmine',
        'Rich electric blue', 'Rich lilac', 'Rich maroon', 'Rifle green',
        "Robin's Egg Blue", 'Rose', 'Rose bonbon', 'Rose ebony', 'Rose gold',
        'Rose madder', 'Rose pink', 'Rose quartz', 'Rose taupe', 'Rose vale',
        'Rosewood', 'Rosso corsa', 'Rosy brown', 'Royal azure', 'Royal blue',
        'Royal fuchsia', 'Royal purple', 'Ruby', 'Ruddy', 'Ruddy brown',
        'Ruddy pink', 'Rufous', 'Russet', 'Rust', 'Sacramento State green',
        'Saddle brown', 'Safety orange', 'Saffron', 'Saint Patrick Blue', 'Salmon',
        'Salmon pink', 'Sand', 'Sand dune', 'Sandstorm', 'Sandy brown',
        'Sandy taupe', 'Sap green', 'Sapphire', 'Satin sheen gold', 'Scarlet',
        'School bus yellow', 'Screamin Green', 'Sea blue', 'Sea green', 'Seal brown',
        'Seashell', 'Selective yellow', 'Sepia', 'Shamrock',
        'Shamrock green', 'Shocking pink', 'Sienna', 'Silver', 'Sinopia',
        'Skobeloff', 'Sky blue', 'Sky magenta', 'Slate blue', 'Slate gray', 'Smalt',
        'Smokey topaz', 'Smoky black', 'Snow', 'Spiro Disco Ball', 'Spring bud',
        'Spring green', 'Steel blue', 'Stil de grain yellow', 'Stizza', 'Stormcloud',
        'Straw', 'Sunglow', 'Sunset', 'Sunset Orange', 'Tan', 'Tangelo',
        'Tangerine', 'Tangerine yellow', 'Taupe', 'Taupe gray', 'Tawny', 'Tea green',
        'Tea rose', 'Teal', 'Teal blue', 'Teal green', 'Terra cotta', 'Thistle',
        'Thulian pink', 'Tickle Me Pink', 'Tiffany Blue', 'Tiger eye', 'Timberwolf',
        'Titanium yellow', 'Tomato', 'Toolbox', 'Topaz', 'Tractor red',
        'Trolley Grey', 'Tropical rain forest', 'True Blue', 'Tufts Blue',
        'Tumbleweed', 'Turkish rose', 'Turquoise', 'Turquoise blue', 'Turquoise green',
        'Tuscan red', 'Twilight lavender', 'Tyrian purple', 'UA blue', 'UA red',
        'UCLA Blue', 'UCLA Gold', 'UFO Green', 'UP Forest green', 'UP Maroon',
        'USC Cardinal', 'USC Gold', 'Ube', 'Ultra pink', 'Ultramarine',
        'Ultramarine blue', 'Umber', 'United Nations blue',
        'University of California Gold', 'Unmellow Yellow', 'Upsdell red', 'Urobilin',
        'Utah Crimson', 'Vanilla', 'Vegas gold', 'Venetian red', 'Verdigris',
        'Vermilion', 'Veronica', 'Violet', 'Violet Blue', 'Violet Red', 'Viridian',
        'Vivid auburn', 'Vivid burgundy', 'Vivid cerise', 'Vivid tangerine',
        'Vivid violet', 'Warm black', 'Waterspout', 'Wenge', 'Wheat', 'White Gold', 'White',
        'White smoke', 'Wild Strawberry', 'Wild Watermelon', 'Wild blue yonder',
        'Wine', 'Wisteria', 'Xanadu', 'Yale Blue', 'Yellow', 'Yellow Orange',
        'Yellow green', 'Zaffre', 'Zinnwaldite brown', 'Multicolor', 'Fuschia',
        'cement grey', 'DARK CEMENT', 'Berry', 'Nude', 'Stone', 'Yellow Gold', 'Faded Denim',
        'Frozen Green', 'Stealth', 'Stone Melee', 'Off White', 'Antra', 'Metallic Silver',
        'Dark Brown Denim', 'Feather Black', 'Seaflow Green', 'Maldive', 'Sunburned Purple',
        'Flame Red', 'Fluro Yellow', 'Silver Grey', 'Shell Pink', 'Bright Red', 'Light Aqua',
        'Fog', 'Punk Pink', 'Seaglass', 'Tahitian Blue', 'Pepper', 'Sulphur', 'Spring', 'Furrow',
        'Sandy', 'Dayglo', 'Natural', 'Maroono', 'Military', 'Cyanine', 'Metal', 'Fluro Lemon',
        'Cardinal Red', 'Gunmetal', 'Sherbet', 'Jungle Camo', 'Midnight', 'Brick', 'Poncho Camo',
        'Paprika', 'Medieval', 'Petrol Blue', 'Bluebird Blue', 'Resin Heather', 'Heather',
        'Asphalt', 'Ebony', 'Titanium', 'Dark Gull Grey', 'Multi Colour', 'Tribal', 'Pewter',
        'Sugar Pine', 'Pool Blue', 'Glacier', 'Fatigue', 'Green Tea', 'Aqua Green', 'Pistaccio',
        'Cloudberry', 'Neon Pink', 'Seaside', 'Moss', 'Mirage', 'Waikiki', 'Hurricane', 'Cayenne',
        'Alert Red', 'Optic White', 'Carbon', 'Solstice', 'Denim Clouds', 'Baltic Blue', 'Nubuck',
        'True Navy', 'Surf', 'Hi-Vis', 'denim', 'whiteyello', 'ink blue', 'Liquorice',
        'Dark Moss', 'Parchment', 'Dahlia', 'Fire Orange', 'Military Green', 'Walnut',
        'Dark Olive', 'Royal Navy', 'Archive Olive', 'Bark', 'Peat', 'Hunting Green', 'Rustic',
        'Sage Green', 'Red Sky', 'Lovat', 'Laurel', 'French Navy', 'Soft Khaki', 'Soft Pink',
        'Oyster', 'Cafe', 'Mocha Brown', 'Mocha', 'Forest', 'Espresso', 'Bourbon', 'Merlot',
        'Verdigris', 'White Sea Air Ditsy', 'Soft Coral', 'Bright White', 'Haze Blue Spot',
        'Hope Stripe French Navy', 'Grey Marl', 'Cream Red Navy Stripe', 'Palm Stripe',
        'Multi Stripe', 'Regatta', 'Duck Egg Peony', 'Cream Star', 'Cream Chinoise Blossom',
        'Navy Gold Ditsy', 'Acorn Border Stripe', 'Burgundy Bircham', 'Raspberry Bircham',
        'Black Winter Floral Border', 'French Navy Festive Birds', 'Meadow', 'Seedling',
        'Red Sky Stripe Stripe', 'Cream Star Stripe', 'Haze Blue', 'Bright Rose', 'Larkspur',
        'Harbour Blue', 'French Navy Fay Floral', 'White & Navy', 'Saffron', 'Ruby Stripe',
        'Ruby Poppy', 'French Navy Stripe', 'Navy Raspberry Stripe', 'Marine Navy', 'Antique Gold',
        'Storm', 'Victoria Blue', 'Redcurrant', 'Heritage Navy', 'Plum Potion Herringbone',
        'Marmalade', 'Chilli Red', 'Bordeaux', 'Blue Steel', 'Kelp', 'Aubergine',
        'Victoria Blue', 'Ice White', 'Signal Orange', 'Blue Lake', 'Reef Red', 'Mist', 'Mortimer',
        'Morris Butterfly', 'Vert Vierzon', 'Sail White',
    ],

    'de': [
        'koningsblauw', 'gelb', 'Rosafarben', 'gold', 'zwart zand', 'gefroren grün', 'beige', 'tiefer see', 'Rosa',
        'Hellblau', 'asche', 'Marineblaue', 'grau', 'dunkel-blau', 'hellbraun', 'crip', 'Natur', 'Silber', 'dark navy',
        'Braun', 'Gruen', 'Marine', 'lila', 'rot', 'Dunkelblau', 'Crème', 'mergel', 'grün nahkampf', 'türkis',
        'Antikgoldfarben', 'hellweiß', 'Blaue', 'weiß', 'Schwarze', 'Dunkelblau/Weiß', 'weiss', 'Grün', 'hell-blau',
        'Grau', 'Dunkelrot', 'Crème/Schwarz', 'zaffer', 'Beige', 'red', 'Blau/Multi', 'Gelb', 'braun', 'Blau', 'blau',
        'koralle', 'grün', 'Lila', 'Weiss', 'gasoline', 'schwarz', 'Blau/Grün', 'navy', 'orange', 'Schwarz',
        'Goldfarben',
        'violett', 'Rot', 'Bunt', 'Roségoldfarben', 'Dunkelblau/Rot', 'Dunkelbraun', 'Dunkel', 'sealife', 'schokolade',
        'baby blue', 'Weiß', 'silber', 'rosa', 'Hi-Vis', 'eichefarben', 'Nussbaum', 'Créme', 'Braun', 'Hellgrau',
        'Marineblau', 'Mittelblau', 'Schwarzgold', 'Weißgold', 'rosé', 'Denimblau', 'Antharzitgrau', 'Crémeweiß',
        'Taubenblau', 'Roségold', 'Gelbgold', 'Olivgrün', 'dunklem Oliv', 'Oliv', 'Dunkelgrün', 'Crèmeweiß',
        'Salmon',
    ],

    # Italian
    'it': [
        'Argento', 'moss', 'argento', 'gunmetal', 'arancione', 'Rosso', 'Ematite', 'Blu', 'cyanine', 'lime', 'righe',
        'blu',
        'ash', 'Verde', 'verde', 'pistaccio', 'Azzuro', 'grafite', 'Giallo', 'marrone', 'Grigio', 'teal', 'royal blue',
        'slate', 'grigio', 'nero', 'Rosé', 'porpora', 'Nero', 'tan', 'coral', 'Bianca', 'Gris', 'viola', 'Arancio',
        'dorado',
        'carbone', 'graph', 'bianco', 'cyan', 'pewter', 'Marrone', 'giallo', 'Azul', 'rosso', 'limone', 'rosa',
        'Hi-Vis', 'Dorato', 'Nera', 'Rossa'
    ],

    # French
    'fr': [
        'sea blue', 'bright pink', 'roses', 'dresden bleu', ' mist', 'darkness', 'turquoise', 'gbsmetal', 'khaki',
        'doré',
        'Rose', 'Pourpre', 'Verte', 'tarmac', 'rose', 'ébène', 'red', 'aloe', 'bleu', 'bleu marine', 'navy',
        'neon vert',
        'argent', 'bleu ciel', 'aquahaze', 'Light gris', 'hotpink', 'pourpre', 'bleu océan', 'Violet', 'lime',
        'multicolore', 'grises', 'foncé', 'cendre bleu', 'pacific', 'caviar', 'de bain bordeaux', 'vert', 'Noir',
        'blanc', 'charcoal', 'Grise', 'flo rose', 'Rouge', 'Dunkelgrün', 'jaune', 'gris froid', 'Bleue', 'Jaune',
        'marron foncé', 'sulphur', 'magenta', 'black', 'port', 'gris clair', 'aqua', 'lilas', 'os', 'ocean',
        'rouge', 'marine sombre', 'noires', 'Beige', 'bleu clair', 'Gris', 'Or', 'brun', 'Noire',
        'gris', 'acid blue', 'marron', 'moss', 'violet', 'marine', 'ardoise', 'Argent', 'Blanc', 'fog blue',
        'ash', 'clair', 'slate', 'royal blue', 'corail', 'graphite', 'Blanche', 'nova', 'carbone', 'orange',
        'fox pink', 'mulberry', 'sarcelle', 'cyan', 'pervenche', 'Marron', 'kaki', 'Corail', 'Hi-Vis', 'blanches',
        'brune', 'bourgogn', 'argenté', 'bleus et verts', 'rouge', 'blanc et bleu', 'gazon', 'anthracite', 'Índigo',
    ],
    # Czech
    'cs': [
        'bílá', 'černá', 'zelená', 'šedá', 'růžová', 'bílé', 'fialová', 'červená', 'ervená', 'béžová', 'žlutá', 'tmavá',
        'zlatá', 'stříbrná', 'modrá', 'světlá', 'hnědá', 'oranžová', 'světle',
    ],

    # Turkish
    'tr': [
        'acı renkli', 'uçuk renkli', 'açık', 'açık renkli', 'açık yeşil', 'alacalı bulucalı, alaca buluca',
        'altın renkli',
        'altuni', 'bej', 'bordo', 'boyalı', 'boz', 'çim rengi', 'çivit rengi', 'eflatun', 'galibarda', 'gökkuşağı',
        'gökkuşağı renkli', 'gri', 'gül rengi', 'gümüş rengi', 'gümüş renkli', 'haki rengi', 'i̇kirenkli, çift renkli',
        'kahverengi', 'koyu', 'koyu gri', 'koyu renkli', 'koyu yeşil', 'lacivert', 'menekşe rengi', 'metalik rengi',
        'morumsu kırmızı renk', 'nefti', 'nilgün', 'beyaz', 'siyah', 'kırmızı', 'mavi', 'turuncu', 'yeşil', 'mor',
        'pembe',
        'kahverengi', 'sarı', 'gri', 'renk', 'açık', 'koyu', 'oranj', 'sari', 'haki', 'yeşi̇l',
    ],
    # Chinese
    'zh': [
        '黑', '蓝', '棕', '灰', '橙', '粉', '紫', '红', '白', '其他',
        '米/白/银', '绿', '驼/棕', '黄/金', '蓝', '灰', '藏青', '浅灰',
        '棕色', '红色', '粉色', '白色', '深棕', '绿色', '浅灰色', '米白色',
        '藏青色', '棕色', '浅棕色', '酒红', '灰色', '红色', '白色', '橙色',
        '黑色', '粉色', '黄色', '蓝色', '绿色' '浅灰', '深棕色', '紫色', '中棕色', '驼色',
        '酒红色', '浅蓝色', '深灰色', '米色', '卡其', '银色', '珍珠母贝', '黑玛瑙色', '藏青色',
        '黑色', '深蓝色', '粉红色',
    ],

    # Netherlands
    'nl': [
        'island bloom', 'sugar pine', 'Zwart', 'gray', 'gletsjer', 'jade', 'brown denim', 'geelrood',
        'neptune', 'grijs', 'zeeblauw', 'stam', 'zilver', 'tortoise shell', 'Zilverkleurig', 'leger',
        'saffron', 'streep', 'limoen', 'zwart / grijs', 'Roze', 'paars', 'blue', 'yellow', 'ibiza',
        'oranje', 'grafiet', 'brown', 'turkoois', 'ZWARTE', 'zwart', 'tinnen', 'Zilverkleuren', 'vida',
        'cerise', 'dark brown', 'zilvergrijs', 'blauwe', 'hi-vis', 'sky', 'donkerblauw', 'light stone',
        'lichtgrijs', 'wit', 'groen', 'costa blue', ' zeemel', 'roze', 'cherry', 'zwarte zanden', 'camo',
        'grijs / zwart', 'stoomer grijs', 'staalblauw', 'rood', 'BLAUW', 'Witte', 'Goud', 'geel',
        'Olijfgroene', 'bruin', 'Greige', 'Antraciet', 'Hemelsblauw', 'Middenblauw', 'rode', 'witte'
    ],
    # Spanish
    'es': [
        'reef', 'roja', 'rojo', 'marl', 'amarillo', 'arancio', 'verde', 'plateado', 'passion pop', 'oro',
        'pimienta', 'blanca', 'blancos', 'Hi-Vis', 'Blanco', 'rouge', 'Gris claro', 'azul marino', 'blanco',
        'Marrón', 'plata', 'marrón', 'gris claro', 'agave', ' grafite', 'orange', 'gris oscuro',
        'laranja', 'café', 'grises', 'negros', 'turquesa', 'melee', 'naranja', 'rosa', 'andorra', 'shell rosa',
        'negro', 'negro de', 'azul', 'sherbet', 'gris', 'grigio', 'caqui', 'marrón claro', 'vermelho melee', 'vino',
        'heather pizarra', 'morado', 'azul claro', 'arena', 'fog', 'lagoon', 'Azul', 'fiano arancio', 'ardesia', 'punk',
        'Marino', 'Rojas', 'Blancas', 'Gris', 'Indigo', 'blanco', 'Azulón', 'Azulon', 'Negra', 'Marineblau',
    ],
    # Polish
    'pl': [
        'brązowa', 'zielona', 'szara', 'jasnobrązowa', 'granatowe', 'granatowe',
        'czarne', 'biel', 'czerwony', 'różowy', 'pomarańczowa', 'pomarańczowa', 'ciemnobrązowy',
        'granatowy', 'brązowy', 'czerwień', ' ciemnobrązowa', 'szara', 'jasnoniebieski', ' różowy', 'pomarańczowy',
        'zielony', ' brązowa', 'biała', 'beżowe', 'czarne', 'ciemnobrązowe', 'jasnobrązowe', 'żółty',
        'camel', 'Srebrny', 'niebieska', 'bieli', 'zieloną', 'jasnoniebieska', 'niebieskie',
        'różowe', 'granatową', 'granatowa Bluz', 'brązowe', 'czerwony', 'niebieski', 'jasnoszary',
        'ciemnoszare', 'szary', 'jasnoszara', 'szare', 'jasnoniebieskie', 'jasnobrązowy', 'czarny',
        'jasnoniebieską', 'błękitne',
    ],
    # Swedish
    'sv': [
        'Khaki', 'Ljusbeige', 'Grå', 'Vinröda', 'Vita', 'Ljusgrå', 'Svart Grå', 'Mörkgrå', 'Svarta', 'Violett',
        'bruna', 'Merino', 'Röd', 'svart/vit', 'Mörkgrön', 'svart', 'Ljusblå', 'Marinblå', 'Vit', 'Café', 'blå',
        'Sunshine', 'KAFFE', 'ljusbrun', 'Mørk indigo', 'Rosa', 'Flerfärgade', 'Brun', 'Ljusrosa', 'grøn',
        'jeansblå', 'Ljusbruna', 'Lila', 'Mörkblå', 'Grön', 'Ljusbrun', 'Blå', 'VIT', 'GRÖNBLÅ CREAM',
    ],
    # Korean
    'ko': [
        '라이트 블루', '다크 브라운', '녹색', '그레이', '블루', '흰색', '빨간색', '핑크', '블랙', '회색', '카멜', '빨간색', '브라운',
    ],
    # Russian
    'ru': [
        'Темно/синяя', 'Темно/синий', 'Синий', 'Оранжевый', 'Красный', 'Коричневый', 'Красный', 'Зеленый', 'Белая',
        'Синяя', 'Темно/синие', 'Темно-коричневые', 'серую', 'песочного', 'Бордовый', 'Голубой', 'Зеленая', 'Желтый',
        'Синие', 'Серые', 'Бежевые', 'Фиолетовый', 'Темно/синее', 'Темно/серый', 'БЕЛЫЙ',
        'Голубая', 'Голубой', 'Коричневое', 'Коричневые', 'Коричневый', 'коричневого', 'Розовый', 'бургунди',
        'светло/коричневую', 'розовую', 'Светло/коричневые', 'Светло/коричневое', 'Светло/коричневый',
        'Rosa', 'Чёрный', 'Разноцветные', 'Черн', 'Разноцветная',
    ],
    'ar': [
        'gris', 'gris claro', 'verde', ' arena',
    ],
    'ja': [
        'ブルー', 'ライトグレー', 'ブラウン', 'ホワイト', 'ブラック', 'ピンク', 'ダークグレ', 'キャメル',
        'ライトブラウン', 'バーガンディ', 'イエロー', 'パープル', 'サ', 'ンドベージュ',
        'ート ブルー', 'サンド', 'オフホワイト', 'ネイビー', 'ィ グレー', 'ピンク', 'ダークブラウン',
        'グレー', 'ライトブルー', 'グレー', 'ライトブルー', 'グリーン', 'ボルドー', 'カーキ', 'サンド', 'オレンジ',
        'レッド', 'シルバー', 'レッド', '濃い紺', '黒', '白', '黄色', '青', '緑', 'ベージュ', '浅青', 'ヌード', '紺'
    ],
    'pt': [
        'vermelho', 'cinza', 'creme', 'preta', 'azul', 'NOIR', 'branca', 'verde', 'roxa e azul',
        'preto', 'amarelo', 'carvão', 'Vela Preto', 'Gray', 'Branco', 'Grapefruit', 'Cinza', 'Azul', 'prata',
        'vermelho', 'ciano', 'Tortoise', 'Amarelo', 'PÊSSEGO', 'violeta', 'alaranjado', 'grapefruit', 'névoa azul',
        'TITÂNIO', 'laranja', 'Marinha', 'ciano'
    ],
    'da': [
        'Mørkrosa', 'blå', 'Teal', 'Camo', 'Plum', 'Aftenblå', 'Persisk Rød', 'Rød', 'Grafit', 'Blå', 'DUSTY BLUE',
        'Turkis', 'Skifer', 'Agave', 'Sølv', 'Hvid', 'Mørke Navy', 'Sort', 'Grå', 'Baltisk Green', 'Hi-Vis',
        'light ink', 'MØRKEBLÅ', 'lilla', 'Brun', 'Guld', 'WHT/PNK', 'Blå/pink', 'Grøn', 'Rosa',
        'Mørkegul', 'Mecca Orange', 'Gul', 'Mørk Rosa', 'Lysegrå', 'Groene', 'bruin', 'GRÅ', 'zwart', 'Mørkgrøn',
        'Blues', 'Vit',
    ],
    'no': [
        'MØRKEBLÅ', 'RØD', 'Svart', 'ROSA', 'SORT', 'Grå', 'Grått', 'Brun', 'Blå', 'Brunt', 'Mørkeblått',
        'grønn', 'Marineblå', 'Lyseoransje', 'Mørkegrå', 'Lyseblå', 'Hvit', 'Burgunder', 'Natur Offwhite',
        'INDIGOBLÅ', 'Armygrønn', 'Rosa', 'Gull', 'GRÅ', 'Oransje', 'mørk grå', 'Lysegrønn', 'Kaki',
        'Mørk oransje', 'Mørkgrå', 'Gul', 'Mørkegrønn', 'Mørkt Oransje', 'Offwhite', 'zwart',
    ],
}

STOP_WORDS = [
    'a',
    'an',
    'and',
    'are',
    'as',
    'at',
    'be',
    'by',
    'for',
    'from',
    'has',
    'he',
    'in',
    'is',
    'it',
    'its',
    'of',
    'on',
    'that',
    'the',
    'to',
    'was',
    'were',
    'will',
    'with'
]



class ColourDetector:
    '''
    .. Note::
        detect_colour() is only publicly available function which returns the detected colours
        and wrapes the underlying implementation.

    Usage::


        >>> from skuscraper.parsers.colourparser import ColourDetector
        >>> self.colour_detector = ColourDetector()

        # For Single Colour ------ It returns a string
        >>> self.colour_detector.detect_colour(colour_str)
        Out[1]: 'Detected Single Colour'

        # For Multiple Colours ------ It returns a string
        >>> self.colour_detector.detect_colour(colour_str, True)
        Out[1]: 'Detected Multiple Colours joined with "/".'
    '''

    attributes_map = [
        ('lang', 'en'),
        ('spider_colours', []),
        ('default_colours', True),
        ('merge_colours', True),
        ('greedy_colour_detection', False),
    ]

    stop_words_re = re.compile(f"(^| ){' |(^| )'.join(STOP_WORDS)} ", re.I)
    separator: str = '/'

    def __init__(self, **kwargs):
        self.trie_tree: StringTrie = StringTrie()

        for attribute, default in self.attributes_map:
            setattr(self, attribute, kwargs.get(attribute, default))

        self.colours: list = self.spider_colours

        if self.merge_colours:
            self.colours += COLOURS.get(self.lang, [])

        if self.default_colours:
            self.colours += COLOURS.get('en', [])

        self.colours: list = [c.lower() for c in sorted(self.colours, key=len, reverse=True)]

        if not self.greedy_colour_detection:
            for colour in self.colours:
                self.trie_tree[re.sub('\W+', self.separator, colour)] = colour

    def detect_colour(self, text: str, multiple: bool) -> str:
        '''Publically available function to be used from outside to interact with API

        :param text: a raw string from which we have to detect colour
        :param multiple: flag to identify if we have to detect single colour or multiple
        :return: detected color/colours.
        '''

        text = self._clean_text(text)
        colours: list = []

        if self.greedy_colour_detection:
            self._greedy_detect_colour(text, colours)
        else:
            self._colour_detection(text, colours)

        if multiple:
            colours = self._unique_colours(colours)
            return '/'.join(colours)
        return colours[0] if colours else ''

    def _unique_colours(self, colours: list) -> list:
        '''Return the unique colours from list of detected colours

        Example:
            colours: ['green blue', 'pink', 'green']
            return: ['green blue', 'pink']

        :param colours: list of detected colours
        :return: a list having unique colours
        '''

        index = colours.index
        colours = sorted(colours, key=len)
        colours = [colour for index, colour in enumerate(colours)
                   if colour not in ' '.join(colours[index + 1:])]
        return sorted(colours, key=index)

    def _clean_text(self, text: str) -> str:
        '''This method accepts a raw string and return a clean string.

        :param text: raw string need to be cleaned
        :return: a well formatted string after removing stop words and
         special characters except '/'
        '''

        text = self.stop_words_re.sub(' ', text or '').lower().strip()
        return re.sub('[\W_]+', self.separator, text)

    def _colour_detection(self, text: str, colours: list) -> None:
        '''This method is supposed to be private and will be called only from
        detect_colour function of this class.

        :param text: text from which we have to detect colour
        :param colours: list of colours detected by this method
        :return: return None
        '''

        colour = self.trie_tree.longest_prefix(text or '')
        if not colour and self.separator not in text:
            return

        if colour:
            colours.append(colour[1])
            text = text[text.find(colour[0]) + len(colour[0]) + 1:]
        else:
            text = text[text.find(self.separator) + 1:]

        return self._colour_detection(text, colours)

    def _greedy_detect_colour(self, text: str, detected_colours: list) -> None:
        '''This method is used to detect colour using greedy approach.

        :param text: text from which we have to detect colour
        :param colours: list of colours detected by this method
        :return: return None
        '''

        for colour in self.colours:
            if colour in text:
                detected_colours.append(colour)


class TestColourParser(unittest.TestCase):
    def setUp(self):
        self.colour_detector = ColourDetector()

    def test_single_colour_english(self):
        text = 'This beige and black Gucci Invite Stamp print A-line skirt has been created with cotton by Italian artisans, features two front button pockets, a button fastening front, gold tone hardware and the spring/summer 2018 catwalk show invite print.'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'beige')

    def test_multiple_colour_english(self):
        text = 'This beige and black Gucci Invite Stamp print A-line skirt has been created with cotton by Italian artisans, features two front button pockets, a button fastening front, gold tone hardware and the spring/summer 2018 catwalk show invite print.'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'beige/black/gold')

    def test_single_colour_with_adjective_english(self):
        text = 'This Rose pink beige and black Gucci Invite Stamp print A-line skirt has been created with cotton by Italian artisans, features two front button pockets, a button fastening front, gold tone hardware and the spring/summer 2018 catwalk show invite print.'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'rose pink')

    def test_multiple_colour_with_adjective_english(self):
        text = 'This Rose pink beige and black Gucci Invite Stamp print A-line skirt has been created with cotton by Italian artisans, features two front button pockets, a button fastening front, gold tone hardware and the spring/summer 2018 catwalk show invite print.'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'rose pink/beige/black/gold')

    def test_invalid_language(self):
        self.colour_detector = ColourDetector(lang='ko')
        text = 'This Rose pink beige and black Gucci Invite Stamp print A-line skirt has been created with cotton by Italian artisans, features two front button pockets, a button fastening front, gold tone hardware and the spring/summer 2018 catwalk show invite print.'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'rose pink')

    def test_text_with_no_colour(self):
        text = 'she is wearing long jacket.'
        self.assertEqual(self.colour_detector.detect_colour(text, False), '')

    def test_empty_text(self):
        text = ''
        self.assertEqual(self.colour_detector.detect_colour(text, False), '')

    def test_none_text(self):
        text = None
        self.assertEqual(self.colour_detector.detect_colour(text, False), '')

    def test_single_colour_german(self):
        self.colour_detector = ColourDetector(lang='de')
        text = 'Sie trägt ein schönes schwarze Hemd'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'schwarze')

    def test_multiple_colour_german(self):
        self.colour_detector = ColourDetector(lang='de')
        text = 'Sie trägt ein schönes Crème/Schwarz und Blau Hemd'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'crème/schwarz/blau')

    def test_single_colour_italian(self):
        self.colour_detector = ColourDetector(lang='it')
        text = 'lei indossa una maglietta arancio giallo'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'arancio')

    def test_multiple_colour_italian(self):
        self.colour_detector = ColourDetector(lang='it')
        text = 'lei indossa una maglietta arancio giallo'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'arancio/giallo')

    def test_single_colour_french(self):
        self.colour_detector = ColourDetector(lang='fr')
        text = 'elle porte une chemise Pourpre Bleue'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'pourpre')

    def test_multiple_colour_french(self):
        self.colour_detector = ColourDetector(lang='fr')
        text = 'elle porte une chemise Pourpre Bleue'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'pourpre/bleue')

    def test_single_colour_czech(self):
        self.colour_detector = ColourDetector(lang='cs')
        text = 'Má na sobě oranžová růžová košili'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'oranžová')

    def test_multiple_colour_czech(self):
        self.colour_detector = ColourDetector(lang='cs')
        text = 'Má na sobě oranžová růžová košili'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'oranžová/růžová')

    def test_single_colour_turkish(self):
        self.colour_detector = ColourDetector(lang='tr')
        text = 'o altın renkli kahverengi bir gömlek giyiyor'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'altın renkli')

    def test_multiple_colour_turkish(self):
        self.colour_detector = ColourDetector(lang='tr')
        text = 'o altın renkli kahverengi bir gömlek giyiyor'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'altın renkli/kahverengi')

    def test_single_colour_chinese(self):
        self.colour_detector = ColourDetector(lang='zh')
        text = '她穿着一件 驼/棕 蓝 色的衬衫'
        self.assertEqual(self.colour_detector.detect_colour(text, False), '驼/棕')

    def test_multiple_colour_chinese(self):
        self.colour_detector = ColourDetector(lang='zh')
        text = '她穿着一件 驼/棕 蓝 色的衬衫'
        self.assertEqual(self.colour_detector.detect_colour(text, True), '驼/棕/蓝')

    def test_single_colour_dutch(self):
        self.colour_detector = ColourDetector(lang='nl')
        text = 'ze draagt ​​een Zilverkleurig ZWARTE shirt'
        self.assertEqual(self.colour_detector.detect_colour(text, False), 'zilverkleurig')

    def test_multiple_colour_dutch(self):
        self.colour_detector = ColourDetector(lang='nl')
        text = 'ze draagt ​​een Zilverkleurig ZWARTE shirt'
        self.assertEqual(self.colour_detector.detect_colour(text, True), 'zilverkleurig/zwarte')

    def test_greedy_colour_detection(self):
        self.colour_detector = ColourDetector(lang='zh', greedy_colour_detection=True)
        text = '她穿着一件 驼/棕 蓝 色的衬衫'
        self.assertEqual(self.colour_detector.detect_colour(text, True), '驼/棕/蓝')


if __name__ == '__main__':
    unittest.main()
