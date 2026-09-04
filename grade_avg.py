def grades(homework):
    sum_of_grade = 0
    for average in homework.values():
        sum_of_grade += average
    calculate = round((sum_of_grade / len(homework)),2)
    return calculate