import unittest
import random

from CoffeeMachine import CoffeeMachine, Beverage

input_test_json = {
  "machine": {
    "outlets": {
      "count_n": 4
    },
    "total_items_quantity": {
      "hot_water": 500,
      "hot_milk": 500,
      "ginger_syrup": 100,
      "sugar_syrup": 100,
      "tea_leaves_syrup": 100
    },
    "beverages": {
      "hot_tea": {
        "hot_water": 200,
        "hot_milk": 100,
        "ginger_syrup": 10,
        "sugar_syrup": 10,
        "tea_leaves_syrup": 30
      },
      "hot_coffee": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "hot_milk": 400,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "black_tea": {
        "hot_water": 300,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "green_tea": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "green_mixture": 30
      },
    }
  }
}

class TestCoffeeMachine(unittest.TestCase):

	def setUp(self): # setup function to intialize the objects needed.
		self.CoffeeMachine = CoffeeMachine(input_test_json["machine"]["outlets"]["count_n"])
		for ingredient, quantity in input_test_json["machine"]["total_items_quantity"].items():
			self.CoffeeMachine.refill_ingredient(ingredient, quantity)
		self.beverages = []
		for beverage, ingredients in input_test_json["machine"]["beverages"].items():
			beverage_obj = Beverage(beverage)
			for ingredient, quantity in ingredients.items():
				beverage_obj.add_required_ingredient(ingredient, quantity)
			self.beverages.append(beverage_obj)
			self.CoffeeMachine.add_beverage(beverage_obj)

	def test_get_all_ingredients_required(self):
		for beverage in self.beverages:
			all_required_ingredients = beverage.get_all_ingredients_required()
			self.assertEqual(len(all_required_ingredients),len(input_test_json["machine"]["beverages"][beverage.name]), "FAILED")
			for ingredient, quantity in all_required_ingredients.items():
				self.assertTrue(ingredient in input_test_json["machine"]["beverages"][beverage.name], "FAILED")
				self.assertEqual(input_test_json["machine"]["beverages"][beverage.name][ingredient], quantity, "FAILED")

	def test_get_all_available_ingredients(self):
		available_ingredients = self.CoffeeMachine.get_all_available_ingredients()
		self.assertEqual(len(available_ingredients), len(input_test_json["machine"]["total_items_quantity"]))
		for ingredient, quantity in available_ingredients.items():
			self.assertTrue(ingredient in input_test_json["machine"]["total_items_quantity"], "FAILED")
			self.assertEqual(input_test_json["machine"]["total_items_quantity"][ingredient], quantity, "FAILED")

	def test_add_extra_beverage(self):
		extra_beverage = Beverage("cold_coffee")
		extra_beverage.add_required_ingredient("sugar_syrup", 50)
		with self.assertRaises(Exception):
			self.CoffeeMachine.add_beverage(extra_beverage)

	def test_dispense_unavailable_beverage(self):
		with self.assertRaises(Exception):
			self.CoffeeMachine.dispense("cold_coffee")

	def test_dispence_bevarages_in_parallel(self):
		beverage_names = [beverage.name for beverage in self.beverages]
		random.shuffle(beverage_names)
		self.CoffeeMachine.dispense_beverages(beverage_names)


