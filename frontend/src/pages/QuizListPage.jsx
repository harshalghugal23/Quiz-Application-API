import React, { useEffect, useState } from "react";
import { fetchQuizzes } from "../api/quizApi";
import { Link } from "react-router-dom";

const QuizListPage = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadQuizzes = async () => {
      try {
        const data = await fetchQuizzes();
        setQuizzes(data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching quizzes:", err);
        setError("Failed to load quizzes.");
        setLoading(false);
      }
    };

    loadQuizzes();
  }, []);

  if (loading) return <div>Loading quizzes...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!quizzes.length) return <div>No quizzes available.</div>;

  return (
    <div className="quiz-list-page">
      <h2>Available Quizzes</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {quizzes.map((q) => (
          <li key={q.id} style={{ margin: "10px 0" }}>
            <Link
              to={`/quiz/${q.id}`}
              style={{
                textDecoration: "none",
                padding: "10px 15px",
                display: "inline-block",
                borderRadius: "8px",
                backgroundColor: "#4caf50",
                color: "#fff",
                transition: "all 0.2s",
              }}
            >
              {q.title} ({q.num_questions} Qs)
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default QuizListPage;
