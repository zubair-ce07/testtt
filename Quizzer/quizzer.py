from random import shuffle
import question


class QuizTaker:
    """
    Presents questions to user and evaluates answers
    """
    question_obj = question.QuestionReader()
    key_answers = []
    user_answers = []
    question_asked_order = []

    def read_key(self):
        """
        Reads key.txt and populates key_answers[]
        """
        try:
            with open('key.txt', 'r') as f:
                self.key_answers = f.readlines()
        except FileNotFoundError:
            print("File not found. Error in quizzer.py")
            exit()

        # Remove numbering of answers
        for i in range(len(self.key_answers)):
            first_space = self.key_answers[i].find(' ')
            self.key_answers[i] = self.key_answers[i][first_space+1:]

    def present_questions(self):
        """
        Prints the questions to the user
        """
        print("--------------------Questions-------------------")
        qo_no = 1
        #Shuffle questions
        shuffle(self.question_obj.list_of_questions)

        for i in self.question_obj.list_of_questions:
            # Remove numbering of questions
            first_space = i.find(' ')
            qo_without_number = i[first_space+1:]

            print(str(qo_no) + ". " + qo_without_number + "\n")
            qo_no += 1

    def input_answers(self):
        """
        Prompts the user to input answers
        """
        print("------------------Give Answers------------------")
        for i in range(len(self.question_obj.list_of_questions)):
            print("\nQuestion - " + str(i+1) + " :")
            self.user_answers.append(str(input()))

    def show_results(self):
        """
        Evaluates user's answers and displays results
        """
        print("---------------------Result---------------------")
        for i in range(len(self.question_obj.list_of_questions)):
            if self.get_correct_answer(i) == self.user_answers[i]:
                print("Question-" + str(i+1) + " Correct Answer!\n")
            else:
                print("Sorry, the correct answer of Question-" + str(i+1) + " is: " + self.get_correct_answer(i) + "\n")

    def get_correct_answer(self, index_of_question_list):
        """
        Find the right answer from shuffled questions
        """
        question = self.question_obj.list_of_questions[index_of_question_list]
        qo_no = question[: question.find('.')]

        key_ans = self.key_answers[int(qo_no)-1]
        return key_ans.replace('\n', '', 1)

    def start_quiz(self):
        """
        Calls relative functions to proceed with the quiz
        """
        self.read_key()
        self.present_questions()
        self.input_answers()
        self.show_results()
