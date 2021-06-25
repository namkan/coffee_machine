from concurrent import futures

class Beverage(object):
	def __init__(self, name):
		self.__name = name
		self.__ingredients = {}

	@property
	def name(self):
		return self.__name
	
	def add_required_ingredient(self, ingredient, quantity): # This function helps us adding required ingredient and their quantity.
		self.__ingredients[ingredient] = quantity

	def get_all_ingredients_required(self):
		return self.__ingredients

class CoffeeMachine(object):
	def __init__(self, outlets):
		self.__outlets = outlets
		self.__beverages = []
		self.__beverage_names = []
		self.__total_available_ingredients = {}

	def _dispense(self, beverage_name): #Private function to dispense a single beverage
		if beverage_name not in self.__beverage_names:
			raise Exception("%s is not available." % beverage_name)
		for beverage in self.__beverages: #Get beverage object from beverage name
			if beverage.name == beverage_name:
				beverage_obj = beverage
				break
		
		#Show warning if ingredient is not available or not sufficient
		ingredients_required = beverage_obj.get_all_ingredients_required()
		for ingredient, quantity in ingredients_required.items():
			if ingredient not in self.__total_available_ingredients:
				print("%s can not be prepared because %s is not available." % (beverage_name, ingredient))
				return 
		for ingredient, quantity in ingredients_required.items():
			if self.__total_available_ingredients[ingredient] < quantity:
				print("%s can not be prepared because %s is not sufficient." % (beverage_name, ingredient))
				return

		#Reduce the quantity of available ingredients by the amount required to make beverage
		for ingredient, quantity in ingredients_required.items():
			self.__total_available_ingredients[ingredient] = self.__total_available_ingredients[ingredient] - quantity
		
		print("%s is prepared." % beverage_name)

	def refill_ingredient(self, ingredient, quantity_to_add): # Refill an ingredient if it is not sufficient
		available_quantity = self.__total_available_ingredients.get(ingredient,0)
		self.__total_available_ingredients[ingredient] = available_quantity + quantity_to_add

	def get_all_available_ingredients(self): #Getter function to see all available ingredients and there quantity
		return self.__total_available_ingredients

	def add_beverage(self, beverage): #Method to add a beverage to coffee machine. Accepts a beverage object.
		if len(self.__beverages) == self.__outlets:
			raise Exception("Already %s beverages. No more beverages can be added." % self.__outlets)
		self.__beverages.append(beverage)
		self.__beverage_names.append(beverage.name)

	def dispense_beverages(self, beverage_names): #Public method to dispense multiple beverages parallelly
		executor = futures.ThreadPoolExecutor(self.__outlets) #Making thread to execute them parallelly
		jobs = [executor.submit(self._dispense, beverage) for beverage in beverage_names]
		futures.wait(jobs)

