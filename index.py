from flask import Flask, render_template, request, redirect, url_for




app = Flask(__name__)





menu = []
orders = []
order_id_counter = 1


@app.route("/")
def index():
    return render_template("index.html", menu=menu, orders=orders)

count=1
@app.route("/add_dish", methods=["POST"])
def add_dish():
    global count
    dish_name = request.form["dish_name"]
    price = float(request.form["price"])
    availability = "availability" in request.form

    dish = {
        "id": count,
        "name": dish_name,
        "price": price,
        "availability": availability
    }
    menu.append(dish)
    count+=1

    return redirect(url_for("index"))

@app.route("/remove_dish", methods=["POST"])
def remove_dish():
    dish_id = int(request.form["dish_id"])

    
    global menu
    menu = [dish for dish in menu if dish["id"] != dish_id]

    
    for order in orders:
        order["dish_ids"] = [dish_id for dish_id in order["dish_ids"] if dish_id != dish_id]

    return redirect(url_for("index"))


@app.route("/update_availability", methods=["POST"])
def update_availability():
    dish_id = int(request.form["dish_id"])
    availability = "availability" in request.form

   
    dish = next((dish for dish in menu if dish["id"] == dish_id), None)
    if dish:
        dish["availability"] = availability

    return redirect(url_for("index"))


@app.route("/place_order", methods=["POST"])
def place_order():
    customer_name = request.form["customer_name"]
    dish_ids = request.form.getlist("dish_id")

    
    for dish_id in dish_ids:
        dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
        if not dish or not dish["availability"]:
            return render_template("index.html", menu=menu, orders=orders, error_message="Invalid dish selection")

    
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1

    order = {
        "id": order_id,
        "customer_name": customer_name,
        "dish_ids": dish_ids,
        "status": "received"
    }
    orders.append(order)

    return redirect(url_for("index"))


@app.route("/update_status", methods=["POST"])
def update_status():
    order_id = int(request.form["order_id"])
    status = request.form["status"]

   
    order = next((order for order in orders if order["id"] == order_id), None)
    if order:
        order["status"] = status
        order = next((order for order in orders if order["id"] == order_id), None)
    

    return redirect(url_for("index"))


def calculate_total_price(dish_ids):
     # Calculate the total price of an order based on the dish IDs
     total_price = 0
     for dish_id in dish_ids:
         dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
         if dish:
             total_price += dish["price"]
             return total_price


app.jinja_env.globals.update(calculate_total_price=calculate_total_price)






if __name__ == "__main__":
    app.run()






























 