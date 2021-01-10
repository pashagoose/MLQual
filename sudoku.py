import pickle

class State:
	BIG_SQR_SZ = 9
	SMALL_SQR_SZ = 3
	__table = [[]]

	def __clear(self):
		self.__table = [[0 for x in range(State.BIG_SQR_SZ)] for y in range(State.BIG_SQR_SZ)]

	def __init__(self):
		self.__clear()

	def __str__(self):
		result = ""
		print(len(self.__table))
		for i in range(State.BIG_SQR_SZ):
			for j in range(State.BIG_SQR_SZ):
				if (self.__table[i][j] == 0):
					result += '*'
				else:
					result += str(self.__table[i][j])	
			result += '\n'
		return result

	def __checkSmallSquareUniqueness(self, i, j):
		seen = set()
		for x in range(0, State.SMALL_SQR_SZ):
			for y in range(0, State.SMALL_SQR_SZ):
				if self.__table[i + x][j + y] != 0:
					if self.__table[i + x][j + y] in seen:
						return False
					else:
						seen.add(self.__table[i + x][j + y])
		return True

	def __checkPlacement(self, i, j, dig):
		if (i < 0 or i >= State.BIG_SQR_SZ or j < 0 or j >= State.BIG_SQR_SZ or self.__table[i][j] != 0):
			raise IndexError("wrong index")
		if (dig < 0 or dig > 9):
			raise ValueError("wrong digit")


	def __checkUniqueness(self):
		# checking uniqueness in rows
		for i in range(State.BIG_SQR_SZ):
			seen = set()
			for j in range(State.BIG_SQR_SZ):
				if self.__table[i][j] != 0:
					if self.__table[i][j] in seen:
						return False
					else:
						seen.add(self.__table[i][j])

		# checking uniqueness in columns
		for i in range(State.BIG_SQR_SZ):
			seen = set()
			for j in range(State.BIG_SQR_SZ):
				if self.__table[j][i] != 0:
					if self.__table[j][i] in seen:
						return False
					else:
						seen.add(self.__table[j][i])

		# checking uniqueness in squares
		for i in range(0, State.BIG_SQR_SZ, State.SMALL_SQR_SZ):
			for j in range(0, State.BIG_SQR_SZ, State.SMALL_SQR_SZ):
				if not self.__checkSmallSquareUniqueness(i, j):
					return False
		return True

	def set(self, i, j, dig):
		i -= 1
		j -= 1
		try:
			self.__checkPlacement(i, j, dig)
		except Exception as e:
			raise e
		self.__table[i][j] = dig
		if not self.__checkUniqueness():
			self.__table[i][j] = 0
			raise ValueError("uniqueness is broken")

	def init(self):
		filled_cells = int(input())
		self.__table = [[0 for x in range(State.BIG_SQR_SZ)] for y in range(State.BIG_SQR_SZ)]
		for i in range(filled_cells):
			x, y, dig = map(int, input().split())
			x -= 1
			y -= 1
			try:
				self.__checkPlacement(x, y, dig)
			except Exception as e:
				self.__clear()
				raise e
			self.__table[x][y] = dig
		if not self.__checkUniqueness():
			self.__clear()
			raise ValueError("uniqueness is broken")

	def save(self, path):
		try:
			file = open(path, 'wb')
		except Exception as e:
			raise e
		try:
			pickle.dump(self.__table, file)
		except Exception as e:
			raise e
		file.close()

	def load(self, path):
		try:
			file = open(path, 'rb')
		except Exception as e:
			raise e
		try:
			new_table = pickle.load(file)
		except Exception as e:
			raise e
		self.__table = new_table
		file.close()


class Session:
	__state = State()
	__name = "defaultSession"

	def __init__(self):
		self.__state = State()

	def userSet(self, command):
		try:
			self.__state.set(int(command[1]), int(command[2]), int(command[3]))
		except Exception as e:
			print(e)

	def userInit(self, command):
		try:
			self.__state.init()
		except Exception as e:
			print(e)

	def userSave(self, command):
		try:
			path = self.__name + ".pkl"
			if len(command) > 1:
				path = command[1] + "/" + path
			self.__state.save(path)
		except Exception as e:
			print(e)

	def userLoad(self, command):
		try:
			self.__state.load(command[1])
		except Exception as e:
			print(e)

	def rename(self, command):
		try:
			new_name = command[1]
		except Exception as e:
			print(e)
		self.__name = new_name

	def startCommunicating(self):
		while True:
			command = input().split()
			if command[0] == "set":
				self.userSet(command)
			if command[0] == "init":
				self.userInit(command)
			if command[0] == "rename":
				self.rename(command)
			if command[0] == "save":
				self.userSave(command)
			if command[0] == "load":
				self.userLoad(command)
			if command[0] == "exit":
				break
			print(self.__name)
			print(self.__state)
		
game = Session()
game.startCommunicating()