import weatherdata
import os


class DataParser:
    """Class for parsing and storing data in correct formats,
    this class is not static so multiple instances of data
    can be created and different changes can be made to them
    """
    def __init__(self):
        self.data = weatherdata.WeatherData()

    def get_data(self, file_path):
        """This function reads data from all the txt files present in directory"""
        try:
            # Create a list of all the files to read
            all_files = [x for x in os.listdir(file_path) if x[-4:] == '.txt']
        except FileNotFoundError:
            print("Wrong path, no such directory exists!")
            return None

        for file_name in all_files:
            try:
                file = open(file_path + "/" + file_name, "r")
                # Store the first row of the file for further use with remaining rows.
                header = file.readline().split(",")
                for line in file:
                    self.data.add(line, header)

                file.close()
            except FileNotFoundError:
                print("Wrong file path or name, no such file exists!")
                return None

        return self.data
