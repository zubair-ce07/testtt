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

        txt_files = []
        for file in os.listdir(dir_path):
            if file.endswith(".txt"):
                txt_files.append(dir_path+file)

        return txt_files

    def filter_list_by(self, list_of_strings, filter):
        """
            Funtion returns list of strings that contain filter string in it.
        """

        filtered_list = []

        for file in list_of_strings:
            if file.find(filter) != -1:
                filtered_list.append(file)

        return filtered_list
