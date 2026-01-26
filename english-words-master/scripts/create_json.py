import sys
import json

words = open(sys.argv[1])
word_list = words.readlines()
json_words = {word.rstrip(): "1" for word in word_list}

print(json.dumps(json_words, indent=4))
