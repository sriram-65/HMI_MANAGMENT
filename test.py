questions = (
    "1. How Ram get huge amount of milk from his breast?",
    "2. Why Ram is called as KLINEFILTER?",
    "3. Why Ram don’t call us for 10 days?",
    "4. Choose the Ram's future wife name?",
    "5. Choose the Ram's most significant title?"
)

options = (
    ('A) by hands', 'B) by machine', 'C) sucking his own breast', 'D) all the above'),
    ('A) his tall finger', 'B) his goands', 'C) his breast', 'D) all the above'),
    ('A) busy in his sucking business', 'B) busy in his milk business', 'C) he was going to honey moon with venkatalakshmi', 'D) all the above'),
    ('A) venkatalakshmi', 'B) his mama ponnu', 'C) santhosh kanna', 'D) Bavadaughter'),
    ('A) milk producing ram', 'B) best blowjober', 'C) calling friends for some work', 'D) all the above')
)

answers = ('B', 'D', 'D', 'C', 'D')
score = 0
guesses = []
question_number = 0

for question in questions:
    print('------------------------')
    print(question)

    for option in options[question_number]:
        print(option)

    guess = input('Enter your answer (A/B/C/D): ').upper()
    guesses.append(guess)

    if guess == answers[question_number]:
        print('✅ YOU ARE ABSOLUTELY CORRECT')
        score += 1
    else:
        print('X YOUR ANSWER IS INCORRECT')
        print(f"✅ CORRECT ANSWER IS: {answers[question_number]}")

    question_number += 1

print('-------------------------')
print('📝 QUIZ RESULTS')
print('-------------------------')
print(f'Your guesses: {guesses}')
print(f'Correct answers: {answers}')

percentage = int((score / len(questions)) * 100)
print(f'🎯 YOUR FINAL SCORE: {percentage}%')
