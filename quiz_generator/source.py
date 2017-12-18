from quizzer import Quizzer


if __name__ == "__main__":
    q1 = Quizzer()
    q1.read_questions_with_key("./questions.txt", "./key.txt")

    '''
    start_quiz takes no. of questions as argument
    '''
    q1.start_quiz(3)

    q1.generate_result()
