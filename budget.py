

class Category:

	def __init__(self, category_name):
		self.category_name = category_name
		self.ledger = []

	def deposit(self, amount, description=''):
		self.ledger.append({'amount': amount, 'description': description})

	def withdraw(self, amount, description=''):
		enough_funds = self.check_funds(amount)
		if enough_funds:
			self.ledger.append({'amount': -amount, 'description': description})
			return True
		else:
			return False

	def get_balance(self):
		# balance = sum of all amounts
		return sum(x['amount'] for x in self.ledger)

	def transfer(self, amount, destination):
		if isinstance(destination, Category):
			enough_funds = self.check_funds(amount)
			if enough_funds:
				# withdraw money from this category
				self.withdraw(amount, f'Transfer to {destination.category_name}')
				# add a deposit to the destination category
				destination.deposit(amount, f'Transfer from {self.category_name}')
				return True
			else:
				return False
		else:
			return f'{destination} is Invalid'

	def check_funds(self, amount):
		if amount <= self.get_balance():
			return True
		else:
			return False

	def __str__(self):
		title = f'{self.category_name}'.center(30, '*')
		amount, description = [], []
		for transaction in self.ledger:
			amount.append(transaction['amount'])
			description.append(transaction['description'][0:23])
		total = '{:.2f}'.format(self.get_balance())

		output = ''
		output += title + '\n'
		for amnt, desc in zip(amount, description):
			rjust = 30 - len(desc)
			amnt = '{:.2f}'.format(amnt)
			output += desc + amnt.rjust(rjust) + '\n'
		output += f'Total: {total}'

		return output



class Chart:
	@classmethod
	def round_down(cls, decimal):
		str_decimal = '{:.2f}'.format(decimal)
		if int(str_decimal[-1]) > 0:
			return float(f'{str_decimal[:len(str_decimal)-1]}0')
		else:
			return float(str_decimal)

	@classmethod
	def withdraws(cls, category):
		withdrawals = []
		category_ledger = category.ledger
		for transaction in category_ledger:
			if transaction['amount'] <= 0:
				current_trans = {'amount': transaction['amount'], 'description': transaction['description']}
				withdrawals.append(current_trans)
		return withdrawals

	@classmethod
	def withdraw_totals(cls, category_names, list_of_categories):
		category_withdrawal_totals = {}
		for name, category in zip(category_names, list_of_categories):
			category_withdraws = cls.withdraws(category)
			for withdrawal in category_withdraws:
				category_withdrawal_totals[name] = sum(abs(withdraw['amount']) for withdraw in category_withdraws)
		return category_withdrawal_totals

	@classmethod
	def withdrawalRatios(cls, category_withdrawal_totals, total_withdrawals):
		ratio = lambda x, y: x / y
		withdrawals_ratios = []
		for withdrawal in category_withdrawal_totals:
			x = cls.round_down(ratio(abs(category_withdrawal_totals[withdrawal]), total_withdrawals)) * 100
			withdrawals_ratios.append(x)
		return withdrawals_ratios

	@classmethod
	def x_axis(cls, category_names_list):
		longest = 0
		for category in category_names_list:
			if len(category) > longest:
				longest = len(category)
		x_axis = [''] * longest	# [list of chars for each row]
		for name in category_names_list:
			if len(name) < longest:
				name += ' ' * (longest - len(name))
			for index, char in enumerate(name):
				x_axis[index] += f"{char}  "
		return x_axis

	@classmethod
	def bars(cls, list_of_ratios, category_names_list):
		graph = {}	# Dictionary consisting of: category: [bars per line]
		for ratio, category in zip(list_of_ratios, category_names_list):
			num_list = [x for x in range(0, 101, 10)]
			num_list.reverse()
			for num in num_list:
				if num == num_list[0]:
					graph[category] = []
				if num <= ratio:
					graph[category].append('o  ')
				elif num > ratio:
					graph[category].append('   ')
		bars = [''] * 11
		for category, items in graph.items():
			for index, item in enumerate(items):
				bars[index] += item
		return bars

	@classmethod
	def chart_format(cls, list_of_ratios, category_names_list):
		title = 'Percentage spent by category\n'
		y_axis = [str(x).rjust(3) + '| ' for x in range(0, 101, 10)]
		dashes = f"{' ' * 4}{'-' * (len(category_names_list) + (2 * len(category_names_list)) + 1)}"
		x_axis = cls.x_axis(category_names_list)

		bars_ = cls.bars(list_of_ratios, category_names_list)

		output = f'{title}'
		y_axis.reverse()
		for yAxis, bar in zip(y_axis, bars_):
			output += yAxis + bar + '\n'
		output += dashes + '\n'
		n = 1
		for row in x_axis:
			output += f"{' ' * 5}{row}"
			if n != len(x_axis):
				output += '\n'
				n += 1

		return output



def create_spend_chart(list_of_categories):

	category_names = [category.category_name for category in list_of_categories]
	category_withdrawal_totals = Chart.withdraw_totals(category_names, list_of_categories)
	total_withdrawals = sum(category_withdrawal_totals[amount] for amount in category_withdrawal_totals)
	withdrawals_ratios = Chart.withdrawalRatios(category_withdrawal_totals, total_withdrawals)

	return Chart.chart_format(withdrawals_ratios, category_names)
