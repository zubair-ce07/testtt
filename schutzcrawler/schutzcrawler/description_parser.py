class DescriptionParser:
    care_keywords = ['Eisen', 'weich', 'waschen', 'bleichen', 'material', 'mantel', 'iron', 'Do not', 'soft', 'wash',
                     'bleach', 'Material', 'coat', 'Fabric', 'dryclean', 'cotton', 'leather', 'woven', 'water',
                     'temperature', 'textile', 'gentle', 'heat', 'dry']

    def is_care(self, description_text):
        return any(k for k in self.care_keywords if k in description_text)
