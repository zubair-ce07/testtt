from scrapy.exporters import JsonItemExporter


class AthleteItemExportPipeline(JsonItemExporter):

    def __init__(self):
        self.file = open('athletes.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if 'age' in item.keys():
            self.exporter.export_item(item)
        return item


class SportItemExportPipeline(JsonItemExporter):

    def __init__(self):
        self.file = open('sports.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if 'schedules' in item.keys():
            self.exporter.export_item(item)
        return item


class MedalItemExportPipline(JsonItemExporter):

    def __init__(self):
        self.file = open('medals.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if 'total_medals' in item.keys():
            self.exporter.export_item(item)
        return item
