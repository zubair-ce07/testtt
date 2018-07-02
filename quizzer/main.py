import quizzer

# Import the quizzer module, start quiz
quizzer_obj = quizzer.QuizTaker()
try:
    quizzer_obj.start_quiz()
except FileNotFoundError as f:
    print(f.args[0])