
import json
import random
import re

slides_data_file = "refined_slides_data.js"

def generate_quiz_questions(slides_data):
    questions = []
    question_id = 1

    # Generate questions from each slide
    for slide in slides_data:
        slide_num = slide["slide"]
        title = slide["title"]
        explanation = slide["explanation"]

        # Generate 3-4 questions per slide to reach 100 questions for 30 slides
        num_questions_per_slide = random.randint(3, 4)

        for _ in range(num_questions_per_slide):
            if len(questions) >= 100:
                break

            question_type = random.choice(["multiple_choice", "true_false", "binary_conversion"])

            if question_type == "multiple_choice" and "•" in slide["literal_translation"]:
                options = [opt.strip() for opt in slide["literal_translation"].split("•") if opt.strip()]
                if len(options) > 1:
                    correct_answer = random.choice(options)
                    question_text = f'أي من التالي يعتبر من {title}؟'
                    choices = random.sample(options, min(len(options), 4))
                    if correct_answer not in choices:
                        choices[0] = correct_answer
                    random.shuffle(choices)
                    questions.append({
                        "id": question_id,
                        "slide": slide_num,
                        "type": "multiple_choice",
                        "question": question_text,
                        "options": choices,
                        "correct": choices.index(correct_answer),
                        "explanation": explanation
                    })
                    question_id += 1

            elif question_type == "true_false":
                is_true = random.choice([True, False])
                if is_true:
                    question_text = explanation
                else:
                    # Create a false statement by slightly modifying the explanation
                    words = explanation.split()
                    if len(words) > 5:
                        # Simple negation for demonstration
                        question_text = explanation.replace(" هو ", " ليس ")
                        if question_text == explanation: # if no change, add a negative word
                            question_text = "غير صحيح أن " + explanation
                    else:
                        question_text = "هذا شرح خاطئ."

                questions.append({
                    "id": question_id,
                    "slide": slide_num,
                    "type": "true_false",
                    "question": f'هل العبارة التالية صحيحة؟ \n\'{question_text}\'',
                    "correct": is_true,
                    "explanation": explanation
                })
                question_id += 1

            elif question_type == "binary_conversion" and "binary" in title.lower():
                decimal_value = random.randint(1, 255)
                binary_value = bin(decimal_value)[2:].zfill(8)
                questions.append({
                    "id": question_id,
                    "slide": slide_num,
                    "type": "binary",
                    "question": "قم بتحويل الرقم العشري التالي إلى ثنائي:",
                    "decimal_value": decimal_value,
                    "binary_positions": [128, 64, 32, 16, 8, 4, 2, 1],
                    "correct_binary": binary_value,
                    "explanation": explanation
                })
                question_id += 1

    return questions

if __name__ == "__main__":
    with open(slides_data_file, "r", encoding="utf-8") as f:
        # Read the file and remove the JavaScript variable assignment
        js_content = f.read()
        json_content = js_content.replace("const refinedSlidesData = ", "").replace(";", "")
        # Add quotes to keys to make it valid JSON
        json_content = re.sub(r'([{,])\s*(\w+)\s*:', r'\1"\2":', json_content)
        slides_data = json.loads(json_content)

    quiz_questions = generate_quiz_questions(slides_data)

    # Ensure we have exactly 100 questions
    while len(quiz_questions) < 100:
        slide = random.choice(slides_data)
        explanation = slide["explanation"]
        is_true = random.choice([True, False])
        if is_true:
            question_text = explanation
        else:
            question_text = explanation.replace(" هو ", " ليس ")
            if question_text == explanation:
                question_text = "غير صحيح أن " + explanation

        quiz_questions.append({
            "id": len(quiz_questions) + 1,
            "slide": slide["slide"],
            "type": "true_false",
            "question": f'هل العبارة التالية صحيحة؟ \n\'{question_text}\'',
            "correct": is_true,
            "explanation": explanation
        })

    with open("quiz_data.js", "w", encoding="utf-8") as f:
        f.write("const quizData = ")
        json.dump(quiz_questions, f, ensure_ascii=False, indent=2)
        f.write(";")

    print("Generated 100 quiz questions in quiz_data.js")

