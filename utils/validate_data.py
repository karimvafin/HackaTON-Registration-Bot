def check_age(age):
    return not (not age.isdigit() or age[0] == '0' or int(age) < 1)
