class DescriptionParser:
    #care_keywords = ['iron', 'soft', 'wash', 'bleach', 'Material', 'coat']
    care_keywords = ['Eisen', 'weich', 'waschen', 'bleichen', 'material', 'mantel']

    def is_care(self, description_text):
        if any(k for k in self.care_keywords if k in description_text):
            return True
