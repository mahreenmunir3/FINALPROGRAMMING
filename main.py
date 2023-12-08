import pickle
from datetime import datetime


# Define the Employee base class
class Employee:
    def __init__(self, id, name, age, dob, passport, department, jobTitle, basicSalary, managerId):
        self.id = id
        self.name = name
        self.age = age
        self.dob = dob
        self.passport = passport
        self.department = department
        self.jobTitle = jobTitle
        self.basicSalary = basicSalary
        self.managerId = managerId

    def calculateCommission(self):
        return 0  # Base class does not calculate commission

    def calculateLossDeduction(self):
        return 0  # Base class does not calculate loss deduction

    def __str__(self):
        return f"Employee ID: {self.id}, Name: {self.name}, Department: {self.department}, Job Title: {self.jobTitle}"


# Define the Salesperson class
class Salesperson(Employee):
    def __init__(self, *args, commissionRate):
        super().__init__(*args)
        self.commissionRate = commissionRate

    def calculateCommission(self):
        return self.basicSalary * self.commissionRate

    def __str__(self):
        return super().__str__() + f", Commission Rate: {self.commissionRate}"


# Define the Manager class
class Manager(Employee):
    def __init__(self, *args):
        super().__init__(*args)
        self.salespersons = []  # Managers will manage salespersons

    def calculateLossDeduction(self):
        return self.basicSalary * 0.02  # For example purposes

    def __str__(self):
        return super().__str__() + f", Managed Salespersons: {len(self.salespersons)}"


# Define the House class
class House:
    def __init__(self, id, name, rooms, bathrooms, builtArea, declaredPrice, type, status, sellingPrice, salespersonId):
        self.id = id
        self.name = name
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.builtArea = builtArea
        self.declaredPrice = declaredPrice
        self.type = type
        self.status = status
        self.sellingPrice = sellingPrice
        self.salespersonId = salespersonId

    def calculateProfit(self):
        return self.sellingPrice - self.declaredPrice

    def __str__(self):
        return f"House ID: {self.id}, Type: {self.type}, Status: {self.status}, Selling Price: {self.sellingPrice}"


# Define the Sales class
class Sales:
    def __init__(self, houseId, salespersonId, salesDate, sellingPrice):
        self.houseId = houseId
        self.salespersonId = salespersonId
        self.salesDate = salesDate
        self.sellingPrice = sellingPrice

    def recordSale(self):
        print(f"Sale recorded for House ID {self.houseId} by Salesperson ID {self.salespersonId} on {self.salesDate}")

    def __str__(self):
        return f"Sales for House ID: {self.houseId}, Salesperson ID: {self.salespersonId}, Date: {self.salesDate}, Selling Price: {self.sellingPrice}"


# Define test cases to showcase the program features
def run_test_cases():
    # Create an employee
    manager = Manager("M001", "Alice", 35, "1985-04-12", "P123456", "Sales", "Manager", 75000, None)

    # Create a salesperson
    salesperson = Salesperson("S001", "Bob", 29, "1991-07-19", "P654321", "Sales", "Salesperson", 50000, "M001",
                              commissionRate=0.065)

    # Assign the salesperson to the manager
    manager.salespersons.append(salesperson)

    # Create a house
    house = House("H001", "Seaside Villa", 5, 3, 3500, 1000000, "Villa", "Sold", 1200000, salesperson.id)

    # Create a sale
    sales_date = datetime.now().strftime("%Y-%m-%d")
    sale = Sales(house.id, salesperson.id, sales_date, house.sellingPrice)
    sale.recordSale()

    # Display details
    print(manager)
    print(salesperson)
    print(house)
    print(sale)

    # Calculate commissions and profits
    print(f"Salesperson Commission: {salesperson.calculateCommission()}")
    print(f"Manager Loss Deduction: {manager.calculateLossDeduction()}")
    print(f"House Profit: {house.calculateProfit()}")

    # Serialize the objects to binary files using pickle
    with open('manager.pkl', 'wb') as output:
        pickle.dump(manager, output, pickle.HIGHEST_PROTOCOL)

    with open('salesperson.pkl', 'wb') as output:
        pickle.dump(salesperson, output, pickle.HIGHEST_PROTOCOL)

    with open('house.pkl', 'wb') as output:
        pickle.dump(house, output, pickle.HIGHEST_PROTOCOL)

    with open('sale.pkl', 'wb') as output:
        pickle.dump(sale, output, pickle.HIGHEST_PROTOCOL)

# Run the test cases to showcase the program features
run_test_cases()

# Deserialize the objects to demonstrate loading from binary files
with open('manager.pkl', 'rb') as input:
    loaded_manager = pickle.load(input)
    print(f"Loaded {loaded_manager}")

with open('salesperson.pkl', 'rb') as input:
    loaded_salesperson = pickle.load(input)
    print(f"Loaded {loaded_salesperson}")

with open('house.pkl', 'rb') as input:
    loaded_house = pickle.load(input)
    print(f"Loaded {loaded_house}")

with open('sale.pkl', 'rb') as input:
    loaded_sale = pickle.load(input)
    print(f"Loaded {loaded_sale}")

import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
from datetime import datetime

# Assume these are loaded from files or initialized somehow
employees = {}
houses = {}
sales = {}

# GUI Functions
def add_employee():
    id = simpledialog.askstring("Input", "Enter employee ID:", parent=root)
    if id in employees:
        messagebox.showerror("Error", "Employee ID already exists.")
        return
    name = simpledialog.askstring("Input", "Enter employee name:", parent=root)
    age = simpledialog.askinteger("Input", "Enter employee age:", parent=root)
    dob = simpledialog.askstring("Input", "Enter employee date of birth:", parent=root)
    passport = simpledialog.askstring("Input", "Enter employee passport number:", parent=root)
    department = simpledialog.askstring("Input", "Enter employee department:", parent=root)
    jobTitle = simpledialog.askstring("Input", "Enter employee job title:", parent=root)
    basicSalary = simpledialog.askfloat("Input", "Enter employee basic salary:", parent=root)
    managerId = simpledialog.askstring("Input", "Enter manager ID (or leave blank if none):", parent=root)
    if jobTitle.lower() == 'manager':
        emp = Manager(id, name, age, dob, passport, department, jobTitle, basicSalary, managerId)
    else:
        emp = Salesperson(id, name, age, dob, passport, department, jobTitle, basicSalary, managerId, commissionRate=0.065)
    employees[id] = emp
    messagebox.showinfo("Success", "Employee added successfully.")

def delete_employee():
    id = simpledialog.askstring("Input", "Enter employee ID to delete:", parent=root)
    if id in employees:
        del employees[id]
        messagebox.showinfo("Success", "Employee deleted successfully.")
    else:
        messagebox.showerror("Error", "Employee ID not found.")

def display_employee():
    id = simpledialog.askstring("Input", "Enter employee ID to display:", parent=root)
    if id in employees:
        employee = employees[id]
        messagebox.showinfo("Employee Details", str(employee))
    else:
        messagebox.showerror("Error", "Employee ID not found.")

def add_sale():
    house_id = simpledialog.askstring("Input", "Enter house ID:", parent=root)
    salesperson_id = simpledialog.askstring("Input", "Enter salesperson ID:", parent=root)
    selling_price = simpledialog.askfloat("Input", "Enter selling price:", parent=root)
    sales_date = datetime.now().strftime("%Y-%m-%d")  # Automatically use the current date for the sale

    if salesperson_id not in employees:
        messagebox.showerror("Error", "Salesperson ID does not exist.")
        return

    if house_id not in houses:
        messagebox.showerror("Error", "House ID does not exist.")
        return

    new_sale = Sales(house_id, salesperson_id, sales_date, selling_price)
    if salesperson_id in sales:
        sales[salesperson_id].append(new_sale)
    else:
        sales[salesperson_id] = [new_sale]
    messagebox.showinfo("Success", "Sale added successfully.")

def delete_sale():
    salesperson_id = simpledialog.askstring("Input", "Enter salesperson ID of the sale to delete:", parent=root)
    if salesperson_id in sales:
        sales[salesperson_id].pop()  # Removes the last sale made by the salesperson
        messagebox.showinfo("Success", "Sale deleted successfully.")
    else:
        messagebox.showerror("Error", "No sales found for this salesperson.")

def modify_sale():
    salesperson_id = simpledialog.askstring("Input", "Enter salesperson ID of the sale to modify:", parent=root)
    if salesperson_id in sales and sales[salesperson_id]:
        new_selling_price = simpledialog.askfloat("Input", "Enter the new selling price:", parent=root)
        sales[salesperson_id][-1].sellingPrice = new_selling_price
        messagebox.showinfo("Success", "Sale modified successfully.")
    else:
        messagebox.showerror("Error", "No sales found for this salesperson.")

def display_sales():
    salesperson_id = simpledialog.askstring("Input", "Enter salesperson ID to display sales:", parent=root)
    if salesperson_id in sales:
        sales_info = "\n".join(str(sale) for sale in sales[salesperson_id])
        messagebox.showinfo("Sales Details", sales_info)
    else:
        messagebox.showerror("Error", "No sales found for this salesperson.")


# Initialize the main window
root = tk.Tk()
root.title("Real Estate Management System")

# Add buttons
tk.Button(root, text="Add Employee", command=add_employee).pack(fill=tk.X)
tk.Button(root, text="Delete Employee", command=delete_employee).pack(fill=tk.X)
tk.Button(root, text="Display Employee Details", command=display_employee).pack(fill=tk.X)
tk.Button(root, text="Add Sale", command=add_sale).pack(fill=tk.X)
tk.Button(root, text="Modify Sale", command=modify_sale).pack(fill=tk.X)
tk.Button(root, text="Display Sales Details", command=display_sales).pack(fill=tk.X)

# Run the main loop
root.mainloop()
