import React from "react";

const Question = ({ question, selectedOption, onSelect }) => {
  return (
    <div className="question">
      <h3>{question.text}</h3>
      <ul>
        {question.options.map((opt) => (
          <li key={opt.id}>
            <label>
              <input
                type="radio"
                name={`question-${question.id}`}
                value={opt.id}
                checked={selectedOption === opt.id}
                onChange={() => onSelect(opt.id)}
              />
              {opt.text}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Question;
