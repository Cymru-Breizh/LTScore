from .main import LTScore


def get_score(text, language):
    wrapper = LTScore(language=language, input_text=text)
    return wrapper.find_errors().score


def get_mistakes(text, language):
    wrapper = LTScore(language=language, input_text=text)
    return wrapper.find_errors().mistakes
