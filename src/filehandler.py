import os


class FileHandler:
    '''
        This class privdes methods for manipulation on file names in a
        specific directory.
    '''

    def get_txt_files_list(self, dir_path):
        """
            Funtion returns list of all txt files present in given directory.
        """
        return [dir_path+file for file in os.listdir(dir_path)
                if file.endswith(".txt")]

    def filter_list_by(self, list_of_strings, filter):
        """
            Funtion returns list of strings that contain filter string in it.
        """
        return [file for file in list_of_strings if file.find(filter) != -1]
