from question_model import Question
from data import question_data

question_bank  = []
for question in question_data:
    question_text = question["text"]
    question_answer = question["answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# todo
# asking the questions
# checking if the answer was correct
# CHECKING IF WE WERE AT THE END OF THE QUIZ
