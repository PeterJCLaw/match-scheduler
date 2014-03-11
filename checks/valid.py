#!/usr/bin/env python
import sys

if len(sys.argv) != 3 or '--help' in sys.argv:
    print 'Usage: valid.py <schedule-file> <teams-file>'
    print '  Ensures that all the teams listed (one TLA per line) are in the schedule'
    exit(1)

all_teams = [x.strip() for x in open(sys.argv[2], 'r').readlines()]

lines = open(sys.argv[1], 'r').readlines()

found_teams = []

for line in lines:
    line = line.strip()
    if len(line) == 0:
        continue
    teams = [x.strip() for x in line.strip().split('|')]
    #print line
    assert len(set(teams)) == len(teams) == 4, teams
    found_teams += teams

# Sanity
assert len(set(all_teams)) == len(all_teams), all_teams

# Sanity
missing_teams = set(all_teams) - set(found_teams)
print ', '.join(missing_teams)
assert len(set(found_teams)) == len(all_teams)

print 'Is valid'
