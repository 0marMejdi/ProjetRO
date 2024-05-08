import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox
import gurobipy as gp
from gurobipy import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knapsack Solver - Main Window")
        self.setGeometry(100, 100, 400, 150)
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Widgets
        self.n_label = QLabel("Enter the number of items (n):")
        self.n_edit = QLineEdit()
        input_layout.addWidget(self.n_label)
        input_layout.addWidget(self.n_edit)

        self.capacity_label = QLabel("Enter the capacity:")
        self.capacity_edit = QLineEdit()
        input_layout.addWidget(self.capacity_label)
        input_layout.addWidget(self.capacity_edit)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.openSecondWindow)
        button_layout.addWidget(self.next_button)

        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def openSecondWindow(self):
        n = int(self.n_edit.text())
        capacity = int(self.capacity_edit.text())  # Retrieve capacity value
        self.secondWindow = SecondWindow(n, capacity)  # Pass n and capacity to SecondWindow
        self.secondWindow.show()


class SecondWindow(QWidget):
    def __init__(self, n, capacity):
        super().__init__()
        self.setWindowTitle("Knapsack Solver - Second Window")
        self.setGeometry(100, 100, 400, 300)
        self.n = n
        self.capacity = capacity  # Store capacity attribute
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()

        # Widgets
        self.weight_labels = []
        self.value_labels = []
        self.weight_edits = []
        self.value_edits = []

        for i in range(self.n):
            item_layout = QHBoxLayout()

            weight_label = QLabel(f"Weight {i+1}:")
            self.weight_labels.append(weight_label)
            weight_edit = QLineEdit()
            self.weight_edits.append(weight_edit)
            item_layout.addWidget(weight_label)
            item_layout.addWidget(weight_edit)

            value_label = QLabel(f"Value {i+1}:")
            self.value_labels.append(value_label)
            value_edit = QLineEdit()
            self.value_edits.append(value_edit)
            item_layout.addWidget(value_label)
            item_layout.addWidget(value_edit)

            main_layout.addLayout(item_layout)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)

        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solveKnapsack)
        main_layout.addWidget(solve_button)

        self.setLayout(main_layout)

    def solveKnapsack(self):
        try:
            # Get weights and values from QLineEdit widgets
            self.weights = []
            self.values = []

            for weight_edit, value_edit in zip(self.weight_edits, self.value_edits):
                weight_text = weight_edit.text().strip()
                value_text = value_edit.text().strip()

                if weight_text and value_text:
                    weight = int(weight_text)
                    value = int(value_text)
                    self.weights.append(weight)
                    self.values.append(value)
                else:
                    raise ValueError("Empty or invalid input detected.")

            # Create a new model
            model = gp.Model("Knapsack")

            # Create variables
            x = model.addVars(self.n, vtype=GRB.BINARY, name="x")

            # Set objective
            model.setObjective(sum(self.values[i] * x[i] for i in range(self.n)), GRB.MAXIMIZE)

            # Add constraint
            model.addConstr(sum(self.weights[i] * x[i] for i in range(self.n)) <= self.capacity, "Capacity")

            # Solve the model
            model.optimize()

            # Display the result
            result = ""
            for i in range(self.n):
                if x[i].x > 0.5:
                    result += f"Item {i+1}: Weight={self.weights[i]}, Value={self.values[i]}\n"
            result += f"Total Value: {model.objVal}"
            self.result_text.setText(result)

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
