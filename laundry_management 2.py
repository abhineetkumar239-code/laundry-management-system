from datetime import datetime


# ==========================================
# CLASS 1: CUSTOMER
# ==========================================

class Customer:
    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone

    def display_details(self):
        print(f"Customer ID   : {self.customer_id}")
        print(f"Customer Name : {self.name}")
        print(f"Phone Number  : {self.phone}")


# ==========================================
# CLASS 2: LAUNDRY ORDER
# ==========================================

class LaundryOrder:
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.order_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.status = "Received"
        self.payment_status = "Unpaid"

    def calculate_bill(self):
        total = 0

        for item in self.items:
            total += item["quantity"] * item["price"]

        return total

    def update_status(self, new_status):
        self.status = new_status

    def make_payment(self):
        if self.payment_status == "Paid":
            print("Payment has already been completed.")
        else:
            self.payment_status = "Paid"
            print("Payment completed successfully!")

    def display_order(self):
        print("\n" + "=" * 55)
        print(f"ORDER ID       : {self.order_id}")
        print(f"CUSTOMER       : {self.customer.name}")
        print(f"ORDER DATE     : {self.order_date}")
        print(f"ORDER STATUS   : {self.status}")
        print(f"PAYMENT STATUS : {self.payment_status}")
        print("-" * 55)

        print(f"{'Item':<15}{'Service':<15}{'Qty':<7}{'Amount':>10}")
        print("-" * 55)

        for item in self.items:
            amount = item["quantity"] * item["price"]

            print(
                f"{item['name']:<15}"
                f"{item['service']:<15}"
                f"{item['quantity']:<7}"
                f"Rs. {amount:>6.2f}"
            )

        print("-" * 55)
        print(f"TOTAL BILL: Rs. {self.calculate_bill():.2f}")
        print("=" * 55)


# ==========================================
# CLASS 3: LAUNDRY MANAGEMENT SYSTEM
# ==========================================

class LaundryManagementSystem:

    def __init__(self):
        self.customers = {}
        self.orders = {}

        self.next_customer_id = 1001
        self.next_order_id = 5001

        # Prices are in Indian Rupees per item.
        # These are example prices and can be changed.

        self.prices = {
            "Shirt": {
                "Wash": 15,
                "Iron": 8,
                "Dry Cleaning": 60
            },
            "Trousers": {
                "Wash": 20,
                "Iron": 10,
                "Dry Cleaning": 80
            },
            "Bedsheet": {
                "Wash": 40,
                "Iron": 25,
                "Dry Cleaning": 120
            },
            "Blanket": {
                "Wash": 100,
                "Iron": 50,
                "Dry Cleaning": 250
            },
            "Jacket": {
                "Wash": 50,
                "Iron": 30,
                "Dry Cleaning": 150
            }
        }

        self.services = [
            "Wash",
            "Iron",
            "Dry Cleaning"
        ]

        self.status_options = [
            "Received",
            "Processing",
            "Ready",
            "Delivered"
        ]

    # --------------------------------------
    # CUSTOMER REGISTRATION
    # --------------------------------------

    def register_customer(self):
        print("\n--- CUSTOMER REGISTRATION ---")

        name = input("Enter customer name: ").strip()

        if not name:
            print("Customer name cannot be empty.")
            return

        phone = input("Enter phone number: ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print("Please enter a valid 10-digit phone number.")
            return

        customer = Customer(
            self.next_customer_id,
            name,
            phone
        )

        self.customers[self.next_customer_id] = customer

        print("\nCustomer registered successfully!")
        customer.display_details()

        self.next_customer_id += 1

    # --------------------------------------
    # DISPLAY CUSTOMERS
    # --------------------------------------

    def display_customers(self):
        print("\n--- REGISTERED CUSTOMERS ---")

        if not self.customers:
            print("No customers registered yet.")
            return

        for customer in self.customers.values():
            print("-" * 35)
            customer.display_details()

    # --------------------------------------
    # DISPLAY PRICE LIST
    # --------------------------------------

    def display_price_list(self):
        print("\n--- LAUNDRY PRICE LIST ---")

        print(f"{'Clothing Item':<18}", end="")

        for service in self.services:
            print(f"{service:<17}", end="")

        print()
        print("-" * 68)

        for item_name, service_prices in self.prices.items():
            print(f"{item_name:<18}", end="")

            for service in self.services:
                print(
                    f"Rs. {service_prices[service]:<13}",
                    end=""
                )

            print()

        print("\nPrices are per item and are in Indian Rupees.")

    # --------------------------------------
    # PLACE A LAUNDRY ORDER
    # --------------------------------------

    def place_order(self):
        print("\n--- PLACE LAUNDRY ORDER ---")

        if not self.customers:
            print("Please register a customer first.")
            return

        self.display_customers()

        customer_id = self.get_integer(
            "\nEnter customer ID: ",
            minimum=1001
        )

        customer = self.customers.get(customer_id)

        if customer is None:
            print("Customer not found.")
            return

        items = []

        while True:
            print("\nAvailable clothing items:")

            item_names = list(self.prices.keys())

            for index, item_name in enumerate(item_names, start=1):
                print(f"{index}. {item_name}")

            item_choice = self.get_integer(
                "Select clothing item: ",
                minimum=1,
                maximum=len(item_names)
            )

            item_name = item_names[item_choice - 1]

            print("\nAvailable services:")

            for index, service in enumerate(self.services, start=1):
                price = self.prices[item_name][service]

                print(
                    f"{index}. {service} - Rs. {price} per item"
                )

            service_choice = self.get_integer(
                "Select service: ",
                minimum=1,
                maximum=len(self.services)
            )

            service_name = self.services[service_choice - 1]

            quantity = self.get_integer(
                "Enter quantity: ",
                minimum=1
            )

            price = self.prices[item_name][service_name]

            items.append({
                "name": item_name,
                "service": service_name,
                "quantity": quantity,
                "price": price
            })

            print(f"\nAdded {quantity} {item_name}(s) successfully.")

            another = input(
                "Add another item or service? (y/n): "
            ).strip().lower()

            if another != "y":
                break

        if not items:
            print("No items added. Order cancelled.")
            return

        order = LaundryOrder(
            self.next_order_id,
            customer,
            items
        )

        self.orders[self.next_order_id] = order

        print("\nOrder placed successfully!")
        order.display_order()

        self.next_order_id += 1

    # --------------------------------------
    # SEARCH / TRACK ORDER
    # --------------------------------------

    def track_order(self):
        print("\n--- TRACK LAUNDRY ORDER ---")

        order_id = self.get_integer(
            "Enter order ID: ",
            minimum=5001
        )

        order = self.orders.get(order_id)

        if order is None:
            print("Order not found.")
            return

        order.display_order()

    # --------------------------------------
    # VIEW ALL ORDERS
    # --------------------------------------

    def display_all_orders(self):
        print("\n--- ALL LAUNDRY ORDERS ---")

        if not self.orders:
            print("No orders available.")
            return

        for order in self.orders.values():
            order.display_order()

    # --------------------------------------
    # UPDATE ORDER STATUS
    # --------------------------------------

    def update_order_status(self):
        print("\n--- UPDATE ORDER STATUS ---")

        order_id = self.get_integer(
            "Enter order ID: ",
            minimum=5001
        )

        order = self.orders.get(order_id)

        if order is None:
            print("Order not found.")
            return

        print(f"\nCurrent status: {order.status}")
        print("\nAvailable statuses:")

        for index, status in enumerate(
            self.status_options,
            start=1
        ):
            print(f"{index}. {status}")

        choice = self.get_integer(
            "Select new status: ",
            minimum=1,
            maximum=len(self.status_options)
        )

        new_status = self.status_options[choice - 1]

        # Prevent an order from moving backwards.
        current_index = self.status_options.index(order.status)
        new_index = self.status_options.index(new_status)

        if new_index < current_index:
            print("An order cannot move to an earlier status.")
            return

        if new_status == "Delivered" and order.payment_status != "Paid":
            print("Please complete payment before delivery.")
            return

        order.update_status(new_status)

        print(f"Order status updated to: {new_status}")

    # --------------------------------------
    # PROCESS PAYMENT
    # --------------------------------------

    def process_payment(self):
        print("\n--- PAYMENT MANAGEMENT ---")

        order_id = self.get_integer(
            "Enter order ID: ",
            minimum=5001
        )

        order = self.orders.get(order_id)

        if order is None:
            print("Order not found.")
            return

        print(f"Customer: {order.customer.name}")
        print(f"Total bill: Rs. {order.calculate_bill():.2f}")
        print(f"Payment status: {order.payment_status}")

        if order.payment_status == "Paid":
            print("This order has already been paid for.")
            return

        confirm = input(
            "Confirm payment? (y/n): "
        ).strip().lower()

        if confirm == "y":
            order.make_payment()
        else:
            print("Payment cancelled.")

    # --------------------------------------
    # CUSTOMER ORDER HISTORY
    # --------------------------------------

    def customer_order_history(self):
        print("\n--- CUSTOMER ORDER HISTORY ---")

        customer_id = self.get_integer(
            "Enter customer ID: ",
            minimum=1001
        )

        customer = self.customers.get(customer_id)

        if customer is None:
            print("Customer not found.")
            return

        print(f"\nOrder history for {customer.name}:")

        found = False

        for order in self.orders.values():
            if order.customer.customer_id == customer_id:
                order.display_order()
                found = True

        if not found:
            print("This customer has not placed any orders yet.")

    # --------------------------------------
    # SUMMARY REPORT
    # --------------------------------------

    def display_summary(self):
        print("\n--- LAUNDRY BUSINESS SUMMARY ---")

        total_orders = len(self.orders)
        paid_orders = 0
        unpaid_orders = 0
        delivered_orders = 0
        revenue = 0
        pending_amount = 0

        for order in self.orders.values():
            bill = order.calculate_bill()

            if order.payment_status == "Paid":
                paid_orders += 1
                revenue += bill
            else:
                unpaid_orders += 1
                pending_amount += bill

            if order.status == "Delivered":
                delivered_orders += 1

        print(f"Total customers       : {len(self.customers)}")
        print(f"Total orders          : {total_orders}")
        print(f"Paid orders           : {paid_orders}")
        print(f"Unpaid orders         : {unpaid_orders}")
        print(f"Delivered orders      : {delivered_orders}")
        print(f"Total revenue received: Rs. {revenue:.2f}")
        print(f"Pending payments      : Rs. {pending_amount:.2f}")

    # --------------------------------------
    # HELPER FUNCTION FOR INTEGER INPUT
    # --------------------------------------

    @staticmethod
    def get_integer(prompt, minimum=None, maximum=None):
        while True:
            try:
                value = int(input(prompt))

                if minimum is not None and value < minimum:
                    print(f"Enter a number greater than or equal to {minimum}.")
                    continue

                if maximum is not None and value > maximum:
                    print(f"Enter a number less than or equal to {maximum}.")
                    continue

                return value

            except ValueError:
                print("Invalid input. Please enter a whole number.")

    # --------------------------------------
    # MAIN MENU
    # --------------------------------------

    def run(self):
        while True:
            print("\n")
            print("=" * 45)
            print("       LAUNDRY MANAGEMENT SYSTEM")
            print("=" * 45)

            print("1.  Register Customer")
            print("2.  View All Customers")
            print("3.  View Laundry Price List")
            print("4.  Place Laundry Order")
            print("5.  Track Order")
            print("6.  View All Orders")
            print("7.  Update Order Status")
            print("8.  Process Payment")
            print("9.  View Customer Order History")
            print("10. View Business Summary")
            print("0.  Exit")

            print("=" * 45)

            choice = self.get_integer(
                "Enter your choice: ",
                minimum=0,
                maximum=10
            )

            if choice == 1:
                self.register_customer()

            elif choice == 2:
                self.display_customers()

            elif choice == 3:
                self.display_price_list()

            elif choice == 4:
                self.place_order()

            elif choice == 5:
                self.track_order()

            elif choice == 6:
                self.display_all_orders()

            elif choice == 7:
                self.update_order_status()

            elif choice == 8:
                self.process_payment()

            elif choice == 9:
                self.customer_order_history()

            elif choice == 10:
                self.display_summary()

            elif choice == 0:
                print("\nThank you for using the Laundry Management System!")
                print("Exiting program...")
                break


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":
    system = LaundryManagementSystem()
    system.run()
