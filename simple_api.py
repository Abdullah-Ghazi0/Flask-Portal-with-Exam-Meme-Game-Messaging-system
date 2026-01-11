from models import Questions
import json

def to_dict(self):
    return {
        "id": self.id,
        "question_text": self.q_text,
        "answer": self.answer
        }

def convertor():
    all_questions = Questions.query.all()
    data = [to_dict(question) for question in all_questions]
    return data

