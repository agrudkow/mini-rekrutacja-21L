from typing import List, TextIO


def convert_char_to_decimal(char: str) -> int:
    '''
    Funkcja konvertująca znaki do reprezentacji decymalnej
    wskazanej w treści zadania.
    '''
    ascii_repr = ord(char)

    if ascii_repr >= ord('0') and ascii_repr <= ord('9'):
        return int(char, base=10)
    elif ascii_repr >= ord('a') and ascii_repr <= ord('z'):
        return ascii_repr - 87
    elif ascii_repr >= ord('A') and ascii_repr <= ord('Z'):
        return ascii_repr - 29
    else:
        msg = 'Invalid character {}'.format(char)
        raise RuntimeError(msg)


def converter_base_to_decimal(number: str, base: int) -> int:
    '''
    Funkcja konwertująca liczbę w reprezentacji o podstawie
    `base` do reprezentacji dziesiętnej
    '''
    # Rozdziel liczbę na pszczególne znaki (liczby)
    # Konwertuj znaki do postaci decymalnej
    figures = [convert_char_to_decimal(i) for i in number]
    # Odwróć kolejność liczb
    figures = figures[::-1]

    result: int = 0
    # Iteruj po liczbach i agregują sumę po konwersji
    for i in range(len(figures)):
        result += figures[i] * base**i
    return result


def decode_number(encoded_number: str) -> int:
    '''
        Funkcja dekodująca pojedynczą zakodowaną liczbę.

        Funkcja rozdziela liczbę od jej bazy i wywołuje
        na niej konwerter.
    '''
    base, number = encoded_number.split(':')
    converted_base = convert_char_to_decimal(base) + 1
    return converter_base_to_decimal(number, converted_base)


def decode_numbers(encoded_numbers: List[str]) -> List[int]:
    '''
    Funkcja iterująca po liście zakodowanych liczb
    i wywołująca na nich funkcję dekodującą. Funkcja
    ta zwraca zdekodowaną listę liczb.
    '''
    return [
        decode_number(encoded_number) for encoded_number in encoded_numbers
    ]


def map_file(file: TextIO) -> List[List[int]]:
    '''
    Funkcja iterująca po kolejnych liniach w pliku `file`
    i zwracająca dla każdej lini listę zdekodowanych
    liczb do reprezentacji dziesiętnej.

    Każda koljna linia jest pozbawiana początkowych i końcowych
    znaków białych oraz końcowego średnika, a do funkjcji dekodującej
    przekazywane są wekstrahowane, zakodowane liczby.
    '''
    parsed_list: List[List[int]] = []
    for line in file:
        line = line.strip().rstrip(';')
        parsed_list.append(decode_numbers(line.split(';')))
    return parsed_list


if __name__ == '__main__':
    results: List[List[int]] = []

    with open('data_1') as file:
        results = map_file(file)

    for line in results:
        print(line)
