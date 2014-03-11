#!/usr/bin/env python
from collections import defaultdict, Counter
import sys

if len(sys.argv) != 2 or '--help' in sys.argv:
    print 'Usage: close.py <schedule-file>'
    print '  Displays statistics about how close the matches for all teams are.'
    print '  A min-gap of 3 indicates that a team has a match, followed by two'
    print '  match intervals off, and then another match.'
    exit(1)

lines = open(sys.argv[1], 'r').readlines()

matches = defaultdict(lambda: [])
breaks = defaultdict(lambda: [])

match_num = 1

for line in lines:
    if line.strip() == "":
        continue
    teams = line.strip().split('|')
    for tla in teams:
        matches[tla].append(int(match_num))

    match_num += 1

min_breaks = []

for tla, matches in matches.iteritems():
    last_match = -25
    min_break = 200
    for match in matches:
        diff = match - last_match
        breaks[tla].append(diff)
        if diff < min_break:
            min_break = diff
        last_match = match
    min_breaks.append((tla, min_break, breaks[tla]))

print 'Team\tMin-gap\tCount\tGaps'

count_n = 0
for tla, min_break, btla in sorted(min_breaks, key=lambda x:x[1]):
    c = Counter()
    for x in sorted(btla):
        c[x] += 1
    if min_break == 2:
        count_n += 1
    print "{0}\t{1}\t{2}\t{3}".format(tla, min_break, c[min_break], btla)

print
print count_n
