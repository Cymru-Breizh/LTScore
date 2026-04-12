from .main import LTScore


def get_score(text):
    cysgor = LTScore(text)
    return cysgor.find_errors().score


def get_mistakes(text):
    cysgor = LTScore(text)
    return cysgor.find_errors().mistakes
