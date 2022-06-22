import re

from django import template


register = template.Library()

CENSORED = [
    'редиска',
    'жопа',
    'дурак',

]


@register.filter(name='censor')
def censor(text):

    if isinstance(text, str):
        cens_text = []
        l_text = text.split()

        while l_text:
            word = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", l_text[0])
            l_word = word.split()
            cens_word = []

            for i in l_word:
                if i.lower() in CENSORED:
                    bad_word = i[0] + '*' * (len(i) - 1)
                    cens_word.append(bad_word)
                else:
                    cens_word.append(i)

            cens_text.append("".join(cens_word))
            l_text.remove(l_text[0])

        return " ".join(cens_text)

    else:
        raise TypeError("Фильтр применим только к переменным строкового типа!")
