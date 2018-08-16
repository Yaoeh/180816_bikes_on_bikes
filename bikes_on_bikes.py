'''
180815 WED

Interesting reads:
	a. https://stackoverflow.com/questions/9660085/python-permutations-with-constraints
	b. Multi set permutations at O(1) http://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1644-10.pdf

Basically the problem is one of a multiset combination
	http://www.kcats.org/csci/464/doc/knuth/fascicles/fasc3a.pdf (check page 16)

Constraints: 
	a. the sum of the bike movements has to be zero
	b. the bikes at the rack cannot exceed 10 and cannot go below zero
	The actual list representation is n* 2, where first 0 -> n/2-1 is each rack, and n/2 -> n is for movement

[RACK, MOVE]

'''
import itertools, json, logging, datetime, time

class BikesForDays():
	def __init__(self, bike_rack_list):
		self.bike_rack_length= len(bike_rack_list)
		self.total_number_of_bicycles= sum(bike_rack_list)
		self.rack_min_value= 0
		self.rack_max_value= 10
		self.move_min_value= -10
		self.move_max_value= 10
		self.save_file= 'solution_%s.json' % self.bike_rack_length

		'''META STUFF '''
		self.solution= []
		self.total_count= 0
		self.total_valid_count= 0
		logging.basicConfig(filename='bikes_on_bikes_%s.log' % self.bike_rack_length,level=logging.DEBUG)
		logging.getLogger().addHandler(logging.StreamHandler())
		logging.info('creating bike for days for %s stations' % self.bike_rack_length)

	def get_starting_list(self):
		return [self.rack_min_value] * self.bike_rack_length+ [self.move_min_value] * self.bike_rack_length

	def convert_lists_to_str(self, cool_list):
		return ','.join([str(v) for v in cool_list])

	def is_valid(self, cool_list):
		'''
		a state is valid if the move adds up to zero, and each element of the move cannot make the combined value exceed the max rack nor go below the min rack
		'''
		same_number_of_bikes= sum(cool_list[:self.bike_rack_length]) == self.total_number_of_bicycles
		racks_in_range= not any([self.rack_min_value > cool_list[n] > self.rack_max_value for n in range(self.bike_rack_length)]) 
		sum_is_zero= sum(cool_list[self.bike_rack_length: self.bike_rack_length*2]) == 0 
		movement_is_legit= not any([cool_list[n] + cool_list[n -self.bike_rack_length] < self.rack_min_value or (cool_list[n] + cool_list[n-self.bike_rack_length]) > self.rack_max_value for n in range(self.bike_rack_length, self.bike_rack_length*2)])

		return same_number_of_bikes and racks_in_range and sum_is_zero and movement_is_legit

	def solve_problem(self):
		logging.info('generating total list for combinations')
		tots= []
		for n in range(self.bike_rack_length):
			tots.append(list(range(self.rack_min_value, self.rack_max_value+1)))

		for n in range(self.bike_rack_length):
			tots.append(list(range(self.move_min_value, self.move_max_value+1)))

		logging.info('combination list generation complete. Length: %s' % len(tots))
		logging.info('starting generation...')
		logging.info('-'*80)
		#p = itertools.product(*tots)
		#l =[]

		for p in itertools.product(*tots):
			#logging.info(p)
			self.total_count+= 1
			if self.is_valid(p):
				logging.info('[%s] %s'% (self.total_valid_count, p))
				self.total_valid_count+= 1
				#l.append(p)

		self.print_meta()

	def print_meta(self):
		logging.info('-'*80)
		logging.info('Total valid count: %s' % self.total_valid_count)
		logging.info('Total count: %s' % self.total_count)
		logging.info('Percentage of valids in search space: %s' % (self.total_valid_count*1.0/self.total_count))

	def get_max_range(self, index):
		assert index < self.bike_rack_length*2
		if index < self.bike_rack_length:
			return self.rack_max_value
		else:
			return self.move_max_value

	def get_min_range(self, index):
		assert index < self.bike_rack_length*2
		if index < self.bike_rack_length:
			return self.rack_min_value
		else:
			return self.move_min_value

	def check_break_condition(self, cool_list): #skipping some checks
		should_break= False
		for n in range(self.bike_rack_length):
			if sum(cool_list[:n]) > self.total_number_of_bicycles:
				should_break= True
				break

		if (not should_break): #don't need to check if should already break
			for n in range(self.bike_rack_length, self.bike_rack_length*2):
				if sum(cool_list[n:]) > self.total_number_of_bicycles:
					should_break= True
					break

		return should_break

	def solve_problem_like_a_boss(self, cool_list_str, n):
		self.total_count+= 1
		#print('Running: %s' % cool_list_str + ' ' * 100, end='\r')
		cool_list= [int(v) for v in cool_list_str.split(',')]
		
		if (self.check_break_condition(cool_list)): #if breaking
			# for m in range(n, self.bike_rack_length*2): #set the string to the next one
			# 	cool_list[m]= self.get_min_range(m)

			#return self.solve_problem_like_a_boss(self.convert_lists_to_str(cool_list), self.bike_rack_length*2)
			return

		if n < self.bike_rack_length*2: #not all digits are filled yet
			for x in range(self.get_min_range(n), self.get_max_range(n)+1):
				cool_list[n]= x #set the digit at that list's location
				self.solve_problem_like_a_boss(self.convert_lists_to_str(cool_list), n+1)
		else: #whole digit is filled
			if (self.is_valid(cool_list)):
				self.total_valid_count += 1
				self.solution.append(cool_list)	
				logging.info('[%s] %s'% (self.total_valid_count, cool_list))

	def solve_problem_like_a_boss2(self, cool_list, n):
		self.total_count+= 1
		#print('Running: %s' % cool_list + ' ' * 100, end='\r')
		#cool_list= [int(v) for v in cool_list_str.split(',')]
		
		if (self.check_break_condition(cool_list)): #if breaking
			return

		if n < self.bike_rack_length*2: #not all digits are filled yet
			for x in range(self.get_min_range(n), self.get_max_range(n)+1):
				cool_list[n]= x #set the digit at that list's location

				for m in range(n+1, self.bike_rack_length*2): #resetting the list
					cool_list[m]= self.get_min_range(m)

				self.solve_problem_like_a_boss2(cool_list, n+1)
		else: #whole digit is filled
			if (self.is_valid(cool_list)):
				self.total_valid_count += 1
				self.solution.append(list(cool_list)	)
				logging.info('[%s] %s'% (self.total_valid_count, cool_list))

	def save_solution(self):
		with open(self.save_file, 'w') as f:
			json.dump(self.solution, f)


if __name__ == '__main__':
	bfd= BikesForDays([4,4,4,4])
	start_time = time.time()
	#bfd.solve_problem()
	#bfd.solve_problem_like_a_boss(bfd.convert_lists_to_str(bfd.get_starting_list()), 0)
	bfd.solve_problem_like_a_boss2(bfd.get_starting_list(), 0)
	bfd.print_meta()
	elapsed_time = time.time() - start_time
	logging.info('Time elapsed: %s' % time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
	bfd.save_solution()
	logging.info('run complete.')


