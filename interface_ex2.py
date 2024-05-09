from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGridLayout, QFrame, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
import gurobipy as gp

from solution_ex2 import PL2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textbox_values = []
        self.additional_params_values = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("PL2: Planification des besoins en ressources")
        self.setFixedSize(1500, 1000)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Enonce
        enonce1 = QLabel(
            "Entrer les données pour avoir le planning optimal de production ainsi que la politique optimale de gestion des ouvriers."
        )
        enonce1.setFont(QFont("helvetica", 16))
        main_layout.addWidget(enonce1)

        # Months input
        months_layout = QHBoxLayout()
        label_months = QLabel("Nombre des mois :")
        months_layout.addWidget(label_months)

        self.entry_months = QLineEdit()
        months_layout.addWidget(self.entry_months)

        generate_button = QPushButton("Confirmer le nombre des mois")
        generate_button.clicked.connect(self.generate_input_boxes)
        months_layout.addWidget(generate_button)
        main_layout.addLayout(months_layout)

        # Additional parameters
        additional_params_frame = QFrame()
        additional_params_layout = QGridLayout(additional_params_frame)
        additional_params_layout.setHorizontalSpacing(20)  # Adjust horizontal spacing

        additional_params = [
            ("Cout heures supplementaires :", "heures_sup_cost"),
            ("Cout Chaussure fabriquéé:", "chaussures_fab_cost"),
            ("Cout licenciement d'un ouvrier :", "ouvriers_lic_cost"),
            ("Cout Recrutement d'un ouvrier :", "ouvriers_rec_cost"),
            ("Cout de Stockage d'un paire :", "stock_cost"),
            ("Salaire d'un ouvrier:", "ouvriers_dispo_cost"),
            ("Max Heures supplementaires:", "max_heures_supp"),
            ("Heures de travail par mois:", "heures_travail_mois"),
            ("Heures par chaussure:", "heures_par_chauss"),
            ("Ouvriers initials:", "ouvriers_initial"),
            ("Stock initial:", "stock_initial"),
        ]

        for row, (label_text, param_name) in enumerate(additional_params):
            label = QLabel(label_text)
            entry = QLineEdit()
            self.additional_params_values.append((param_name, entry))

            # Add label and entry to the layout with appropriate spacing
            additional_params_layout.addWidget(label, row, 0)
            additional_params_layout.addWidget(entry, row, 1)

        main_layout.addWidget(additional_params_frame)

        # Solve button
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.call_solver)
        main_layout.addWidget(solve_button)

        # Demand boxes frame
        self.demand_boxes_frame = QFrame()
        self.demand_boxes_layout = QGridLayout(self.demand_boxes_frame)
        main_layout.addWidget(self.demand_boxes_frame)

    def generate_input_boxes(self):
        try:
            # Clear existing demand boxes
            for label, textbox in self.textbox_values:
                label.deleteLater()
                textbox.deleteLater()

            self.textbox_values.clear()

            # Get number of months
            num_months = int(self.entry_months.text())

            rows = (num_months + 1) // 2  # Ensure even number of rows for odd months
            cols = 2

            for row in range(rows):
                for col in range(cols):
                    month_num = row * cols + col + 1
                    if month_num > num_months:
                        break

                    label_text = f"Demande pour le mois {month_num} :"
                    label = QLabel(label_text)
                    textbox = QLineEdit()

                    self.textbox_values.append((label, textbox))
                    self.demand_boxes_layout.addWidget(label, row, col * 2)
                    self.demand_boxes_layout.addWidget(textbox, row, col * 2 + 1)

        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number of months.")

    def call_solver(self):
        try:
            int_value_table = [float(textbox.text()) for label, textbox in self.textbox_values]

            additional_params_dict = {param_name: float(entry.text()) for param_name, entry in self.additional_params_values}

            # Call the solver with additional_params_dict as arguments
            solution_optimal_value, solution_variables = PL2(int(self.entry_months.text()), *additional_params_dict.values(), *int_value_table)

            if solution_optimal_value is not None:
                # Clear any existing result labels and text area
                self.clear_result_widgets()

                # Display optimal solution value
                solution_label = QLabel(f"Optimal solution: {solution_optimal_value}")
                solution_label.setFont(QFont("helvetica", 16))
                self.layout().addWidget(solution_label)

                # Display solution variables
                variables_label = QLabel("Solution variables:")
                variables_label.setFont(QFont("helvetica", 16))
                self.layout().addWidget(variables_label)

                for var_name, var_value in solution_variables.items():
                    var_info = f"{var_name}: {var_value}"
                    var_label = QLabel(var_info)
                    var_label.setFont(QFont("helvetica", 12))
                    self.layout().addWidget(var_label)

                # Add a QTextEdit widget for additional text
                text_area = QTextEdit()
                text_area.setReadOnly(True)  # Set text area to read-only
                text_area.setFont(QFont("helvetica", 12))
                text_area.setPlaceholderText("Additional information...")
                self.layout().addWidget(text_area)
                text_area.append(f"\nOptimal solution: {solution_optimal_value}\n")

                text_area.append("\nSolution variables:\n")
                for var_name, var_value in solution_variables.items():
                    text_area.append(f"{var_name}: {var_value}\n")

            else:
                QMessageBox.critical(self, "Error", "No optimal solution found or an error occurred during optimization.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_result_widgets(self):
        # Clear any existing result widgets from the layout
        for i in reversed(range(self.layout().count())):
            item = self.layout().itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()

""" 
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
 """