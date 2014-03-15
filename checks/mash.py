#!/usr/bin/env python
import collections
import sys

if len(sys.argv) != 3 or '--help' in sys.argv:
    print 'Usage: faced.py schedule-file matchno'
    print '  Displays statistics about which others a team have faced'
    exit(1)

matches = []
lines = [x.strip() for x in open(sys.argv[1])]
for line in lines:
    players = line.split('|')
    while len(players) > 4:
        matches.append(players[0:3])
        players = players[4:]
    matches.append(players[0:3])

c = collections.defaultdict(collections.Counter)

def calc_faced_in_match(match, container):
    for tla in match:
        for faces in match:
            container[tla][faces] += 1

# Calculate how many times each team faces each other, except in the selected
# match
cur_match_no = 0
for match in matches:
    if cur_match_no == int(sys.argv[2]):
        continue

    calc_faced_in_match(match, c)
    cur_match_no += 1

all_teams = set(c.keys())

# Calculate a dictionary of how many times repeats happen: the size of the
# repeat maps to the number of times it happens. Due to an artifact of how
# this is counted, the "number of times" is twice as large as reality
def calc_scoring(c):
    output = collections.defaultdict(collections.Counter)

    for tla, opponents in c.iteritems():
        missed = all_teams - set(opponents.keys())
        del opponents[tla]
        all_repeats = {}
        faced = opponents.keys()
        for opp in faced:
            times = opponents[opp]
            output[times] += 1

    return output

def scoring_cmp(x, y):
    xkeys = x.keys()
    ykeys = y.keys()

    if xkeys != ykeys:
        # One of these dicts has a higher count of repeats than the other.
        xkeys = sorted(xkeys, reverse=True)
        ykeys = sorted(ykeys, reverse=True)

        highest = 0
        if xkeys[0] > ykeys[0]:
            highest = xkeys[0]
        else:
            highest = ykeys[0]

        for i in reversed(range(highest)):
            if i in xkeys and i not in ykeys:
                return 1
            elif i in ykeys and i not in xkeys:
                return -1
        return 0
    else:
        # They have the same set of keys.
        xkeys = sorted(xkeys, reverse=True)
        for i in xkeys:
            if x[i] < y[i]:
                return -1
            elif x[i] > y[i]:
                return 1
        return 0
