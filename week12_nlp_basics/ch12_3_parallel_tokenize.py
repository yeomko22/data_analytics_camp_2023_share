import csv

from konlpy.tag import Komoran
from tqdm.contrib.concurrent import process_map

komoran = Komoran(userdic="./data/user.dic")
