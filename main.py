import argparse
import csv
from random import shuffle

def breakdownLine(contents: list):
    print('Contents ' + str(contents))
    return [contents[1], contents[2], contents[3]]


def process(filename: str, group_len_cap: int):
    words = []

    try:
        wordlist_file = open(filename, 'r', encoding='utf8')
    except FileNotFoundError:
        print('File not found')
        return
    except Exception as err:
        print('Unexpected error opening {fname} is', repr(err))
        return
    with wordlist_file:
        for line in wordlist_file:

            text_split = line.split('\t')

            if len(text_split) < 4:
                continue

            data = breakdownLine(text_split)
            words.append(data)

    shuffle(words)

    count = 0
    group = 0
    writing_file = None
    csv_handle = None

    print('Words processed: ' + str(len(words)))

    for i in range(len(words)):

        if count % group_len_cap == 0:
            group = i / group_len_cap

            if writing_file is not None:
                writing_file.close()

            writing_file = open(filename + '-' + str(group) + '.csv', 'w', newline='', encoding='utf-8-sig')
            csv_handle = csv.writer(writing_file, quoting=csv.QUOTE_ALL)

        word = words[i]
        csv_handle.writerow([word[0], word[1], word[2]])
        count += 1

    writing_file.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', dest='filename', type=str, required=True, help='Filename to process')
    parser.add_argument('--word_group_len', dest='grouplen', type=str, required=True, help='Amount of words per group')

    args = parser.parse_args()

    process(args.filename, int(args.grouplen))
