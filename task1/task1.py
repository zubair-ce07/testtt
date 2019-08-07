import string


def write_dict_to_file(counting_dict):
    """ Method to print dictionary content in given format """
    file_to_write = open("output.txt", "w")
    # Creating title of the file i.e. Word   Frequency
    longest_str = max(counting_dict.keys(), key=len)
    title = "Word {} Frequency\n".format((" " * (len(longest_str)-4)))
    file_to_write.write(title)
    # Divider
    file_to_write.write("-" * len(title) + "\n")
    # Writing frequency of each word
    for key in counting_dict:
        file_to_write.write("{} {} {}\n".format(key, (" " * (len(longest_str)-len(key))), counting_dict[key]))
    file_to_write.close()


def find_frequencies(filename):
    """ Method to find frequency of each word in given file """
    counting_dict = {}
    f = open(filename, "r")
    # Reading and Iterate through each line
    for row in f.readlines():
        # Removing whitespaces and punctuations
        line = row.strip().translate(str.maketrans('', '', string.punctuation))
        for word in line.split():
            # Ignoring case sensitivity
            word = word.lower()
            if counting_dict.get(word):
                counting_dict[word] += 1
            else:
                counting_dict[word] = 1

    return counting_dict


def main():
    """ Main method """
    filename = "words.txt"
    frequencies = find_frequencies(filename)
    write_dict_to_file(frequencies)


main()
