import mysql.connector

class Inventory:
    def __init__(self, product_id, name, category, quantity, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Inventory(ID: {self.product_id}, {self.name}, {self.category}, {self.quantity}, ₹{self.price})"

class InventoryManager:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, category, quantity, price):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO Products (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
            (name, category, quantity, price)
        )
        self.db.commit()
        print(f"Product '{name}' added successfully.")

    def view_products(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Products")
        rows = cursor.fetchall()
        if not rows:
            print("No products found.")
        else:
            print("Product List:")
            for row in rows:
                product = Inventory(*row)
                print(product)

    def update_product(self, product_id, name, category, quantity, price):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE Products SET name=%s, category=%s, quantity=%s, price=%s WHERE id=%s",
            (name, category, quantity, price, product_id)
        )
        self.db.commit()
        print(f"Product ID '{product_id}' updated successfully.")

    def delete_product(self, product_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Products WHERE id=%s", (product_id,))
        self.db.commit()
        print(f"Product ID '{product_id}' deleted successfully.")

class UserManager:
    def __init__(self, db):
        self.db = db

    def register(self, username, password):
        cursor = self.db.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
            self.db.commit()
            print("Registration successful.")
        except mysql.connector.IntegrityError:
            print("Username already exists.")

    def login(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM Users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            print(f"User '{username}' logged in successfully.")
            return True
        else:
            print("Invalid username or password.")
            return False

# Main logic
def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Puppy@2005",
        database="InventoryDB"
    )

    inventory_manager = InventoryManager(db)
    user_manager = UserManager(db)

    print("1. Register\n2. Login")
    option = input("Select an option: ")

    if option == '1':
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        user_manager.register(username, password)

    elif option == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        if user_manager.login(username, password):
            while True:
                print("\n1. Add Product\n2. View Products\n3. Update Product\n4. Delete Product\n5. Exit")
                choice = input("Choose an option: ")

                if choice == '1':
                    name = input("Enter product name: ")
                    category = input("Enter category: ")
                    quantity = int(input("Enter quantity: "))
                    price = float(input("Enter price (₹): "))
                    inventory_manager.add_product(name, category, quantity, price)

                elif choice == '2':
                    inventory_manager.view_products()

                elif choice == '3':
                    product_id = int(input("Enter product ID to update: "))
                    name = input("Enter new name: ")
                    category = input("Enter new category: ")
                    quantity = int(input("Enter new quantity: "))
                    price = float(input("Enter new price: "))
                    inventory_manager.update_product(product_id, name, category, quantity, price)

                elif choice == '4':
                    product_id = int(input("Enter product ID to delete: "))
                    inventory_manager.delete_product(product_id)

                elif choice == '5':
                    print("Exiting...")
                    break

                else:
                    print("Invalid option.")

    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
