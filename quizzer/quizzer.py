from random import shuffle
import question


class QuizTaker:
    """
    Presents questions to user and evaluates answers
    """
    question = question.QuestionReader()
    user_answers = []

    def present_questions(self):
        """
        Prints the questions to the user
        """
        print("--------------------Questions-------------------")
        qo_no = 1
        #Shuffle questions
        shuffle(self.question.questions)

        for i in self.question.questions:
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
        for i in range(len(self.question.questions)):
            print("\nQuestion - " + str(i+1) + " :")
            self.user_answers.append(str(input()))

    def show_results(self):
        """
        Evaluates user's answers and displays results
        """
        print("---------------------Result---------------------")
        for i in range(len(self.question.questions)):
            if self.question.get_correct_answer(i) == self.user_answers[i]:
                print("Question-" + str(i+1) + " Correct Answer!\n")
            else:
                print("Sorry, the correct answer of Question-" + str(i+1) + " is: " + self.question.get_correct_answer(i) + "\n")

    def start_quiz(self):
        """
        Calls relative functions to proceed with the quiz
        """
        self.present_questions()
        self.input_answers()
        self.show_results()
