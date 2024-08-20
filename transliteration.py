def transliterate(string: str, language: str):
    if language == 'ru':
        alphabet = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-'
        }
    elif language == 'es':
        alphabet = {
            'a': 'a', 'á': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'é': 'e',
            'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'í': 'i', 'j': 'j', 'k': 'k',
            'l': 'l', 'm': 'm', 'n': 'n', 'ñ': 'n', 'o': 'o', 'ó': 'o', 'p': 'p',
            'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'ú': 'u', 'ü': 'u',
            'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z', ' ': '-'
        }
    elif language == 'fr':
        alphabet = {
            'a': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'b': 'b', 'c': 'c', 'ç': 'c',
            'd': 'd', 'e': 'e', 'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'f': 'f',
            'g': 'g', 'h': 'h', 'i': 'i', 'î': 'i', 'ï': 'i', 'j': 'j', 'k': 'k',
            'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'ô': 'o', 'ö': 'o', 'p': 'p',
            'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'ù': 'u', 'û': 'u',
            'ü': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'ÿ': 'y', 'z': 'z',
            ' ': '-'
        }
    elif language == 'de':
        alphabet = {
            'a': 'a', 'ä': 'ae', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f',
            'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm',
            'n': 'n', 'o': 'o', 'ö': 'oe', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's',
            't': 't', 'u': 'u', 'ü': 'ue', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y',
            'z': 'z', ' ': '-'
        }
    elif language == 'it':
        alphabet = {
            'a': 'a', 'à': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'é': 'e',
            'è': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'í': 'i', 'ì': 'i',
            'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'ó': 'o',
            'ò': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u',
            'ú': 'u', 'ù': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
            ' ': '-'
        }
    elif language == 'pt':
        alphabet = {
            'a': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'à': 'a', 'b': 'b', 'c': 'c',
            'ç': 'c', 'd': 'd', 'e': 'e', 'é': 'e', 'ê': 'e', 'f': 'f', 'g': 'g',
            'h': 'h', 'i': 'i', 'í': 'i', 'î': 'i', 'j': 'j', 'k': 'k', 'l': 'l',
            'm': 'm', 'n': 'n', 'o': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'p': 'p',
            'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'ú': 'u', 'û': 'u',
            'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z', ' ': '-'
        }
    string = string.lower()
    for l in string:
        if l in alphabet.keys():
            string = string.replace(l, alphabet.get(l))
        elif l in alphabet.values() or l == '-' or l.isdigit():
            continue
        else:
            string = string.replace(l, '')
    return string

if __name__ == '__main__':
    print(transliterate(str(input('Enter the text: ')), str(input('Enter the language: '))))

