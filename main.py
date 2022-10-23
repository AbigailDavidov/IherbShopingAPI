import csv;
from flask import Flask,request;
from flask_restful import Api, Resource;


app = Flask(__name__)
api = Api(app)

lst = [*csv.DictReader(open('Iherb categories.csv'))];
prod_dict = {}
for item in lst:
    prod_dict[item["product_name"]] = [item["product_id"],item["product_size"],item["product_price"]]


class ShopingAPI(Resource):

     def get(self):
        return lst

     def put(self):
        res = {"total_sum":0, "receipt":[]}
        data = request.get_json()
        if data == {}: return {}
        total_sum = 0
        for i in data["groceries"]:
            if "name" in i:
                res_temp = {}
                if i["name"] in prod_dict and prod_dict[i["name"]][2] != 'not availabe':
                    res_temp["id"] = prod_dict[i["name"]][0]
                    res_temp["name"] = i["name"]
                    res_temp["size"] = prod_dict[i["name"]][1]
                    res_temp["price"] = prod_dict[i["name"]][2]
                    if "quantity" in i:
                        sum = float(i["quantity"]) * float(prod_dict[i["name"]][2])
                        res_temp["qnt"] = (i["quantity"])
                        res_temp["total"] = sum
                        total_sum += sum
                    else:
                        res_temp["qnt"] = (1)
                        res_temp["total"] = float(prod_dict[i["name"]][2])
                        total_sum += float(prod_dict[i["name"]][2])
                res["receipt"].append(res_temp)
        res["total_sum"] = total_sum
        return res

api.add_resource(ShopingAPI,"/")


if __name__ == '__main__':
    app.run(debug=True)