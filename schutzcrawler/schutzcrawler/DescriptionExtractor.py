class DescriptionExtractor:
    #care_keywords = ['iron', 'soft', 'wash', 'bleach', 'Material', 'coat']
    care_keywords = ['Eisen', 'weich', 'waschen', 'bleichen', 'material', 'mantel']

    def raw_description(self, response):
        raw_description = response.css('#pdp-details-longdesc ::text').extract()
        return [d for d in raw_description if '\n' not in d]

    def description(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if not [k for k in self.care_keywords if k in rd]]

    def care(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if [k for k in self.care_keywords if k in rd]]
