const API_BASE = "http://localhost:5001/api"; // Update with your deployed API URL

export async function fetchQuizQuestions(quizId) {
  try {
    const response = await fetch(`${API_BASE}/quizzes/${quizId}/questions`);
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    const data = await response.json();
    return data.questions;  // return full array
  } catch (err) {
    console.error("Failed to fetch questions:", err);
    return [];
  }
}

export async function fetchQuizzes() {
  try {
    const response = await fetch("http://localhost:5001/api/quizzes");
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    const data = await response.json();
    return data.quizzes;  // matches backend response
  } catch (err) {
    console.error("Failed to fetch quizzes:", err);
    return [];
  }
}
/**
 * Submit answers for a specific quiz
 * @param {number} quizId 
 * @param {Object} answers - { questionId: selectedOptionId }
 * @returns {Promise<Object>} result { score: ... }
 */
export const submitQuizAnswers = async (quizId, answers) => {
  try {
    const res = await fetch(`${API_BASE}/${quizId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers }),  // <-- must be an object with key 'answers'
    });
    if (!res.ok) {
      throw new Error(`Failed to submit answers: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error("Error submitting quiz answers:", err);
    throw err;
  }
};
