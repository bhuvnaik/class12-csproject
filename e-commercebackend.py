
import mysql.connector
from typing import Tuple, List

# Define a type alias for database cursor.
CursorType = mysql.connector.cursor.CursorBase

# Function to create a database connection and cursor.
def connect_to_database() -> Tuple[mysql.connector.connection.MySQLConnection, CursorType]:
    """
    Establish a connection to the MySQL database and return a cursor.

    Returns:
        Tuple[mysql.connector.connection.MySQLConnection, CursorType]: A tuple containing the database connection
        and cursor.
    """
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Bhuvan123",
            database="enterprise"
        )
        db_cursor = db_connection.cursor()
        return db_connection, db_cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

# Function to create a new admin account.
def create_admin() -> None:
    """
    Create a new admin account and store it in the database.
    """
    try:
        admin_id = input("Enter new admin ID: ")
        admin_name = input("Enter new admin name: ")
        admin_password = input("Enter new admin password: ")

        connection, cursor = connect_to_database()
        cursor.execute("INSERT INTO admin VALUES (%s, %s, %s)", (admin_id, admin_name, admin_password))
        connection.commit()
        print("Admin account created.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to create a new customer account.
def create_customer() -> None:
    """
    Create a new customer account and store it in the database.
    """
    try:
        customer_name = input("Enter your name: ")
        customer_address = input("Enter your address: ")
        contact_number = input("Enter your Contact No: ")
        customer_password = input("Create your password: ")

        connection, cursor = connect_to_database()
        
        # Get the count of existing customers to determine the new customer's ID.
        cursor.execute("SELECT COUNT(ID) FROM customer")
        count = cursor.fetchone()[0]

        # Insert the new customer into the database.
        cursor.execute("INSERT INTO customer (ID, name, address, contact_num, password, balance) "
                       "VALUES (%s, %s, %s, %s, %s, 0.0)", (count + 1, customer_name, customer_address, 
                                                           contact_number, customer_password))
        connection.commit()
        
        print(f"Your ID is {count + 1}")
        print("Account created.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to create a new vendor account.
def create_vendor() -> None:
    """
    Create a new vendor account and store it in the database.
    """
    try:
        vendor_name = input("Enter your name: ")
        vendor_password = input("Create your password: ")

        connection, cursor = connect_to_database()
        
        # Get the count of existing vendors to determine the new vendor's ID.
        cursor.execute("SELECT COUNT(ID) FROM vendor")
        count = cursor.fetchone()[0]

        # Insert the new vendor into the database.
        cursor.execute("INSERT INTO vendor (ID, name, password, balance) "
                       "VALUES (%s, %s, %s, 0)", (count + 1, vendor_name, vendor_password))
        connection.commit()
        
        print(f"Your ID is {count + 1}")
        print("Account created.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display the main menu.
def menu() -> None:
    """
    Display the main menu and handle user choices.
    """
    while True:
        print("Hello! Welcome")
        try:
            choice = int(input("Press 1 for customer, 2 for vendor, 3 for admin, 4 for new customer, 5 for new vendor: "))
            if choice == 1:
                customer_menu()
            elif choice == 2:
                vendor_menu()
            elif choice == 3:
                admin_menu()
            elif choice == 4:
                create_customer()
            elif choice == 5:
                create_vendor()
            else:
                print("Error! Try again")
        except ValueError:
            print("Invalid choice. Please enter a valid option.")

# Function to display the customer menu.
def customer_menu() -> None:
    """
    Display the customer menu and handle customer operations.
    """
    print("Customer Menu")
    customer_id = input("Enter customer ID: ")
    customer_password = input("Enter password: ")

    connection, cursor = connect_to_database()
    
    try:
        cursor.execute("SELECT ID, password, balance FROM customer WHERE ID = %s AND password = %s",
                       (customer_id, customer_password))
        result = cursor.fetchone()

        if result:
            customer_balance = result[2]

            if customer_balance > 0:
                while True:
                    try:
                        choice = int(input("1. Review orders 2. Place orders 3. Review balance 4. Exit: "))
                        
                        if choice == 1:
                            display_orders_customer(customer_id)
                        elif choice == 2:
                            place_order(customer_id)
                        elif choice == 3:
                            print(f"Your current balance is {customer_balance}")
                        elif choice == 4:
                            break
                        else:
                            print("Invalid choice. Please enter a valid option.")
                    except ValueError:
                        print("Invalid choice. Please enter a valid option.")

                print("Exiting customer menu.")
            else:
                print("Insufficient balance")
        else:
            print("Authorization failed")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display the vendor menu.
def vendor_menu() -> None:
    """
    Display the vendor menu and handle vendor operations.
    """
    print("Vendor Menu")
    vendor_id = input("Enter vendor ID: ")
    vendor_password = input("Enter password: ")

    connection, cursor = connect_to_database()

    try:
        cursor.execute("SELECT ID, password FROM vendor WHERE ID = %s AND password = %s",
                       (vendor_id, vendor_password))
        result = cursor.fetchone()

        if result:
            while True:
                try:
                    choice = int(input("1. Deliver order 2. Add product 3. Display orders "
                                       "4. Review Balance 5. Delete product 6. Display products 7. Exit: "))

                    if choice == 1:
                        deliver_order(vendor_id)
                    elif choice == 2:
                        add_product(vendor_id)
                    elif choice == 3:
                        display_orders_vendor(vendor_id)
                    elif choice == 4:
                        cursor.execute("SELECT balance FROM vendor WHERE ID = %s", (vendor_id,))
                        vendor_balance = cursor.fetchone()[0]
                        print(f"Your current balance is {vendor_balance}")
                    elif choice == 5:
                        delete_product(vendor_id)
                    elif choice == 6:
                        display_products(vendor_id)
                    elif choice == 7:
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
                except ValueError:
                    print("Invalid choice. Please enter a valid option.")

            print("Exiting vendor menu.")
        else:
            print("Authorization failed")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display the admin menu.
def admin_menu() -> None:
    """
    Display the admin menu and handle admin operations.
    """
    print("Admin Menu")
    admin_id = input("Enter admin ID: ")
    admin_password = input("Enter admin password: ")

    connection, cursor = connect_to_database()

    try:
        cursor.execute("SELECT ID, password FROM admin WHERE ID = %s AND password = %s",
                       (admin_id, admin_password))
        result = cursor.fetchone()

        if result:
            while True:
                try:
                    choice = int(input("1. Add balance 2. Add admin 3. Extract balance 4. Exit: "))

                    if choice == 1:
                        add_balance()
                    elif choice == 2:
                        create_admin()
                    elif choice == 3:
                        extract_balance()
                    elif choice == 4:
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
                except ValueError:
                    print("Invalid choice. Please enter a valid option.")

            print("Exiting admin menu.")
        else:
            print("Authorization failed")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to place an order.
def place_order(customer_id: str) -> None:
    """
    Place an order for products and update balances accordingly.

    Args:
        customer_id (str): The ID of the customer placing the order.
    """
    try:
        product_id = input("Please enter the product ID: ")
        quantity = input("Enter the quantity: ")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT order_ID FROM orders ORDER BY order_ID")
        order_ids = cursor.fetchall()
        order_id = find_min_gap(order_ids)

        cursor.execute("SELECT price, vend_ID, delay FROM product WHERE ID = %s", (product_id,))
        product_info = cursor.fetchone()

        cursor.execute("UPDATE customer SET balance = balance - %s WHERE ID = %s",
                       (product_info[0] * int(quantity), customer_id))

        cursor.execute("UPDATE vendor SET balance = balance + %s WHERE ID = %s",
                       (product_info[0] * int(quantity), product_info[1]))

        cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, CURDATE() + INTERVAL %s DAY)",
                       (order_id, customer_id, product_id, quantity, product_info[1], product_info[2]))

        connection.commit()
        print("Order placed.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to mark an order as delivered by a vendor.
def deliver_order(vendor_id: str) -> None:
    """
    Mark an order as delivered by a vendor.

    Args:
        vendor_id (str): The ID of the vendor marking the order as delivered.
    """
    try:
        order_id = input("Enter Order ID: ")
        customer_password = input("Enter customer password: ")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT * FROM customer INNER JOIN orders ON orders.cust_ID = customer.ID "
                       "WHERE customer.password = %s AND orders.order_ID = %s AND orders.vend_ID = %s",
                       (customer_password, order_id, vendor_id))

        customer_orders = cursor.fetchall()

        if customer_orders:
            cursor.execute("DELETE FROM orders WHERE order_ID = %s AND vend_ID = %s", (order_id, vendor_id))
            connection.commit()
            print("Order delivered.")
        else:
            print("Error. Please try again.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to find the minimum gap in a sequence of numbers.
def find_min_gap(numbers: List[Tuple[int]]) -> int:
    """
    Find the minimum gap in a sequence of numbers.

    Args:
        numbers (List[Tuple[int]]): A list of tuples containing numbers.

    Returns:
        int: The minimum gap.
    """
    prev = 1
    for number in numbers:
        if prev == number[0]:
            prev += 1
        else:
            break
    return prev

# Function to add a new product by a vendor.
def add_product(vendor_id: str) -> None:
    """
    Add a new product to the database by a vendor.

    Args:
        vendor_id (str): The ID of the vendor adding the product.
    """
    try:
        product_name = input("Enter the product's name: ")
        product_price = input("Enter the price: ")
        delivery_time = input("Enter the delivery time in days: ")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT ID FROM product ORDER BY ID")
        product_ids = cursor.fetchall()
        product_id = find_min_gap(product_ids)

        cursor.execute("INSERT INTO product VALUES (%s, %s, %s, %s, %s)",
                       (product_id, product_name, product_price, vendor_id, delivery_time))

        connection.commit()
        print("Product added.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to delete a product by a vendor.
def delete_product(vendor_id: str) -> None:
    """
    Delete a product by a vendor.

    Args:
        vendor_id (str): The ID of the vendor deleting the product.
    """
    try:
        product_id = input("Enter product ID: ")

        connection, cursor = connect_to_database()

        cursor.execute("DELETE FROM product WHERE ID = %s AND vend_ID = %s", (product_id, vendor_id))
        print("Successful update.")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to add balance to a customer's account.
def add_balance() -> None:
    """
    Add balance to a customer's account.
    """
    try:
        customer_id = input("Enter customer ID: ")
        balance_increment = input("Enter balance increment: ")

        connection, cursor = connect_to_database()

        cursor.execute("UPDATE customer SET balance = balance + %s WHERE ID = %s", (balance_increment, customer_id))
        connection.commit()

        cursor.execute("SELECT COUNT(ID) FROM customer WHERE ID = %s", (customer_id,))
        result = cursor.fetchone()

        if result[0] != 0:
            print("Successful update.")
        else:
            print("Record not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to extract balance from a vendor's account by an admin.
def extract_balance() -> None:
    """
    Extract balance from a vendor's account by an admin.
    """
    try:
        vendor_id = input("Enter vendor ID: ")
        balance_extraction = input("Enter balance extraction: ")

        connection, cursor = connect_to_database()

        cursor.execute("UPDATE vendor SET balance = balance - %s WHERE ID = %s",
                       (balance_extraction, vendor_id))
        connection.commit()

        cursor.execute("SELECT COUNT(ID) FROM vendor WHERE ID = %s", (vendor_id,))
        result = cursor.fetchone()

        if result[0] != 0:
            print("Successful update.")
        else:
            print("Record not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display orders for a vendor.
def display_orders_vendor(vendor_id: str) -> None:
    """
    Display orders for a vendor.

    Args:
        vendor_id (str): The ID of the vendor.
    """
    try:
        print("Your orders are:")
        print("Order_ID\tCust_ID\tProduct_ID\tQuantity\tAddress\tContact_num")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT orders.Order_ID, orders.cust_ID, orders.product_ID, "
                       "orders.quantity, customer.address, customer.contact_num "
                       "FROM orders INNER JOIN customer ON orders.cust_ID = customer.ID "
                       "WHERE orders.vend_ID = %s ORDER BY orders.delivery, orders.order_ID", (vendor_id,))
        orders = cursor.fetchall()

        for order in orders:
            print("\t".join(map(str, order)))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display orders for a customer.
def display_orders_customer(customer_id: str) -> None:
    """
    Display orders for a customer.

    Args:
        customer_id (str): The ID of the customer.
    """
    try:
        print("Your orders are:")
        print("Order_ID\tVendor\tProduct ID\tQuantity\tPrice per unit\tDelivery Date")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT orders.Order_ID, orders.vend_ID, orders.product_ID, "
                       "orders.quantity, product.price, orders.delivery "
                       "FROM ((orders INNER JOIN customer ON orders.cust_ID = customer.ID) "
                       "INNER JOIN product ON product.ID = orders.product_ID) "
                       "WHERE customer.ID = %s ORDER BY orders.delivery, orders.order_ID", (customer_id,))
        orders = cursor.fetchall()

        for order in orders:
            print("\t".join(map(str, order)))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to display products for a vendor.
def display_products(vendor_id: str) -> None:
    """
    Display products for a vendor.

    Args:
        vendor_id (str): The ID of the vendor.
    """
    try:
        print("Your products are:")
        print("ProductID\tName\t\tPrice\t\tDelivery Time")

        connection, cursor = connect_to_database()

        cursor.execute("SELECT ID, name, price, delay FROM product WHERE vend_ID = %s", (vendor_id,))
        products = cursor.fetchall()

        for product in products:
            print("\t".join(map(str, product)))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to search for products based on a keyword.
def search() -> bool:
    """
    Search for products based on a keyword.

    Returns:
        bool: True if the search is successful, False otherwise.
    """
    try:
        keyword = input("Please enter the keyword to search for: ")
        search_results_count = int(input("Include how many search results? "))

        connection, cursor = connect_to_database()

        cursor.execute("SELECT ID, name, price FROM product")
        product_list = cursor.fetchall()
        search_results = []

        for product in product_list:
            levenshtein_distance = calculate_levenshtein_distance(product[1], keyword)
            search_results.append((levenshtein_distance, product[0], product[1], product[2]))

        search_results = sorted(search_results, key=lambda x: x[0])
        search_results_count = min(len(search_results), search_results_count)

        if search_results_count > 0:
            print("Product name\tProduct ID\tPrice")

            for i in range(search_results_count):
                result = search_results[i]
                print(f"{result[2]}\t{result[1]}\t{result[3]}")
            
            return True
        else:
            print("No matching products found.")
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

# Function to calculate Levenshtein distance between two strings.
def calculate_levenshtein_distance(s: str, t: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.

    Args:
        s (str): The first string.
        t (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
    """
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    res = min([
        calculate_levenshtein_distance(s[:-1], t) + 1,
        calculate_levenshtein_distance(s, t[:-1]) + 1,
        calculate_levenshtein_distance(s[:-1], t[:-1]) + cost
    ])
    return res

# Function to compare elements for sorting based on Levenshtein distance.
def compare(x: Tuple[int, int, str, float]) -> int:
    """
    Compare elements for sorting based on Levenshtein distance.

    Args:
        x (Tuple[int, int, str, float]): A tuple containing Levenshtein distance, product ID, product name, and price.

    Returns:
        int: The Levenshtein distance.
    """
    return x[0]

# Main function to display the menu and handle user interactions.
def main() -> None:
    """
    Main function to display the menu and handle user interactions.
    """
    while True:
        menu()
        exit_choice = input("Exit marketplace? (y/n): ")
        if exit_choice.lower() == 'y':
            break

if __name__ == "__main__":
    main()
