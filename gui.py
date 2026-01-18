import sys
import math
import csv
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QProgressBar, QMessageBox,
    QLabel, QLineEdit, QDialog, QTextEdit, QStatusBar
)
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtCore import Qt

from logic import (
    load_requirements_from_csv,
    load_requirements_from_excel,
    optimize_cutting,
    total_waste
)

# =====================================================
# Visualization
# =====================================================

BAR_COLORS = [
    QColor("#4C84C3"),
    QColor("#6FB1E5"),
    QColor("#7BC8A4"),
    QColor("#F2C97D"),
    QColor("#F29F8D"),
    QColor("#B39DDB"),
]


class BarVisualization(QWidget):
    def __init__(self, cuts, bar_length):
        super().__init__()
        self.cuts = cuts
        self.bar_length = bar_length
        self.setMinimumHeight(26)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height() - 6
        x = 0
        scale = width / self.bar_length if self.bar_length else 1

        for i, cut in enumerate(self.cuts):
            w = int(cut * scale)
            painter.setBrush(BAR_COLORS[i % len(BAR_COLORS)])
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x, 3, w, height, 4, 4)
            x += w


# =====================================================
# Manual Input Dialog
# =====================================================

class ManualInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual Cut Entry")
        self.resize(420, 300)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            "One per line:\n"
            "length, quantity (quantity optional)\n\n"
            "Example:\n1200, 3\n800\n450, 2"
        ))

        self.text = QTextEdit()
        layout.addWidget(self.text)

        buttons = QHBoxLayout()
        ok = QPushButton("Apply")
        cancel = QPushButton("Cancel")
        buttons.addStretch()
        buttons.addWidget(ok)
        buttons.addWidget(cancel)
        layout.addLayout(buttons)

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    def get_data(self):
        req = []
        for line in self.text.toPlainText().splitlines():
            if not line.strip():
                continue
            try:
                parts = [p.strip() for p in line.split(",")]
                length = math.ceil(float(parts[0]))
                qty = int(parts[1]) if len(parts) > 1 else 1
                if length > 0 and qty > 0:
                    req.extend([length] * qty)
            except:
                continue
        return req


# =====================================================
# Main GUI
# =====================================================

class CutOptimizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bar Cut Optimizer")
        self.resize(1300, 720)

        self.bar_length = 6000
        self.cut_requirements = []
        self.schedule = []

        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("BAR CUT OPTIMIZER")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        controls = QHBoxLayout()

        self.bar_input = QLineEdit()
        self.bar_input.setFixedWidth(120)
        self.bar_input.setPlaceholderText("6000")

        controls.addWidget(QLabel("Standard Bar Length"))
        controls.addWidget(self.bar_input)

        self.btn_csv = QPushButton("Import CSV")
        self.btn_xlsx = QPushButton("Import Excel")
        self.btn_manual = QPushButton("Manual Input")
        self.btn_opt = QPushButton("Optimize")
        self.btn_exp_csv = QPushButton("Export CSV")
        self.btn_exp_xlsx = QPushButton("Export Excel")
        self.btn_clear = QPushButton("Clear")

        for b in (
            self.btn_csv, self.btn_xlsx, self.btn_manual,
            self.btn_opt, self.btn_exp_csv,
            self.btn_exp_xlsx, self.btn_clear
        ):
            controls.addWidget(b)

        layout.addLayout(controls)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Bar #", "Cuts", "Waste", "Visualization"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # signals
        self.btn_csv.clicked.connect(self.import_csv)
        self.btn_xlsx.clicked.connect(self.import_excel)
        self.btn_manual.clicked.connect(self.manual_input)
        self.btn_opt.clicked.connect(self.optimize)
        self.btn_exp_csv.clicked.connect(self.export_csv)
        self.btn_exp_xlsx.clicked.connect(self.export_excel)
        self.btn_clear.clicked.connect(self.clear_all)

    def _apply_theme(self):
        self.setStyleSheet("""
        QWidget { background:#f4f6f8; color:#2e3440; }
        QPushButton { background:#e6ecf3; border:1px solid #c9d3df; padding:6px; }
        QPushButton:hover { background:#dbe7f3; }
        QLineEdit { background:white; border:1px solid #c9d3df; padding:4px; }
        QHeaderView::section { background:#e6ecf3; border:1px solid #c9d3df; }
        QProgressBar::chunk { background:#3CB371; }
        """)

    # -------------------------------------------------

    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.cut_requirements = load_requirements_from_csv(path)
            QMessageBox.information(self, "CSV Loaded",
                                    f"{len(self.cut_requirements)} cuts loaded.")
            self.status.showMessage("CSV loaded successfully", 4000)
        except Exception as e:
            QMessageBox.critical(self, "Load Failed", str(e))

    def import_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Excel", "", "Excel Files (*.xlsx)")
        if not path:
            return
        try:
            self.cut_requirements = load_requirements_from_excel(path)
            QMessageBox.information(self, "Excel Loaded",
                                    f"{len(self.cut_requirements)} cuts loaded.")
            self.status.showMessage("Excel loaded successfully", 4000)
        except Exception as e:
            QMessageBox.critical(self, "Load Failed", str(e))

    def manual_input(self):
        dlg = ManualInputDialog()
        if dlg.exec():
            data = dlg.get_data()
            if not data:
                QMessageBox.warning(self, "No Data", "No valid entries found.")
                return
            self.cut_requirements = data
            QMessageBox.information(self, "Manual Input",
                                    f"{len(data)} cuts loaded.")

    def optimize(self):
        if not self.cut_requirements:
            QMessageBox.warning(self, "No Data", "Load cut requirements first.")
            return

        if self.bar_input.text():
            try:
                self.bar_length = int(self.bar_input.text())
            except:
                QMessageBox.warning(self, "Invalid Input", "Bar length must be numeric.")
                return

        self.progress.setValue(0)
        self.schedule = optimize_cutting(
            self.cut_requirements,
            self.bar_length,
            self.progress.setValue
        )

        self.populate_table()

        waste = total_waste(self.schedule, self.bar_length)
        used = sum(sum(b) for b in self.schedule)
        yield_pct = 100 * used / (used + waste) if used else 0

        QMessageBox.information(
            self, "Optimization Complete",
            f"Bars used: {len(self.schedule)}\n"
            f"Total waste: {waste}\n"
            f"Yield: {yield_pct:.1f}%"
        )

        self.status.showMessage("Optimization complete", 5000)

    def populate_table(self):
        self.table.setRowCount(len(self.schedule))
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 90)

        for r, bar in enumerate(self.schedule):
            waste = self.bar_length - sum(bar)

            self.table.setRowHeight(r, 42)
            self.table.setItem(r, 0, QTableWidgetItem(str(r + 1)))
            self.table.setItem(r, 1, QTableWidgetItem(", ".join(map(str, bar))))

            w_item = QTableWidgetItem(str(waste))
            w_item.setForeground(QColor("#2e8b57") if waste == 0 else QColor("#c0392b"))
            self.table.setItem(r, 2, w_item)

            self.table.setCellWidget(r, 3, BarVisualization(bar, self.bar_length))

    def export_csv(self):
        if not self.schedule:
            QMessageBox.warning(self, "No Data", "Nothing to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            for i, bar in enumerate(self.schedule, 1):
                w.writerow([i, sum(bar), self.bar_length - sum(bar)] + bar)
        QMessageBox.information(self, "Export Complete", "CSV exported.")

    def export_excel(self):
        if not self.schedule:
            QMessageBox.warning(self, "No Data", "Nothing to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export Excel", "", "Excel Files (*.xlsx)")
        if not path:
            return
        rows = []
        for i, bar in enumerate(self.schedule, 1):
            rows.append([i, ", ".join(map(str, bar)), self.bar_length - sum(bar)])
        pd.DataFrame(rows, columns=["Bar", "Cuts", "Waste"])\
          .to_excel(path, index=False, engine="openpyxl")
        QMessageBox.information(self, "Export Complete", "Excel exported.")

    def clear_all(self):
        self.cut_requirements = []
        self.schedule = []
        self.table.setRowCount(0)
        self.progress.setValue(0)
        self.status.showMessage("Cleared", 3000)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CutOptimizerGUI()
    win.show()
    sys.exit(app.exec())
