# Python program to create
# a pdf file
import logging
import math
import random

from fpdf import FPDF

logging.basicConfig(level=logging.DEBUG,
                    filemode='a',
                    format='{asctime} - {levelname} - [{funcName}:{lineno}] - {message}',
                    style='{')

def save_to_pdf():
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)

    # create a cell
    pdf.cell(200, 10, txt = "GeeksforGeeks",
            ln = 1, align = 'C')

    # add another cell
    pdf.cell(200, 10, txt = "A Computer Science portal for geeks.",
            ln = 2, align = 'C')

    # save the pdf with name .pdf
    pdf.output("GFG.pdf")


"""
Case-1. Addition - Two digit + one digit 
Case-2. Addition - two digit + two digit with no carry forward
Case-3. Addition - three digit + three digit with no carry forward
Case-4. uh!! forgot it :-)
Case-5. Subtraction - Two digit - one digit 
Case-6. Subtraction - two digit + two digit with no carry forward
Case-7. random missing letters with no carry forward - two digit
Case-8. random missing letters with no carry forward - three digit
"""

def addition_no_carry_dataset():
    probs = []

    for itrAns in range(1, 10):
        for itrX in range(1, itrAns):
           if ([str(itrAns - itrX), str(itrX), str(itrAns)]) not in probs:
                probs.append([str(itrAns - itrX), str(itrX), str(itrAns)])
           if ([str(itrX), str(itrAns - itrX), str(itrAns)]) not in probs:
                probs.append([str(itrX), str(itrAns - itrX), str(itrAns)])

    for itr in probs:
	    print(itr)

    print(len(probs))
    return probs

def sub_no_carry_dataset():
    probs = []

    for itrAns in range(1, 10):
        for itrX in range(1, 10-itrAns):
            if ([str(itrAns + itrX), str(itrX), str(itrAns)]) not in probs:
                probs.append([str(itrAns + itrX), str(itrX), str(itrAns)])

    for itr in probs:
        print(itr)

    print(len(probs))
    return probs

def main():
    final_questions = []
    MAX_Q_PER_SECTION = 25

    ques_add_no_cf = addition_no_carry_dataset()
    ques_sub_no_cf = sub_no_carry_dataset()

    final_questions.append([[y for y in ['+'] + x] for x in get_question_CASE1and5(True)[0:MAX_Q_PER_SECTION]])
    ## List list loop is necessary in argument to ensure the original list is not modified. very important learning
    ## We can also do this as list(ques_add_no_cf)
    final_questions.append([[y for y in ['+'] + x] for x in get_question_CASE2and6and7(ques_add_no_cf[:], False)[0:MAX_Q_PER_SECTION]])
    final_questions.append([[y for y in ['+'] + x] for x in get_question_CASE3and8([x for x in ques_add_no_cf], False)[0:MAX_Q_PER_SECTION]])
    final_questions.append([[y for y in ['-'] + x] for x in get_question_CASE1and5(False)[0:MAX_Q_PER_SECTION]])
    final_questions.append([[y for y in ['-'] + x] for x in get_question_CASE2and6and7([x for x in ques_sub_no_cf], False)[0:MAX_Q_PER_SECTION]])
    final_questions.append([[y for y in ['+'] + x] for x in get_question_CASE2and6and7([x for x in ques_add_no_cf], True)[0:MAX_Q_PER_SECTION]])
    final_questions.append([[y for y in ['+'] + x] for x in get_question_CASE3and8([x for x in ques_add_no_cf], True)[0:MAX_Q_PER_SECTION]])
    print(final_questions)
    print(len(final_questions))
    for x in final_questions:
        print(len(x))

    write_questions_to_file(final_questions)

def format_numbers(data):
    if len(data) == 1:
        data = '&nbsp;' + '&nbsp;' + data
    if len(data) == 2:
        data = '&nbsp;' + data

    data = data.replace('x', '&#9633;')

    return data

def write_questions_to_file(questions):
    ques_in_html = []
    number_of_question = 0

    for itr in questions:
        isDivOpen = False
        for itrQues in itr:
            number_of_question += 1

            if not isDivOpen:
                ques_in_html.append('<div class="question_box">')


            ques_in_html.append('<div class="question_single">')
            ques_in_html.append('<span class ="equation stacked" > ')
            ques_in_html.append('<span class ="number" > ' + format_numbers(itrQues[1]) + '</span> ')
            ques_in_html.append('<span class ="operator" > ' + itrQues[0] + ' </span> ')
            ques_in_html.append('<span class ="number" > ' + format_numbers(itrQues[2]) + '</span> ')
            ques_in_html.append('<span class ="equals" >= </span> ')
            ques_in_html.append('<span class ="number" > ' + format_numbers(itrQues[3]) + '</span> ')
            ques_in_html.append('<span class ="equals" >= </span> ')
            ques_in_html.append('</span> ')
            ques_in_html.append('</div>')

            if number_of_question%16 == 0:
                ques_in_html.append('<div class="question_single">')
                ques_in_html.append('<span>GOOD JOB!<br> You earned a coupon <br> Here is your &#9734; </span>')
                ques_in_html.append('</div>')

            if isDivOpen:
                ques_in_html.append('</div>')

            if isDivOpen:
                isDivOpen = False
            else:
                isDivOpen = True

        if isDivOpen:
            ques_in_html.append('</div>')

    print(ques_in_html)

    file_content = ''

    try:
        with open(r'index.html.base') as file:
            for line in file.read().splitlines():
                if line == '__YOUR_QUESTIONS_HERE__':
                    for itrQues in ques_in_html:
                        file_content = file_content + itrQues + '\n'
                else:
                    file_content = file_content + line

        with open('index.html', 'w') as file:
            file.write(file_content)

    except Exception as error:
        print("ERROR")

def get_question_CASE1and5(isAddition=True):
    questions = []

    ## Actually you need not know the answer as we are not printing,
    ## so we need not know if its add or substrate
    while (len(questions) <= 50):
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 9)
        ans = 0

        if (isAddition):
            ans = num1 + num2
        else:
            ans = num1 - num2

        if (ans >= 100 or ans <= 0):
            continue

        if(ans > 9):
            ans = 'xx'
        else:
            ans = 'x'
        questions.append([str(num1), str(num2), ans])

    return questions

def get_question_CASE2and6and7(dataset, maskRandomDigit = False):
    questions = []
    random.shuffle(dataset)

    while(len(dataset) >= 2):
        units = list(dataset.pop(0))
        tens = list(dataset.pop(0))

        if(maskRandomDigit):
            units[random.randint(0,2)] = 'x'
            tens[random.randint(0,2)] = 'x'
        else:
            units[2] = 'x'
            tens[2] = 'x'


        questions.append([ tens[0] + units[0], tens[1] + units[1], tens[2] + units[2]])

    return questions

def get_question_CASE3and8(dataset, maskRandomDigit = False):
    questions = []

    ## Because we need bigger data set here, so just doubling it and shuffling
    temp_dataset = list(dataset) + list(dataset)
    ## just like that another shuffle, so that we get questions like 22 + 11 (repeated from datasets)
    random.shuffle(temp_dataset)

    while(len(temp_dataset) >= 3):
        hundreds = list(temp_dataset.pop(0))
        units = list(temp_dataset.pop(0))
        tens = list(temp_dataset.pop(0))

        if(maskRandomDigit):
            hundreds[random.randint(0,2)] = 'x'
            tens[random.randint(0,2)] = 'x'
            units[random.randint(0,2)] = 'x'
        else:
            hundreds[2] = 'x'
            tens[2] = 'x'
            units[2] = 'x'

        questions.append([ hundreds[0] + tens[0] + units[0], hundreds[1] + tens[1] + units[1], hundreds[2] + tens[2] + units[2]])

    return questions

if __name__ == "__main__": main()
