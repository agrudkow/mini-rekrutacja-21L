from typing import List, TextIO


def convert_char_to_decimal(char: str) -> int:
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


def converter(number: str, base: int) -> int:
    # split number in figures
    figures = [convert_char_to_decimal(i) for i in number]
    # invert oder of figures (lowest count first)
    figures = figures[::-1]
    result: int = 0
    # loop over all figures
    for i in range(len(figures)):
        # add the contirbution of the i-th figure
        result += figures[i] * base**i
    return result


def decode_nunmbers(base: int, number: str) -> int:
    return converter(number, base)


def extract_encoded_numbers(line: str) -> List[int]:
    extracted_encoded_numbers: List[int] = []

    for encoded_tuple in line.split(';'):
        base, number = encoded_tuple.split(':')
        converted_base = convert_char_to_decimal(base) + 1
        extracted_encoded_numbers.append(
            decode_nunmbers(converted_base, number))

    return extracted_encoded_numbers


def parse_to_decimal(line: str) -> List[int]:
    extracted_encodings = extract_encoded_numbers(line)
    # print(extracted_encodings)
    return extracted_encodings


def map_file(file: TextIO) -> List[List[int]]:
    parsed_list: List[List[int]] = []
    for line in file:
        parsed_list.append(parse_to_decimal(line.strip().rstrip(';')))
    return parsed_list


if __name__ == '__main__':
    with open('data_1') as file:
        print('numbers', map_file(file))
