import sys

piece_score = {'X' : 1, 'Y' : 2, 'Z' : 3}

results = {'A' : {'X' : 3, 'Y' : 6, 'Z' : 0},
           'B' : {'X' : 0, 'Y' : 3, 'Z' : 6},
           'C' : {'X' : 6, 'Y' : 0, 'Z' : 3}}

data = []

with open(sys.argv[1], 'r') as file:
    for line in file:
        theirs, ours = line.strip().split()
        data.append((theirs, ours))

score = 0
for theirs, ours in data:
        score += piece_score[ours] + results[theirs][ours]

print(score)

#for part 2 we can construct the required move from the results table

moves = {}

for theirs, table in results.items():
    moves[theirs] = {}
    for ours, result in table.items():
        if result == 0:
            moves[theirs]['X'] = ours
        elif result == 3:
            moves[theirs]['Y'] = ours
        else:
            moves[theirs]['Z'] = ours
            
score = 0
for theirs, result in data:
    our_move = moves[theirs][result]
    score += piece_score[our_move] + results[theirs][our_move]
    

print(score)
