import re


def validate_cpf(cpf: str) -> bool:
    cpf = ''.join([c for c in cpf if c.isdigit()])

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    summation = sum(int(cpf[i]) * (10 - i) for i in range(9))
    verifier_1 = (summation * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    verifier_2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{verifier_1}{verifier_2}"

def format_cpf(cpf: str) -> str:
    cpf = ''.join([c for c in cpf if c.isdigit()])
    return f"{cpf[0:2]}.{cpf[2:5]}.{cpf[5:8]}-{cpf[8:]}"

def validate_email(email: str) -> bool:
    email_match = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(email_match, email) is not None

def validate_phone(phone: str) -> bool:
    phone = ''.join([c for c in phone if c.isdigit()])
    if len(phone) in (10, 11):
        return True
    return False

def format_phone(phone: str) -> str:
    phone = ''.join([c for c in phone if c.isdigit()])
    if len(phone) == 11:
        return f"({phone[0:2]}) {phone[2:7]}-{phone[7:]}"
    return f"({phone[0:2]}) {phone[2:6]}-{phone[6:]}"