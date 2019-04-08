import glob
import csv


class Reader:

    all_content = []
    basepath = None
    
    def __init__(self, basepath):
        self.basepath = basepath

    def read_files(self, basepath):
        files = glob.glob(f'{basepath}{"/"}{"*.txt"}')
    
        for filee in files:
            input_file = csv.DictReader(open(str(filee)))
            for row in input_file:
                if row.keys().__contains__("PKT"):
                    row["PKST"] = ''
                    self.all_content.append(row)
                else:
                    row["PKT"] = ''
                    self.all_content.append(row)

        return self.all_content

