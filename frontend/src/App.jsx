import React, { useState } from "react";
import StartPage from "./components/StartPage";
import QuizPage from "./components/QuizPage";
import ScorePage from "./components/ScorePage";

const App = () => {
  const [stage, setStage] = useState("start"); // start, quiz, score
  const [quizResult, setQuizResult] = useState(null);

  const handleStart = () => setStage("quiz");
  const handleFinish = (result) => {
    setQuizResult(result);
    setStage("score");
  };
  const handleRestart = () => {
    setQuizResult(null);
    setStage("start");
  };

  return (
    <div className="app">
      {stage === "start" && <StartPage onStart={handleStart} />}
      {stage === "quiz" && <QuizPage quizId={1} onFinish={handleFinish} />}
      {stage === "score" && <ScorePage score={quizResult.score} total={quizResult.total} onRestart={handleRestart} />}
    </div>
  );
};

export default App;
