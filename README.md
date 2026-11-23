from collections import deque
from datetime import datetime

# In-memory data structures: dictionaries, queue, and list
customers = {}
orders = {}
laundry_queue = deque()
order_history = []
next_order_id = 1001


def line():
    print("-" * 60)


def add_customer():
    print("\n--- Add Customer ---")
    cid = input("Customer ID: ").strip()
    if not cid:
        print("Customer ID cannot be empty.")
        return
    if cid in customers:
        print("Customer already exists.")
        return

    name = input("Customer name: ").strip()
    phone = input("Phone number: ").strip()
    if not name or not phone:
        print("Name and phone number are required.")
        return

    customers[cid] = {"name": name, "phone": phone}
    print("Customer added successfully.")


def view_customers():
    print("\n--- Customers ---")
    if not customers:
        print("No customers found.")
        return
    line()
    print(f"{'ID':<12}{'Name':<25}{'Phone':<15}")
    line()
    for cid, data in customers.items():
        print(f"{cid:<12}{data['name']:<25}{data['phone']:<15}")
    line()


def create_order():
    global next_order_id
    print("\n--- Create Laundry Order ---")
    cid = input("Customer ID: ").strip()
    if cid not in customers:
        print("Customer not found. Add the customer first.")
        return

    print("Service types: 1. Wash & Fold  2. Dry Cleaning  3. Ironing")
    service_choice = input("Choose service (1-3): ").strip()
    services = {"1": ("Wash & Fold", 80), "2": ("Dry Cleaning", 150), "3": ("Ironing", 40)}
    if service_choice not in services:
        print("Invalid service choice.")
        return

    try:
        weight = float(input("Clothes weight (kg): ").strip())
        if weight <= 0:
            print("Weight must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number for weight.")
        return

    service, rate = services[service_choice]
    total = round(weight * rate, 2)
    oid = next_order_id
    next_order_id += 1
    order = {
        "order_id": oid,
        "customer_id": cid,
        "customer_name": customers[cid]["name"],
        "service": service,
        "weight": weight,
        "rate": rate,
        "total": total,
        "status": "Queued",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    orders[oid] = order
    laundry_queue.append(oid)
    order_history.append({"order_id": oid, "action": "Created", "time": order["created_at"]})
    print(f"Order created successfully! Order ID: {oid}")
    print(f"Estimated charge: Rs. {total:.2f}")


def view_orders():
    print("\n--- All Orders ---")
    if not orders:
        print("No orders found.")
        return
    line()
    for order in orders.values():
        print(
            f"Order #{order['order_id']} | {order['customer_name']} | "
            f"{order['service']} | {order['weight']:.2f} kg | "
            f"Rs. {order['total']:.2f} | Status: {order['status']}"
        )
    line()


def process_next_order():
    print("\n--- Process Next Order ---")
    while laundry_queue and orders[laundry_queue[0]]["status"] != "Queued":
        laundry_queue.popleft()
    if not laundry_queue:
        print("No queued orders to process.")
        return

    oid = laundry_queue.popleft()
    orders[oid]["status"] = "In Progress"
    order_history.append({
        "order_id": oid,
        "action": "Marked In Progress",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    print(f"Order #{oid} is now In Progress.")


def complete_order():
    print("\n--- Complete Order ---")
    try:
        oid = int(input("Order ID: ").strip())
    except ValueError:
        print("Enter a valid numeric order ID.")
        return

    if oid not in orders:
        print("Order not found.")
        return
    if orders[oid]["status"] == "Completed":
        print("This order is already completed.")
        return
    if orders[oid]["status"] == "Queued":
        print("Process this order first before completing it.")
        return

    orders[oid]["status"] = "Completed"
    order_history.append({
        "order_id": oid,
        "action": "Completed",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    print(f"Order #{oid} marked as Completed.")


def search_order():
    print("\n--- Search Order ---")
    try:
        oid = int(input("Order ID: ").strip())
    except ValueError:
        print("Enter a valid numeric order ID.")
        return
    order = orders.get(oid)
    if not order:
        print("Order not found.")
        return
    line()
    for key, value in order.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    line()


def show_history():
    print("\n--- Order Activity History ---")
    if not order_history:
        print("No activity recorded yet.")
        return
    for item in order_history:
        print(f"Order #{item['order_id']} | {item['action']} | {item['time']}")


def show_menu():
    print("\n" + "=" * 60)
    print("             LAUNDRY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Add customer")
    print("2. View customers")
    print("3. Create laundry order")
    print("4. View all orders")
    print("5. Process next queued order")
    print("6. Complete an order")
    print("7. Search order by ID")
    print("8. View order history")
    print("0. Exit")
    line()


def main():
    actions = {
        "1": add_customer,
        "2": view_customers,
        "3": create_order,
        "4": view_orders,
        "5": process_next_order,
        "6": complete_order,
        "7": search_order,
        "8": show_history,
    }
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Thank you for using Laundry Management System!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
