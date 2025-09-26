const API_BASE = "http://localhost:5000"; // Update with deployed URL

export const fetchQuizQuestions = async (quizId) => {
  const res = await fetch(`${API_BASE}/quizzes/${quizId}/questions`);
  return res.json();
};

export const submitQuizAnswers = async (quizId, answers) => {
  const res = await fetch(`${API_BASE}/quizzes/${quizId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  });
  return res.json();
};
