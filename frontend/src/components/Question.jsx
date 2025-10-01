import React from "react";

const Question = ({ question, selectedOption, onSelect, onTextChange }) => {
  return (
    <div className="question">
      <h3>{question.text}</h3>

      {question.type === "text" ? (
        <textarea
          value={selectedOption || ""}
          onChange={(e) => onTextChange(e.target.value)}
          placeholder={`Type your answer (max ${question.max_words || 300} words)`}
        />
      ) : (
        <ul>
          {question.options?.map((opt) => (
            <li key={opt.id}>
              <label>
                <input
                  type={question.type === "single" ? "radio" : "checkbox"}
                  name={`question-${question.id}`}
                  value={opt.id}
                  checked={
                    question.type === "single"
                      ? selectedOption === opt.id
                      : selectedOption?.includes(opt.id)
                  }
                  onChange={() => onSelect(opt.id)}
                />
                {opt.text}
              </label>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Question;
