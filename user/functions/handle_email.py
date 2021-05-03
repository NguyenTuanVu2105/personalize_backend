import re


def handle_email(email):
    mail_length = len(email.split("@")[0])
    sub_length = round(mail_length * 0.4)
    sub = ''.join('.' for _ in range(sub_length)) + "@"
    rep = ''.join('*' for _ in range(sub_length)) + "@"
    return re.sub(sub, rep, email)