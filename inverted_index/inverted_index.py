__author__ = 'abdul'

import constants


class InvertedIndex:
    inverted_index = {}

    def build_inverted_index(self):
        """
        Builds an inverted index using the parsed data.
        Format of inverted index is
        word : [index1, index2, index3, ...]
        where index is the line no of paragraph in data.
        """
        with open(constants.parsed_data_file_name, 'r') as f:
            lines = f.readlines()

            for i in  range(len(lines)):
                words = lines[i].split()

                for word in words:
                    if word.lower() not in constants.stop_words:
                        self.insert_in_list(word.lower(), i)

    def insert_in_list(self, word, position):
        """
        inserts index in list that is the value of
        key 'word' in self.inverted_index
        """
        positions = self.inverted_index.get(word, [])
        positions.append(position)
        self.inverted_index[word] = positions

    def write_inverted_index(self):
        """
        Writes the inverted index on a file
        in the format key value1,value2...
        """
        with open(constants.inverted_index_file_name, 'w') as f:
            for word, positions in self.inverted_index.items():

                f.write("{} ".format(word))
                for index in positions:
                    f.write("{},".format(index))
                f.write("\n")

    def load_inverted_index(self):
        """
        Reads from inverted_index file and populates
        self.inverted_index
        """
        with open(constants.inverted_index_file_name, 'r') as f:
            lines = f.readlines()

            for line in lines:
                splited_line = line.split()
                word = splited_line[0]

                if len(splited_line) < 2:
                    continue
                positions = splited_line[1].split(',')

                all_positions = []
                for index in range(len(positions)-1):
                    all_positions.append(int(positions[index]))

                all_positions = [int(positions[index]) for index in range(len(positions)-1)]

                self.inverted_index[word] = all_positions

    def search_inverted_index(self, search_strings):
        """
        Searches search_strings in data using inverted index.
        Populates search_results with results in format:
        word : [result1, result2, result3...]
        """
        search_results = {}
        with open(constants.parsed_data_file_name, 'r') as f:
            lines = f.readlines()

            for word in search_strings:
                positions = self.inverted_index.get(word.lower(), None)
                if positions is None:
                    search_results[word] = ["No results found."]
                    continue

                current_results = search_results.get(word, [])
                index_error_msg = 'Data file has changed\nPlease reconstruct Inverted Index'
                for position in positions:
                    raise IndexError(index_error_msg) if position > len(lines) \
                        else current_results.append(lines[position])
                search_results[word] = current_results

        self.print_search_results(search_results)


    def print_search_results(self, search_results):
        """
        Prints the search results in an appropriate format
        """
        for word, results in search_results.items():
            print("Results for \"{}\":".format(word))
            for result in results:
                print("- {}".format(result))
            print("\n")

