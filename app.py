from flask import Flask, redirect, request, jsonify, Response,render_template,url_for
from pymongo import MongoClient
import os
mongo_host = os.environ['MONGOHOST']
client = MongoClient(mongo_host,27017)
db = client.e_commerce
coll = db.store
coll2=db.incr
app = Flask(__name__)

p_data = {"pID":"","category":"","name":"","Price":0.0,"quantity":0}




@app.route('/',methods=['GET'])
def home():
    print('-*'*30,'\n','Entered Home route')

    return render_template('home.html')

@app.route('/prints',methods=['GET'])
def prints():
    print('-*'*30,'\n','Entered Printing route')


    li = coll.find()
    return render_template('print.html',list=li)


# -------------------------------------------For buying items from the shop---------------------------
@app.route('/buy',methods=['POST'])
def buy():

    print('-*'*30,'\n','Entered Buy route ')
    message = ''

    p_data={}
    #getting fields from form
    p_ID = int(request.form['pID'])
    quant = int(request.form['quantity'])
    #getting old entry (quantity,price) from db
    print("searching with pid ",p_ID)
    p_data = coll.find_one({'pID': int(p_ID)})
    if p_data == None:
        print("\t\t\tError: id not matching any records")
        message = 'Id you entered does not match any records'
        return render_template('buy.html',error="true",message=message)
    print('type of find',type(p_data))
    # for rec in p_data :
    #     print(rec)
    print(p_data.__doc__)


    old_quantity = int(p_data['quantity'])

    if old_quantity < quant :
        #can't purchase
        print("stocks not available")
        message="stocks not enough to fill requirement"
        return render_template('buy.html',error='true',message=message)
    elif old_quantity == quant :
        price = float(p_data['price'])
        amount = price*quant
        #purchase successsful but stock is now over, so delete item
        message = "success, but this item is now stocked out (for further purchases)"
        coll.remove({'pID':p_ID})
    else:
        price = float(p_data['price'])
        coll.update({'pID': p_ID},
        {
            '$set': {
                'quantity': old_quantity - quant
                
            }
        })
        message = 'Successfully placed your order'
        amount = price * quant


    return render_template('buy.html',error='false', message=message, amount=amount)


# -----------------------------------------For adding items to the Catalog--------------------------
@app.route('/add',methods=['POST'])
def add():
    print('-*'*30,'\n','Entered Add items route')
    p_data={}
    id_inc = coll2.find_one()
    id_inc = id_inc["value"]
    id_inc += 1
    coll2.update({},
    {
        '$set': {
            'value': id_inc
        }
    })
    p_data['pID'] = int(id_inc)
    p_data['name'] = request.form['name']
    p_data['category'] = request.form['category']
    p_data['price'] = float(request.form['price'])
    p_data['quantity'] = int(request.form['quantity'])
    coll.insert_one(p_data)
    return render_template('add.html')

if __name__ == "__main__":
    d2 = coll2.find_one()
    if d2==None:
        coll2.insert_one({"value":1})
    app.run('0.0.0.0','5005',debug=True)

