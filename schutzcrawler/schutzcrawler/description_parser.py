class DescriptionParser:
    #care_keywords = ['iron', 'soft', 'wash', 'bleach', 'Material', 'coat']
    care_keywords = ['Eisen', 'weich', 'waschen', 'bleichen', 'material', 'mantel', 'iron', 'soft', 'wash', 'bleach', 'Material', 'coat']

    def is_care(self, description_text):
        return any(k for k in self.care_keywords if k in description_text)
