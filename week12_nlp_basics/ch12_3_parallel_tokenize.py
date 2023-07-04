import csv
import os

from konlpy.tag import Komoran
from tqdm.contrib.concurrent import process_map

komoran = Komoran(userdic="./data/user.dic")


def load_data():
    data = []
    with open("./data/baseball_preprocessed.csv") as fr:
        reader = csv.reader(fr)
        next(reader)
        for row in reader:
            data.append(row)
    return data


def tokenize(row):
    def _tokenize(x):
        try:
            tokens = komoran.pos(x)
            return tokens
        except Exception as e:
            print(e, x)
            return None
    url, datetime_str, title, content = row
    title_tokens = _tokenize(title)
    content_tokens = _tokenize(content)

    return url, datetime_str, title, content, title_tokens, content_tokens


def write_tokenized_data(data):
    with open("./data/baseball_tokenized.csv", "w") as fw:
        writer = csv.writer(fw)
        writer.writerow(["url", "datetime_str", "title", "content", "title_tokens", "content_tokens"])
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    data = load_data()
    tokenized_data = process_map(tokenize, data, max_workers=4)
    write_tokenized_data(tokenized_data)