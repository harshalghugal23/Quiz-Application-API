import React, { useState, useEffect } from "react";
import Question from "./Question";
import { fetchQuizQuestions, submitQuizAnswers } from "../api/quizApi";

const QuizPage = ({ quizId, onFinish }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    fetchQuizQuestions(quizId).then(setQuestions);
  }, [quizId]);

  const handleSelect = (questionId, optionId) => {
    setAnswers({ ...answers, [questionId]: optionId });
  };

  const handleNext = () => setCurrentIndex((prev) => Math.min(prev + 1, questions.length - 1));
  const handlePrev = () => setCurrentIndex((prev) => Math.max(prev - 1, 0));

  const handleSubmit = async () => {
    const formattedAnswers = Object.entries(answers).map(([qid, oid]) => ({ question_id: qid, option_id: oid }));
    const result = await submitQuizAnswers(quizId, formattedAnswers);
    onFinish(result);
  };

  if (!questions.length) return <div>Loading...</div>;

  return (
    <div className="quiz-page">
      <Question
        question={questions[currentIndex]}
        selectedOption={answers[questions[currentIndex].id]}
        onSelect={(optId) => handleSelect(questions[currentIndex].id, optId)}
      />
      <div className="navigation">
        <button onClick={handlePrev} disabled={currentIndex === 0}>Previous</button>
        {currentIndex < questions.length - 1 ? (
          <button onClick={handleNext}>Next</button>
        ) : (
          <button onClick={handleSubmit}>Submit</button>
        )}
      </div>
    </div>
  );
};

export default QuizPage;
