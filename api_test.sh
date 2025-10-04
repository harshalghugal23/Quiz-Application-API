#!/bin/bash

BASE_URL="http://127.0.0.1:5001/api"
QUIZ_ID=1
USERNAME="testuser"
PASSWORD="testpass"

divider() { echo "----------------------------------------"; }
section() { divider; echo "▶️  $1"; divider; }

# Helper to call API and check HTTP status
run_test() {
  local METHOD=$1
  local URL=$2
  local DATA=$3
  local EXPECTED=${4:-200}

  if [ -z "$DATA" ]; then
    STATUS=$(curl -s -o response.json -w "%{http_code}" -X $METHOD "$URL")
  else
    STATUS=$(curl -s -o response.json -w "%{http_code}" -X $METHOD "$URL" \
      -H "Content-Type: application/json" \
      -d "$DATA")
  fi

  if [ "$STATUS" -eq "$EXPECTED" ]; then
    echo "✅ PASS | HTTP $STATUS"
  else
    echo "❌ FAIL | HTTP $STATUS"
  fi

  cat response.json | jq '.' 2>/dev/null || cat response.json
  echo -e "\n"
}

# 1️⃣ Register User
section "Registering User"
run_test POST "$BASE_URL/register" "{
  \"username\": \"$USERNAME\",
  \"password\": \"$PASSWORD\"
}" 201

# 2️⃣ Login
section "Logging In"
run_test POST "$BASE_URL/login" "{
  \"username\": \"$USERNAME\",
  \"password\": \"$PASSWORD\"
}" 200

# 3️⃣ Create Quiz
section "Creating Quiz"
run_test POST "$BASE_URL/quizzes" '{
  "title": "Sample Quiz"
}' 201

# 4️⃣ Add Multiple Choice Question
section "Adding MCQ Question"
run_test POST "$BASE_URL/quizzes/$QUIZ_ID/questions" '{
  "text": "What is the capital of France?",
  "type": "single",
  "options": [
    { "text": "Berlin", "is_correct": false },
    { "text": "Paris", "is_correct": true },
    { "text": "Rome", "is_correct": false }
  ]
}' 201

# 5️⃣ Add Text Question
section "Adding Text Question"
run_test POST "$BASE_URL/quizzes/$QUIZ_ID/questions" '{
  "text": "Write a short note on MicroK8s",
  "type": "text",
  "max_words": 50
}' 201

# 6️⃣ Fetch All Questions
section "Fetching All Questions for Quiz ID = $QUIZ_ID"
run_test GET "$BASE_URL/quizzes/$QUIZ_ID/questions" 200

# 7️⃣ Fetch Question by Index
section "Fetching Question by Index (index=0)"
run_test GET "$BASE_URL/quizzes/$QUIZ_ID/questions?index=0" 200

# 8️⃣ Submit Quiz Answers
section "Submitting Answers"
run_test POST "$BASE_URL/quizzes/$QUIZ_ID/submit" '{
  "answers": [
    { "question_id": 1, "selected_option_ids": [2] },
    { "question_id": 2, "text_answer": "MicroK8s is a lightweight Kubernetes distribution by Canonical." }
  ]
}' 200

divider
echo "🎯 Quiz API Functional Test Runner Completed"
divider
