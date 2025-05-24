from prompt import trans_db
import json

s = trans_db()
question_bank = s

'''def get_type():
    if "answer" not in question_dict:
        return "unclassified"

    answer_value = str(question_dict["answer"]).strip().upper()

    # Define possible answers for each type
    multiple_choice_answers = {'A', 'B', 'C', 'D'}
    true_false_answers = {'T', 'F', 'TRUE', 'FALSE'}

    if answer_value in multiple_choice_answers:
        return "multiple_choice"
    elif answer_value in true_false_answers:
        return "true_false"
    else:
        return "open_ended"'''
print(question_bank)
print(type(question_bank))