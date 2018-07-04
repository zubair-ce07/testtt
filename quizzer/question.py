import constants


class QuestionReader:
    """
    Reads questions from file and stores them
    """
    questions = []
    key_answers = []

    def __init__(self):
        self.read_questions()
        self.read_key_answers()

    def read_questions(self):
        """
        Reads questions from file
        """
        with open(constants.qo_file_name, 'r') as f:
            self.questions = f.readlines()

    def read_key_answers(self):
        """
        Reads key.txt and populates key_answers[]
        """
        with open(constants.key_file_name, 'r') as f:
            self.key_answers = f.readlines()

        # Remove numbering of answers
        for i in range(len(self.key_answers)):
            first_space = self.key_answers[i].find(' ')
            self.key_answers[i] = self.key_answers[i][first_space+1:]

    def get_correct_answer(self, index_of_question_list):
        """
        Find the right answer from shuffled questions
        """
        question = self.questions[index_of_question_list]
        qo_no = question[: question.find('.')]

        key_ans = self.key_answers[int(qo_no)-1]
        return key_ans.replace('\n', '', 1)
