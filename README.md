# class12-csproject
**PROJECT TITLE:**

Inventory Management system + order placing mechanism for a complete Online Market Management System

**PROJECT SUMMARY:**

This project explores the back-end of a rudimentary e-commerce marketplace. It aims to demonstrate the functionality that might be expected from such a platform. It is written in Python and implements a MySQL connection for managing database operations.This Online Marketplace Management System is a Python-based command-line application that provides a platform for customers, vendors, and administrators to interact in a simulated online marketplace environment. The system is built using the MySQL database to store and manage user data, product information, and order records.


Key Features:


1. User Roles:

 		Admin: Manages the overall system, can add balance to customer accounts, add new administrators, and extract balance from vendor accounts.
 		Customer: Can review orders, place orders, review account balance, and search for products.
 		Vendor: Can deliver orders, add products, display orders, review account balance, delete products, and display their product catalog.
2. User Authentication:

 		Users must provide valid IDs and passwords to access their respective accounts.
 		Passwords are securely stored and authenticated against the database.
3. Account Creation:

		New customers and vendors can create accounts with their personal information.
 		Customers receive a unique customer ID upon registration.
4. Orders Management:

 		Customers can place orders for products, specifying quantity.
 		Vendors can deliver orders, and the system updates balances accordingly.
 		Orders include delivery dates, ensuring timely deliveries.
5. Product Management:

 		Vendors can add new products with details like name, price, and delivery time.
 		Vendors can also delete products from their catalog.
6. Balance Management:

 		Admins can add balance to customer accounts and extract balance from vendor accounts.
7. Product Search:

 		Customers can search for products based on keywords and receive search results.
8. Error Handling:

 		The system provides error handling to ensure data consistency and integrity in the database.
9. Interactive Menu:

 		Users are presented with a user-friendly menu to navigate through the system.
10. MySQL Database:

 		The system uses MySQL as its backend database to store user information, orders, products, and more.
11. Usage:

 		Users can interact with the system through a command-line interface by selecting their user type and providing login credentials.
12. Installation:

 		Clone the repository and ensure you have Python and MySQL installed.
 		Modify the database configuration in the code to match your MySQL setup.
13. Contributions:

 		Contributions to this project are welcome. You can fork the repository and submit pull requests for improvements or bug fixes.
14. Future Enhancements:

 		Implement a web-based interface for a more user-friendly experience.
 		Add more advanced features like order tracking and payment processing.
 		Enhance security measures, such as encryption for user data.

15. Acknowledgments:

 		The project utilizes the MySQL Connector/Python library for database connectivity.
 		This Online Marketplace Management System serves as a foundation for building more advanced e-commerce platforms and provides an excellent starting point for learning about 			database driven applications in Python.
