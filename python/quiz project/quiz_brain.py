class Quizbrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.q_list = question_list
    
    def still_has_questions(self):
        return self.question_number < len(self.q_list)
           
    def next_question(self):
        current_question = self.q_list[self.question_number]
        self.question_number += 1
        user_answer = input (f"Q.{self.question_number}: {current_question.text} (True/False)")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lowwer():
            self.score += 1
            self.question_number += 1
            print("you got it right ")
        else:
            print("that's wrong")
        print(f"the correct answer was: {correct_answer}")
        print(f"Your current score is: {self.score}/{self.question_number}")
        print("\n")
        if self.still_has_questions():
            self.next_question()
        else:
            print("You've completed the quiz!")
            print(f"Your final score was: {self.score}/{self.question_number}")