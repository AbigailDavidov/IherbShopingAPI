import unittest
import requests
import json

class ApiTest(unittest.TestCase):
     BASE = "http://127.0.0.1:5000/"

     # checks if all products uploaded from csv (DB)
     def test_1_get_all_products(self):
          response = requests.get(ApiTest.BASE, json={})
          self.assertEqual(response.status_code, 200)
          self.assertEqual(len(response.json()), 2148)

     # checks that we can handle an empty list and doesn't crash
     def test_2_empty_list(self):
         response = requests.put(ApiTest.BASE, json={})
         self.assertEqual(response.status_code, 200)
         self.assertDictEqual(response.json(), {})

    # if the product is sent without name we can't calculate it
     def test_3_list_prod_no_name(self):
         response = requests.put(ApiTest.BASE, json={"groceries":[{"quantity": "10"}]})
         self.assertEqual(response.status_code, 200)
         self.assertDictEqual(response.json(), {'total_sum': 0, 'receipt': []})

    # we can decide that if there isn't quantity it means to calculate 1 unit
     def test_4_list_prod_no_qnt(self):
         response = requests.put(ApiTest.BASE, json={
             "groceries": [{"name": "Now Foods, Real Food, Organic Triple Omega Seed Mix, 12 oz (340 g)"}]})
         self.assertEqual(response.status_code, 200)
         self.assertEqual(len( response.json()["receipt"]), 1)

    # groceries2.json contains products with no name, products with no quantity and valid products (with name and quantity)
     def test_5_mixed_list(self):
        # loading the shopping list
        f = open('groceries2.json')
        data = json.load(f)
        f.close()

        response = requests.put(ApiTest.BASE, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len( response.json()["receipt"]), 4)
        self.assertEqual(round(response.json()["total_sum"],2), 275.91)

    # groceries1.json contains a valid, long grocery list (with name and quantity)
     def test_6_all_valid_list(self):
         # loading the shopping list
         f = open('groceries1.json')
         data = json.load(f)
         f.close()

         response = requests.put(ApiTest.BASE, json=data)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(len(response.json()["receipt"]), 8)
         self.assertEqual(round(response.json()["total_sum"], 2), 435.57)

if __name__ == '__main__':
     unittest.main()

