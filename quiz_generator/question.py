class Question:

    def __init__(self, question, answer):
        self.question = question
        self.correct_answer = answer
        self.given_answer = None

    def is_correct(self):
        return self.correct_answer == self.given_answer

    def __str__(self):
        return str(self.question)
