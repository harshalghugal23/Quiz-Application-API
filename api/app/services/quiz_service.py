from ..models import Quiz, Question, Option
from .. import db

class QuizService:

    @staticmethod
    def create_quiz(title: str) -> Quiz:
        quiz = Quiz(title=title)
        db.session.add(quiz)
        db.session.commit()
        return quiz

    @staticmethod
    def add_question(quiz_id: int, text: str, qtype: str, options: list=None, max_words: int=None) -> Question:
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise ValueError('Quiz not found')

        question = Question(quiz_id=quiz.id, text=text, type=qtype, max_words=max_words)
        db.session.add(question)
        db.session.flush()  # get id

        opts = []
        for opt in (options or []):
            o = Option(question_id=question.id, text=opt['text'], is_correct=bool(opt.get('is_correct')))
            db.session.add(o)
            opts.append(o)

        db.session.commit()
        return question

    @staticmethod
    def get_quiz_questions_for_taking(quiz_id: int):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return None
        out = []
        for q in quiz.questions:
            qdict = {
                'id': q.id,
                'text': q.text,
                'type': q.type,
                'options': [{'id': o.id, 'text': o.text} for o in q.options] if q.type in ('single','multiple') else None,
                'max_words': q.max_words
            }
            out.append(qdict)
        return out
    # Add this inside QuizService class
    @staticmethod
    def get_quiz_question_by_index(quiz_id: int, index: int):
        quiz = Quiz.query.get(quiz_id)
        if not quiz or index < 0 or index >= len(quiz.questions):
            return None

        q = quiz.questions[index]
        return {
            'id': q.id,
            'text': q.text,
            'type': q.type,
            'options': [{'id': o.id, 'text': o.text} for o in q.options] if q.type in ('single','multiple') else [],
            'max_words': q.max_words if q.max_words else (300 if q.type=='text' else None)
        }

    @staticmethod
    def evaluate_submission(quiz_id: int, answers: list):
        # answers: list of {question_id, selected_option_ids, text_answer}
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            raise ValueError('Quiz not found')

        total = 0
        score = 0
        qmap = {q.id: q for q in quiz.questions}

        for ans in answers:
            qid = ans.get('question_id')
            question = qmap.get(qid)
            if not question:
                continue
            total += 1
            if question.type == 'text':
                # For text questions, simple word count check only; scoring policy: full point if non-empty and within limit
                text_answer = (ans.get('text_answer') or '').strip()
                if not text_answer:
                    continue
                word_count = len(text_answer.split())
                if question.max_words and word_count > question.max_words:
                    continue
                score += 1
            elif question.type == 'single':
                selected = ans.get('selected_option_ids') or []
                if len(selected) != 1:
                    continue
                sel = selected[0]
                opt = Option.query.get(sel)
                if opt and opt.question_id == question.id and opt.is_correct:
                    score += 1
            elif question.type == 'multiple':
                selected = set(ans.get('selected_option_ids') or [])
                if not selected:
                    continue
                correct_opts = {o.id for o in question.options if o.is_correct}
                # scoring policy: full point only if selected set equals correct set
                if selected == correct_opts:
                    score += 1

        return {'score': score, 'total': total}

    @staticmethod
    def list_quizzes():
        return [{'id': q.id, 'title': q.title, 'num_questions': len(q.questions)} for q in Quiz.query.all()]
