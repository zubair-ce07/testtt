import random
from question import Question


class Quizzer:

    def __init__(self):
        self.questions = []
        '''
        questions_sequence contains the question
        numbers to display in sequence
        '''
        self.questions_sequence = []

    def read_questions_with_key(self, questions_file, key_file):
        with open(questions_file) as questions, open(key_file) as key:
            question = questions.readline()
            answer = key.readline()
            while question and answer:
                question = question.split('. ')[1].split('\n')[0]
                answer = answer.split('. ')[1].split('\n')[0]

                self.questions.append(Question(question, answer))

                question = questions.readline()
                answer = key.readline()

    def __generate_quiz(self):
        print("--------------------Questions-------------------")
        for i in range(0, len(self.questions_sequence)):
            output_question = (str(i + 1) +
                               ". " +
                               str(self.questions[self.questions_sequence[i]]) +
                               '\n')

            print(output_question)
            print("Answer - " + str(i + 1) + " :")
            answer = input()
            self.questions[self.questions_sequence[i]].given_answer = answer
            print()

    def generate_result(self):
        print("---------------------Result---------------------")
        for i in range(0, len(self.questions_sequence)):
            if self.questions[self.questions_sequence[i]].is_correct():
                print("Question-" +
                      str(i + 1) +
                      " answered correctly." +
                      '\n')
            else:
                question_no = self.questions_sequence[i]
                print("Sorry, the correct answer of Question-" +
                      str(i + 1) +
                      " is " +
                      self.questions[question_no].correct_answer +
                      '\n')

    def start_quiz(self, no_of_questions):
        if no_of_questions <= len(self.questions):
            for i in range(0, len(self.questions)):
                self.questions_sequence.append(i)

            '''
            shuffling the question sequence,
            so random questions will be displayed
            '''
            self.questions_sequence = random.sample(self.questions_sequence,
                                                    no_of_questions)
            self.__generate_quiz()
        else:
            print("There are only " + str(len(self.questions)) +
                  " questions available.")
