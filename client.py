import requests
import pandas as pd
import json


class Client:

    def get_receipt(self, groceries_file):
        # loading the shopping list
        f = open(groceries_file)
        data = json.load(f)
        f.close()

        # sending the request
        BASE = "http://127.0.0.1:5000/"
        response = requests.put(BASE, json=data)

        # printing the output
        if response.json() == {}:
            return "empty list"
        else:
            receipt = response.json()["receipt"]
            df = pd.DataFrame.from_dict(receipt)
            payment_line = {"id": " ", "name": " ", "size": " ", "price": " ", "qnt": " ",
                    "total": response.json()["total_sum"]}
            df = df.append(payment_line, ignore_index=True)
            return df


#c = Client()
#print(Client.get_receipt(c,'groceries1.json'))
#print(Client.get_receipt(c,'groceries2.json'))
