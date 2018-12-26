import dictionary


def main():

    my_dict = dictionary.MyDictionary()
    print(my_dict)

    my_dict['company'] = 'arbisoft'
    my_dict['company'] = 'xyz'
    my_dict['category'] = 'IT'
    my_dict['since'] = 2000
    my_dict['CEO'] = 'Yasser Bashir'
    my_dict['location'] = 'Pakistan'
    my_dict['technology'] = 'Python 3.x'
    my_dict['total_employees'] = 500
    my_dict[10] = 500

    # print(my_dict.all_keys())
    print('\n')
    # print(my_dict.all_values())
    print(my_dict.all_items())
    # print(my_dict)


if __name__ == "__main__":
    main()
