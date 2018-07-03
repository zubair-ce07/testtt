import quizzer

# Import the quizzer module, start quiz
quizzer = quizzer.QuizTaker()
try:
    quizzer.start_quiz()
except FileNotFoundError as f:
    print(format(f))
