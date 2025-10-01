import json
from app import create_app, db
from app.models import Quiz, Question, Option

# Create Flask app context
app = create_app()
app.app_context().push()

# Load JSON file
with open("questions.json", "r") as f:
    quizzes_data = json.load(f)

for quiz_data in quizzes_data:
    # Check if quiz already exists
    quiz = Quiz.query.filter_by(title=quiz_data["title"]).first()
    if not quiz:
        quiz = Quiz(title=quiz_data["title"])
        db.session.add(quiz)
        db.session.commit()
    
    for q in quiz_data["questions"]:
        # Avoid duplicates
        question = Question.query.filter_by(text=q["text"], quiz_id=quiz.id).first()
        if not question:
            # Use the correct column name in the model
            question = Question(
                text=q["text"],
                type=q.get("type", "text"),  # <-- change from question_type
                quiz_id=quiz.id
            )
            db.session.add(question)
            db.session.commit()

        # Options only for 'single' or 'multiple' type questions
        if q.get("type") in ["single", "multiple"]:
            for opt in q.get("options", []):
                existing_opt = Option.query.filter_by(text=opt["text"], question_id=question.id).first()
                if not existing_opt:
                    option = Option(
                        text=opt["text"],
                        is_correct=opt["is_correct"],
                        question_id=question.id
                    )
                    db.session.add(option)
            db.session.commit()

print("Database seeding completed!")
