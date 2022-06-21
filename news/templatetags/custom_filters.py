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

            for i in l_word:
                count = len(l_word) - 1

                if count == 0 and i.lower() in CENSORED:
                    bad_word = i[0] + '*' * (len(i) - 1)
                    cens_text.append(bad_word)
                    break

                if count and i.lower() in CENSORED:
                    bad_word = i[0] + '*' * (len(i) - 1)
                    g = "".join(l_word)
                    res = g.replace(i, bad_word)
                    cens_text.append(res)
                    break

                if count == 0 and i.lower() not in CENSORED:
                    res = "".join(l_word)
                    cens_text.append(res)
                    break

                if count and i.lower() not in CENSORED:
                    res = "".join(l_word)
                    cens_text.append(res)
                    break

            l_text.remove(l_text[0])

        return " ".join(cens_text)

    else:
        raise TypeError("Фильтр применим только к переменным строкового типа!")
