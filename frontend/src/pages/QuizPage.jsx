import React, { useState, useEffect } from "react";
import Question from "../components/Question";
import { fetchQuizQuestions, submitQuizAnswers } from "../api/quizApi";
import ScorePage from "../components/ScorePage";

const QuizPage = ({ quizId }) => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadQuestions = async () => {
      const data = await fetchQuizQuestions(quizId);
      setQuestions(data);
      setLoading(false);
    };
    loadQuestions();
  }, [quizId]);

  const handleSelect = (qid, optId, type) => {
    setAnswers(prev => {
      const prevAnswer = prev[qid] || (type === "multiple" ? [] : null);

      if (type === "single") {
        return { ...prev, [qid]: optId };
      } else if (type === "multiple") {
        const selected = new Set(prevAnswer);
        if (selected.has(optId)) selected.delete(optId);
        else selected.add(optId);
        return { ...prev, [qid]: Array.from(selected) };
      }
      return prev;
    });
  };

  const handleTextChange = (qid, text) => {
    setAnswers(prev => ({ ...prev, [qid]: text }));
  };

  const handleNext = () => setCurrentIndex(prev => Math.min(prev + 1, questions.length - 1));
  const handlePrev = () => setCurrentIndex(prev => Math.max(prev - 1, 0));

  const handleSubmit = async () => {
    const formattedAnswers = Object.entries(answers)
      .map(([qid, selected]) => {
        const question = questions.find(q => q.id === Number(qid));
        if (!question) return null;

        return {
          question_id: Number(qid),
          selected_option_ids: question.type === "text"
            ? []
            : Array.isArray(selected)
              ? selected.map(Number)
              : [Number(selected)],
          text_answer: question.type === "text" ? selected || "" : undefined,
        };
      })
      .filter(Boolean);

    try {
      const result = await submitQuizAnswers(quizId, formattedAnswers);
      setScoreData(result);
    } catch (err) {
      console.error("Error submitting quiz:", err);
    }
  };

  if (loading) return <div>Loading questions...</div>;
  if (!questions.length) return <div>No questions available for this quiz.</div>;
  if (scoreData) {
    return (
      <ScorePage
        score={scoreData.score}
        total={scoreData.total}
        onRestart={() => {
          setScoreData(null);
          setAnswers({});
          setCurrentIndex(0);
        }}
      />
    );
  }

  const question = questions[currentIndex];

  return (
    <div className="quiz-page">
      <Question
        question={question}
        selectedOption={answers[question.id]}
        onSelect={(optId) => handleSelect(question.id, optId, question.type)}
        onTextChange={(text) => handleTextChange(question.id, text)}
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
