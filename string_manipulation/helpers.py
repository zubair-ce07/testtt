
def retain_first_occurence_remove_rest(str):
    """
    Retains the first occurence of each letter in a string and
    removes all other occurences.
    E.g. TechCity' -> 'Techiy'
    """
    input_str = str
    if not input_str:
        raise IndexError('Empty input is not allowed. Please re-enter:')
    if not input_str.isalpha():
        raise ValueError('Numbers or special characters are not allowed. Please re-enter:')

    # Actual program starts her
    modified_str = ""

    for i in str:
        if i not in modified_str:
            modified_str = modified_str + i

    return modified_str


def retain_last_occurence_remove_rest(str):
    """
    Retains the last occurence of each letter in a string and
    removes all other occurences.
    E.g. 'TechTeam' -> 'chTeam'
    """
    input_str = str
    if not input_str:
        raise IndexError('Empty input is not allowed. Please re-enter:')
    if not input_str.isalpha():
        raise ValueError('Numbers or special characters are not allowed. Please re-enter:')

    # Actual program starts here
    removed_letters = []
    modified_str = str

    for i in range(len(str)-1, 0, -1):
        first_index = str.index(str[i])
        if first_index != i and str[i] not in removed_letters:
            removed_letters.append(str[i])
            modified_str = modified_str.replace(str[i], '', 1)

    return modified_str


