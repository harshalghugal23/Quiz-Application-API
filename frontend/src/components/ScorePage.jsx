import React from "react";

const ScorePage = ({ score, total, onRestart }) => (
  <div>
    <h2>Your Score: {score} / {total}</h2>
    <button onClick={onRestart}>Retry Quiz</button>
  </div>
);

export default ScorePage;
