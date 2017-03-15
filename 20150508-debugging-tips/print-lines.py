import sys
try:
    quote_path = sys.argv[1]
except IndexError:
    quote_path = 'quote1.txt'
for line in open(quote_path, 'rt'):
    print(line)
