import React from "react";

const ScorePage = ({ score, total, onRestart }) => {
  return (
    <div className="score-page">
      <h2>Your Score: {score} / {total}</h2>
      <button onClick={onRestart}>Try Again</button>
    </div>
  );
};

export default ScorePage;
