import csv
import math
from sys import argv
import copy

# Time Complexity - O(n * k) 
# assuming list indexing is constant time(I don't know how to create 2dim array
# without numpy)
# Memory - O(n * k) 
# dp[i][j][0] - maximum amount of money, considering that we have already 
# accomplished exactly j buy-transactions during first i rows of table
# and we don't have stocks on hands
# dp[i][j][1] - same, but having one stock on hands
# I assume that rows in csv are sorted by time

def solve(k, date, time, price, money = math.inf):
	if len(date) == 0:
		print("Profit: ", 0)
		return
	haveStock = [[-1 for y in range(k + 1)] for x in range(len(date))]
	noStock = [[-1 for y in range(k + 1)] for x in range(len(date))]
	parH = [[-1 for y in range(k + 1)] for x in range(len(date))]
	parN = [[-1 for y in range(k + 1)] for x in range(len(date))]
	noStock[0][0] = money
	for i in range(1, len(date)):
		haveStock[i] = copy.deepcopy(haveStock[i - 1])
		noStock[i] = copy.deepcopy(noStock[i - 1])
		parH[i] = copy.deepcopy(parH[i - 1])
		parN[i] = copy.deepcopy(parN[i - 1])
		for j in range(0, k + 1):
			if haveStock[i - 1][j] != -1 and haveStock[i - 1][j] + price[i] > noStock[i][j]:
				noStock[i][j] = haveStock[i - 1][j] + price[i]
				parN[i][j] = i - 1
			if j > 0 and price[i] <= noStock[i - 1][j - 1] and haveStock[i][j] < noStock[i - 1][j - 1] - price[i]:
				haveStock[i][j] = noStock[i - 1][j - 1] - price[i]
				parH[i][j] = i - 1
	optimalTransactionsNumber = 0
	for j in range(k + 1):
		if (noStock[len(date) - 1][j] > noStock[len(date) - 1][optimalTransactionsNumber]):
			optimalTransactionsNumber = j
	print("Profit: ", noStock[len(date) - 1][optimalTransactionsNumber] - noStock[0][0])
	choices = []
	currentTime = len(date) - 1
	while currentTime != -1:
		currentTime = parN[currentTime][optimalTransactionsNumber]
		if currentTime == -1:
			break
		choices.append([currentTime + 1])
		currentTime = parH[currentTime][optimalTransactionsNumber]
		choices[-1].append(currentTime + 1)
		optimalTransactionsNumber -= 1
	for moments in reversed(choices):
		print("Buy: ", date[moments[1]], time[moments[1]], price[moments[1]])
		print("Sell: ", date[moments[0]], time[moments[0]], price[moments[0]])
		print("Diff: ", price[moments[0]] - price[moments[1]])

#beneath is reading and parsing
scriptName, path = argv
table = open(path)
date, time, price = [0], [0], [0]
reader = csv.DictReader(table)
for info in reader:
	date.append(int(info["date"]))
	time.append(int(info["time"]))
	price.append(float(info["price"]))
maximumTransactions = int(input())
money = float(input())
solve(maximumTransactions, date, time, price, money)
table.close()