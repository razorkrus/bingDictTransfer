"""
Script used to transfer the vocabulary of Bing Dict to Youdao Dict.
Vocabulary of Bing Dict is saved in '1000'.

Need to install 'keyboard' module.
"""
from xml.etree.ElementTree import parse
import keyboard
import time
import argparse


def parse_xml(file_name, unit_name, property_name) -> set:
    """
    Parse the xml format file, and extract the required property text while iterating on all qualified unit.
    The result is saved in a set and returned.

    :param file_name: file name to be parsed. Assuming the file is saved in pwd.
    :param unit_name: unit name to be iterated on the parsed file.
    :param property_name: property name to be extracted from the unit.
    :return: set containing all the property text.
    """
    with open(file_name, 'r', encoding='utf8') as f:
        doc = parse(f)
        res = {unit.find(property_name).text for unit in doc.iter(unit_name)}
    return res


def compare_voca(bing_file, youdao_file, print_intersection=False) -> list:
    bing_para = ['WordUnit', 'HeadWord']
    youdao_para = ['item', 'word']
    bing_voca = parse_xml(bing_file, *bing_para)
    youdao_voca = parse_xml(youdao_file, *youdao_para)

    if print_intersection:
        for w in bing_voca and youdao_voca:
            print(w, end=' ')

    res = list(bing_voca - youdao_voca)
    return sorted(res)


def write_to_file(words, filename='wordlist'):
    with open(filename, 'w', encoding='utf8') as f:
        for word in words:
            f.write(word+'\n')


def add_words_to_youdao(words, start_key='enter'):
    """
    Used to simulate the keyboard input to add very word in words to the vocabulary of youdao dict.
    The sleep parameters is tested on my desktop.

    :param words: words to be added.
    :param start_key: keyboard input used to start the keyboard simulating process.
    :return: None
    """
    save_hotkey = 'ctrl+alt+s'
    t0 = 0.1
    t2 = 0.4

    keyboard.wait(start_key)
    for word in words:
        keyboard.write(word)
        time.sleep(t0)
        keyboard.press_and_release('enter')
        time.sleep(t2)
        keyboard.press_and_release(save_hotkey)
        time.sleep(t2)
        keyboard.press_and_release('backspace')


def generate_args():
    parser = argparse.ArgumentParser(description='Transfer the bing dict vocabulary into youdao dict.')

    parser.add_argument('-d', '--duplicate', help='print out the duplicated words if any',
                        action='store_true')
    parser.add_argument('-w', '--write', help='write the sorted word list into file',
                        action='store_true')
    parser.add_argument('-x', '--execute', help='execute the simulation of the keyboard input in application',
                        action='store_true')

    return parser.parse_args()


def main():
    args = generate_args()
    bing_filename = '1000'
    youdao_filename = 'youdao.xml'

    new_words = compare_voca(bing_filename, youdao_filename, args.duplicate)
    if args.write:
        write_to_file(new_words)

    if args.execute:
        add_words_to_youdao(reversed(new_words))


if __name__ == '__main__':
    main()
