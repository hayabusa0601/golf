import random
from quiz_data import quiz_data

class QuizManager:
    def __init__(self, difficulty: str, num_questions: int = 5):
        self.difficulty = difficulty
        self.num_questions = num_questions  # 追加
        # 指定された難易度のクイズから指定された数だけランダムに選択
        all_questions = quiz_data[self.difficulty]
        num_available = len(all_questions)
        num_to_use = min(num_questions, num_available)
        self.questions = random.sample(all_questions, num_to_use)
        self.current_index = 0
        self.score = 0
        self.answered_questions = set()
        self.last_answer = None
        self.last_selected_option = None

    def get_current_question(self):
        if self.current_index >= len(self.questions):
            return None
        return self.questions[self.current_index]

    def check_answer(self, selected_answer: str) -> bool:
        current_question = self.get_current_question()
        if current_question is None:
            return False
        
        self.last_selected_option = selected_answer
        is_correct = selected_answer == current_question.correct_answer
        if is_correct:
            self.score += 1
        
        self.answered_questions.add(current_question.id)
        self.last_answer = is_correct
        return is_correct

    def next_question(self):
        self.current_index += 1
        self.last_answer = None
        self.last_selected_option = None
    
    def get_progress(self) -> tuple:
        return self.current_index + 1, len(self.questions)
    
    def get_score(self) -> tuple:
        return self.score, len(self.questions)
    
    def is_quiz_completed(self) -> bool:
        return self.current_index >= len(self.questions)

    def get_last_result(self) -> dict:
        return {
            "is_correct": self.last_answer,
            "selected_option": self.last_selected_option,
        }

    def reset_quiz(self):
        self.current_index = 0
        self.score = 0
        self.answered_questions = set()
        self.last_answer = None
        self.last_selected_option = None
        
        # 利用可能な問題から指定された数をランダムに選択
        all_questions = quiz_data[self.difficulty]
        num_available = len(all_questions)
        num_to_use = min(self.num_questions, num_available)  # num_questionsをインスタンス変数として保持
        self.questions = random.sample(all_questions, num_to_use)