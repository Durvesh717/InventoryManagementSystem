def load_inventory(file_name):
    try:
        with open(file_name, 'r') as file:
            products = {}
            for line in file:
                name, price, quantity, category, brand = line.strip().split(',')
                products[name] = {"price": float(price), "quantity": int(quantity), "category": category, "brand": brand}
            return products
    except FileNotFoundError:
        print("Inventory file not found. Starting with empty inventory.")
        return {}
    except ValueError:
        print("Error: Invalid inventory file format. Starting with empty inventory.")
        return {}

def save_inventory(file_name,products):
    with open(file_name, 'w') as file:
        for name, details in products.items():
            file.write(f"{name},{details['price']},{details['quantity']},{details['category']},{details['brand']}\n")

def add_product(products, name, price, quantity, category, brand):
    if name.strip() == "":
        print("Error: Product name cannot be empty.")
        return

    if name not in products:
        products[name] = {"price": price, "quantity": quantity, "category": category, "brand": brand}
        print(f"Product '{name}' added to inventory with category '{category}' and brand '{brand}'.")
    else:
        print("Error: Product already exists in inventory.")

def remove_product(products, name):
    if name in products:
        del products[name]
        print(f"Product '{name}' removed from inventory.")
    else:
        print("Error: Product not found in inventory.")

def update_quantity(products, name, quantity, price=None, add=True):
    if name in products:
        if add:
            products[name]["quantity"] += quantity
            if price is not None and price.strip() != "":
                if price.lower() == 'sameprice':
                    print(f"Added {quantity} to the quantity of '{name}' without changing the price.")
                else:
                    try:
                        price = float(price)
                        products[name]["price"] = price
                        print(f"Added {quantity} to the quantity of '{name}' and updated price to ₹{price}.")
                    except ValueError:
                        print("Error: Invalid price format. Price must be a number.")
            else:
                print(f"Added {quantity} to the quantity of '{name}'.")
        else:
            if products[name]["quantity"] >= quantity:
                products[name]["quantity"] -= quantity
                if price is not None and price.strip() != "":
                    if price.lower() == 'sameprice':
                        print(f"Subtracted {quantity} from the quantity of '{name}' without changing the price.")
                    else:
                        try:
                            price = float(price)
                            products[name]["price"] = price
                            print(f"Subtracted {quantity} from the quantity of '{name}' and updated price to ₹{price}.")
                        except ValueError:
                            print("Error: Invalid price format. Price must be a number.")
                else:
                    print(f"Subtracted {quantity} from the quantity of '{name}'.")
            else:
                print(f"Error: Insufficient quantity of '{name}' in stock. Cannot subtract {quantity}.")
    else:
        print("Error: Product not found in inventory.")

def display_inventory(products):
    if not products:
        print("Inventory is empty.")
    else:
        print("Current Inventory:")
        for name, details in sorted(products.items()):
            print(f"Name: {name}, Category: {details['category']}, Brand: {details['brand']}, Price: ₹{details['price']}, Quantity: {details['quantity']}")

def sort_inventory(products, sort_key):
    if not products:
        print("Inventory is empty.")
        return

    if sort_key == 'name':
        sorted_products = sorted(products.items())
    elif sort_key == 'price':
        sorted_products = sorted(products.items(), key=lambda x: x[1]['price'])
    elif sort_key == 'quantity':
        sorted_products = sorted(products.items(), key=lambda x: x[1]['quantity'])
    elif sort_key == 'category':
        sorted_products = sorted(products.items(), key=lambda x: x[1]['category'])
    elif sort_key == 'brand':
        sorted_products = sorted(products.items(), key=lambda x: x[1]['brand'])
    else:
        print("Error: Invalid sort key.")
        return

    print(f"Sorted Inventory by {sort_key.capitalize()}:")
    for name, details in sorted_products:
        print(f"Name: {name}, Category: {details['category']}, Brand: {details['brand']}, Price: ₹{details['price']}, Quantity: {details['quantity']}")

def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

def main():
    inventory_file = "inventory.txt"
    products = load_inventory(inventory_file)

    while True:
        print("\n1. Add Product")
        print("2. Remove Product")
        print("3. Update Quantity")
        print("4. Display Inventory")
        print("5. Sort Inventory")
        print("6. Save Inventory")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nAdding Product:")
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            brand = input("Enter product brand: ")
            price = get_positive_number("Enter product price: ₹")
            quantity = int(get_positive_number("Enter product quantity: "))
            add_product(products, name, price, quantity, category, brand)
        elif choice == '2':
            print("\nRemoving Product:")
            name = input("Enter product name to remove: ")
            remove_product(products, name)
        elif choice == '3':
            print("\nUpdating Quantity:")
            name = input("Enter product name to update quantity: ")
            action = input("Do you want to add or subtract quantity? (add/subtract): ").lower()
            if action == 'add':
                quantity = int(get_positive_number("Enter quantity to add: "))
                price = input("Enter new price or type 'sameprice' to keep the current price: ₹")
                update_quantity(products, name, quantity, price)
            elif action == 'subtract':
                quantity = int(get_positive_number("Enter quantity to subtract: "))
                price = input("Enter new price or type 'sameprice' to keep the current price: ₹")
                update_quantity(products, name, quantity, price, add=False)
            else:
                print("Invalid action. Please enter 'add' or 'subtract'.")
        elif choice == '4':
            print("\nDisplaying Inventory:")
            display_inventory(products)
        elif choice == '5':
            print("\nSorting Inventory:")
            sort_key = input("Enter sort key (name/price/quantity/category/brand): ").lower()
            sort_inventory(products, sort_key)
        elif choice == '6':
            print("\nSaving Inventory:")
            save_inventory(inventory_file, products)
            print("Inventory saved successfully.")
        elif choice == '7':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
