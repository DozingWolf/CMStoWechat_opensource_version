import hashlib
import sys
import json


def hashchecker(p_path):
    hash_text = hashlib.sha1(open(file=p_path,mode='r').read().encode('utf-8')).hexdigest()
    print('calc\'s hash was:',hash_text)

hashchecker(sys.argv[1])
