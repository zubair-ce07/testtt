import string


# Method to print dictionary content in given format
def print_dict(counting_dict):
    file_to_write = open("task1/output.txt", "w")
    # Creating title of the file i.e. Word   Frequency
    longest_str = max(counting_dict.keys(), key=len)
    title = "Word" + (" " * (len(longest_str)-4)) + " Frequency" + "\n"
    file_to_write.write(title)
    # Divider
    file_to_write.write("-" * len(title) + "\n")
    # Writing frequency of each word
    for key in counting_dict:
        file_to_write.write(f"{key}" + (" " * (len(longest_str)-len(key))) + f" {counting_dict[key]}" + "\n")
    file_to_write.close()


# Method to find frequency of each word in given file
def find_frequencies(filename):
    counting_dict = {}
    f = open(filename, "r")
    # Reading and Iterate through each line
    for row in f.readlines():
        # Removing whitespaces and punctuations
        line = row.strip().translate(str.maketrans('', '', string.punctuation))
        if line:
            # Iterate through line for each word
            for word in line.split():
                # Check word a whitespace or line break
                if ''.join(word.split()):
                    # Ignoring case sensitivity
                    word = word.lower()
                    if counting_dict.get(word) is None:
                        counting_dict[word] = 1
                    else:
                        counting_dict[word] += 1
    return counting_dict


# Main method
def main():
    filename = "task1/words.txt"
    frequencies = find_frequencies(filename)
    print_dict(frequencies)


main()
