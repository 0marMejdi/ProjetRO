import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox, QInputDialog
import gurobipy as gp
from gurobipy import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knapsack Solver - Main Window")
        self.setGeometry(100, 100, 550, 300)
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        product_layout = QVBoxLayout() 
        constraint_layout = QVBoxLayout() 
        button_layout = QHBoxLayout()

        # Prompt for the number of products
        while True:
            num_products, ok_pressed = QInputDialog.getInt(self, "Number of Products", "Enter the number of products:")
            if ok_pressed and num_products > 0:
                self.num_products = num_products
                break
            elif not ok_pressed:
                sys.exit()
            else:
                QMessageBox.warning(self, "Warning", "Number of products must be greater than 0. Please enter a valid number.")

        # Labels for each column
        header_layout = QHBoxLayout()
        headers = ["Name", "Buying Price", "Selling Price", "Weight", "Volume", "Available"]
        for header in headers:
            header_label = QLabel(header)
            header_layout.addWidget(header_label)

        # Widgets for product fields
        self.product_fields = []
        product_layout.addLayout(header_layout) 
        for i in range(1, self.num_products + 1):  
            product_field_layout = QHBoxLayout()

            name_label = QLabel(f"Product {i}:")
            product_field_layout.addWidget(name_label)

            name_edit = QLineEdit(f"Product {i}")
            product_field_layout.addWidget(name_edit)

            buying_price_edit = QLineEdit()
            product_field_layout.addWidget(buying_price_edit)

            selling_price_edit = QLineEdit()
            product_field_layout.addWidget(selling_price_edit)

            weight_edit = QLineEdit()
            product_field_layout.addWidget(weight_edit)

            volume_edit = QLineEdit()
            product_field_layout.addWidget(volume_edit)

            available_edit = QLineEdit()  
            product_field_layout.addWidget(available_edit)

            self.product_fields.append((name_edit, buying_price_edit, selling_price_edit, weight_edit, volume_edit, available_edit))
            product_layout.addLayout(product_field_layout)

        # Widgets for truck constraints
        self.capacity_label = QLabel("Enter the maximum weight (W) supported by the truck:")
        self.capacity_edit = QLineEdit()
        constraint_layout.addWidget(self.capacity_label)
        constraint_layout.addWidget(self.capacity_edit)

        self.volume_label = QLabel("Enter the maximum volume (V) supported by the truck:")
        self.volume_edit = QLineEdit()
        constraint_layout.addWidget(self.volume_label)
        constraint_layout.addWidget(self.volume_edit)

        # Budget constraint
        self.budget_label = QLabel("Enter the budget:")
        self.budget_edit = QLineEdit()
        constraint_layout.addWidget(self.budget_label)
        constraint_layout.addWidget(self.budget_edit)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.solveKnapsack)
        button_layout.addWidget(self.next_button)

        # Add layouts to main layout
        main_layout.addLayout(product_layout)
        main_layout.addLayout(constraint_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def solveKnapsack(self):
        try:
            # Get weights, volumes, buying prices, and available number to buy from QLineEdit widgets
            self.buying_prices = []
            self.selling_prices = []
            self.weights = []
            self.volumes = []
            self.available = []

            products_to_buy = []  # List to store products to buy
            total_buying_prices = 0.0  # Total buying prices of selected products
            earnings = 0.0  # Total earnings from selected products
            budget = float(self.budget_edit.text())  # Initial budget

            for name_edit, buying_price_edit, selling_price_edit, weight_edit, volume_edit, available_edit in self.product_fields:
                buying_price = float(buying_price_edit.text())
                selling_price = float(selling_price_edit.text())
                weight = float(weight_edit.text())
                volume = float(volume_edit.text())
                available = int(available_edit.text()) 
                self.buying_prices.append(buying_price)
                self.selling_prices.append(selling_price)
                self.weights.append(weight)
                self.volumes.append(volume)
                self.available.append(available)

            W = float(self.capacity_edit.text())
            V = float(self.volume_edit.text())

            # Create a new model
            model = gp.Model("Knapsack")

            # Create variables
            x = model.addVars(len(self.buying_prices), vtype=GRB.INTEGER, name="x")  # Change to integer variables to allow buying multiple instances of each item

            # Set objective
            model.setObjective(sum((self.selling_prices[i] - self.buying_prices[i]) * x[i] for i in range(len(self.buying_prices))), GRB.MAXIMIZE)

            # Add budget constraint
            model.addConstr(sum(self.buying_prices[i] * x[i] for i in range(len(self.buying_prices))) <= budget, "Budget")

            # Add weight constraint
            model.addConstr(sum(self.weights[i] * x[i] for i in range(len(self.weights))) <= W, "Weight")

            # Add volume constraint
            model.addConstr(sum(self.volumes[i] * x[i] for i in range(len(self.volumes))) <= V, "Volume")

            # Add available number to buy constraint
            for i, available in enumerate(self.available):
                model.addConstr(x[i] <= available, f"Available_{i}")

            # Solve the model
            model.optimize()

            # Display the result
            result = "Products to buy:\n"
            for i in range(len(self.buying_prices)):
                if x[i].x > 0:
                    name = self.product_fields[i][0].text()
                    quantity = int(x[i].x)
                    products_to_buy.append((name, quantity))
                    total_buying_prices += quantity * self.buying_prices[i]
                    earnings += quantity * (self.selling_prices[i] - self.buying_prices[i])
                    result += f"{name}: Quantity={quantity}\n"

            remaining_budget = budget - total_buying_prices
            result += f"\nTotal Earnings: {earnings}\n"
            result += f"Remaining Budget: {remaining_budget}\n"

            QMessageBox.information(self, "Result", result)

        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Invalid input detected: {ve}")

        except gp.GurobiError as e:
            QMessageBox.critical(self, "Error", f"Gurobi error occurred: {str(e)}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
