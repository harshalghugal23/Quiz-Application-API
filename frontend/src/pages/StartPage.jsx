import React from "react";

const StartPage = ({ onStart }) => {
  return (
    <div className="start-page">
      <h1>Welcome to the Quiz!</h1>
      <button onClick={onStart}>Start Quiz</button>
    </div>
  );
};

export default StartPage;
