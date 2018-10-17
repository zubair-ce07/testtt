class DataParser:
    @staticmethod
    def readandparsefile(FilePath):
        Papers = []

        data = open(FilePath, 'r')

        records_list = data.read().split('\n\n')
        for i in range(len(records_list)):
            records_list[i] = records_list[i].replace('\n', '')

        data.close()

        records_list = list(filter(None, records_list))

        temp_dict = {}
        for paper in records_list:
            if '#index' in paper:
                temp_dict['index'] = int(paper.split('#index')[-1])
                paper = paper.split('#index')[0]

            if '#c' in paper:
                temp_dict['venue'] = paper.split('#c')[-1]
                if temp_dict['venue'] == ' ':
                    temp_dict['venue'] = ''
                paper = paper.split('#c')[0]
            else:
                temp_dict['venue'] = ''

            if '#t' in paper:
                temp_dict['date'] = int(paper.split('#t')[-1])
                paper = paper.split('#t')[0]
            else:
                temp_dict['date'] = -1

            if '#@' in paper:
                temp_dict['author'] = paper.split('#@')[-1].split(',')
                paper = paper.split('#@')[0]
            else:
                temp_dict['author'] = ['']

            if '#*' in paper:
                temp_dict['name'] = paper.split('#*')[-1]
            else:
                temp_dict['name'] = ['']

            Papers.append(temp_dict)
            temp_dict = {}

        return Papers
