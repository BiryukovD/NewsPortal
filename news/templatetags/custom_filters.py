from django import template

register = template.Library()

@register.filter()
def censor(phrase):
    words = ['яблоко', 'арбуз', 'зарегистрировались', 'Поисковик', 'мнениях', 'Гарри']
    for word in words:
        fragments = []
        for part in range(len(phrase)):
            fragment = phrase[part: part + len(word)]
            fragments.append(fragment)

        for i, fragment in enumerate(fragments):
            if word == fragment:
                phrase_list = list(phrase)
                for ind in range(i + 1, i + len(word)):
                    phrase_list[ind] = '*'
                phrase = ''.join(phrase_list)

    return phrase
