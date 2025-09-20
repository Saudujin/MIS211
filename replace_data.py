import re

# Read the original HTML content
with open('/home/ubuntu/upload/python-learning-complete_enhanced(1).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the refined slides data
with open('refined_slides_data.js', 'r', encoding='utf-8') as f:
    slides_data_content = f.read()

# Read the generated quiz data
with open('quiz_data.js', 'r', encoding='utf-8') as f:
    quiz_data_content = f.read()

# Replace the slidesData variable in the HTML
# We need to find the script tag containing the slidesData and replace it.
# A simple regex might be too greedy, so we'll be more specific.
slides_pattern = re.compile(r'const slidesData = \[(.*?)\];', re.DOTALL)
html_content = slides_pattern.sub(slides_data_content, html_content)


# Replace the quizData variable in the HTML
quiz_pattern = re.compile(r'const quizData = \[(.*?)\];', re.DOTALL)
# Since there is no quizData in the original file, we will add it before the closing script tag.
if not quiz_pattern.search(html_content):
    html_content = html_content.replace('</script></body>', f'{quiz_data_content}</script></body>')
else:
    html_content = quiz_pattern.sub(quiz_data_content, html_content)



# Write the updated content to a new HTML file
with open('python-learning-final.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully updated the HTML file with new slides and quiz data.')

