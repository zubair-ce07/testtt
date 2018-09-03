from scrapy import Spider

from ..items import PropertyItem


class PropertyParser(Spider):

    name = "atira-parse"

    def parse(self, response):
        atira_property = response.meta.get('property', PropertyItem())
        atira_property['property_url'] = response.url
        atira_property['room_photos'] = self.room_photos(response)
        atira_property['room_availability'] = self.room_availability(response)
        atira_property['room_amenities'] = self.room_amenities(response)
        atira_property['floor_plans'] = self.floor_plans(response)

        for property in self.extract_table_data(response, atira_property):
            yield property

    def room_photos(self, response):
        return response.css('#carousel .slides img::attr(src)').extract()

    def room_availability(self, response):
        if response.css('.button-max'):
            return "Available"
        return "Fully Booked"

    def room_amenities(self, response):
        return response.css('.d-1of4 p::text').extract()

    def floor_plans(self, response):
        return response.css('.button-blue-ghost::attr(data-featherlight)').extract()

    def extract_table_data(self, response, atira_property):
        min_durations = {'1': 119, '2': 308}
        table = response.css('table')
        header_labels = table.css('thead tr th')
        view_types = []

        for label in header_labels:
            view = label.css('* ::text').extract()
            view_types.append(' '.join(view))

        table_rows = table.css('tbody tr')
        name = ""
        for row in table_rows:
            atira_property = atira_property.copy()
            table_columns = row.css('td')
            column_start = 1
            row_start = table_columns[0].css('::text').extract_first()
            if row_start:
                if 'Semester' not in row_start:
                    name = row_start
                else:
                    column_start = 0

            duration = table_columns[column_start].css('::text').extract_first()
            atira_property['min_duration'] = min_durations[duration.split()[0]]

            for room_type in range(column_start + 1, len(table_columns)):
                atira_property = atira_property.copy()
                price = table_columns[room_type].css('::text').extract_first()
                atira_property['room_price'] = price.split()[0].replace('$', '')
                atira_property['room_name'] = f'{self.room_name(response)} {name} ' \
                                              f'{view_types[room_type]}'
                yield atira_property

    def room_name(self, response):
        return response.css('.page-title::text').extract_first()
