import krovetz
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("term", help="Token to be stemmed")

args = parser.parse_args()

token = args.term

ks = krovetz.PyKrovetzStemmer()
stem = ks.stem(token)

print(stem)

