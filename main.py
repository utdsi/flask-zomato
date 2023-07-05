from flask import Flask,request,jsonify,render_template
import pickle

app = Flask(__name__)

menu={}
orders={}

def load_pickled_data():
    global menu, orders
    
    try:
        with open("menu.pickle","rb") as file:
         menu = pickle.load(file)  
        with open("orders.pickle","rb") as file:
            orders= pickle.load(file)  
    
    except FileNotFoundError:
        
        menu={}
        orders={}
            

def write_data():
    with open("menu.pickle","wb") as file:
         pickle.dump(menu,file)  
    with open("orders.pickle","wb") as file:
         pickle.dump(orders,file) 
         


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/add", methods=["POST"] )
def add_items():
    dish=request.json
    menu[dish["id"]] = dish
    write_data()
    return jsonify({"msg":"Dish added successfully"})

@app.route("/get")
def get_items():
    return menu

@app.route("/delete/<int:dish_id>",methods=["DELETE"])

def del_item(dish_id):
    
    if dish_id in menu:
        del menu[dish_id]
        write_data()
        return jsonify({"msg":"Dish deleted successfully"})
    return jsonify({"msg":"Dish not found"})
    
@app.route("/update/<int:dish_id>",methods=["PUT"])

def update_item(dish_id):
       
    if dish_id in menu:
        menu[dish_id] = request.json
        write_data()
        return jsonify({"msg":"Dish updated successfully"})
    return jsonify({"msg":"Dish not found"})

@app.route("/orders", methods=["POST"] )

def take_orders():
    
    order = request.json
    
    id = str(len(orders)+1)
    
    orders[id] = order
    write_data()
    return jsonify({"msg":"Ordered successfully"})
    
@app.route("/geto")
def get_order():
    return orders   

@app.route("/orders/<int:order_id>",methods=["PUT"]) 

def update_order_status(order_id):
    
    if order_id in orders:
        orders[order_id] = request.json
        write_data()
        return jsonify({"msg":"status updated successfully"})
    return jsonify({"msg":"order not found"})



if (__name__ == '__main__'):
    load_pickled_data()
    app.run(debug=True,port=8000)