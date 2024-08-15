import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Data Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 2)

        self.setup_ui()

        self.df = None

    def setup_ui(self):
        self.load_button = QPushButton("Load CSV")
        self.load_button.clicked.connect(self.load_csv)
        self.left_layout.addWidget(self.load_button)

        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.left_layout.addWidget(QLabel("Analysis:"))
        self.left_layout.addWidget(self.analysis_text)

        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Enter your query here...")
        self.left_layout.addWidget(QLabel("Query:"))
        self.left_layout.addWidget(self.query_input)

        self.query_button = QPushButton("Run Query")
        self.query_button.clicked.connect(self.run_query)
        self.left_layout.addWidget(self.query_button)

        self.plot_view = QWebEngineView()
        self.right_layout.addWidget(self.plot_view)

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            self.df = pd.read_csv(file_name)
            self.perform_analysis()
            self.create_plots()

    def perform_analysis(self):
        if self.df is not None:
            analysis = f"Dataset shape: {self.df.shape}\n\n"
            analysis += "Column names:\n" + "\n".join(self.df.columns) + "\n\n"
            analysis += "Data types:\n" + str(self.df.dtypes) + "\n\n"
            analysis += "Summary statistics:\n" + str(self.df.describe())
            self.analysis_text.setText(analysis)

    def create_plots(self):
        if self.df is not None:
            fig = make_subplots(rows=2, cols=2)

            # Histogram
            fig.add_trace(go.Histogram(x=self.df[self.df.columns[0]], name="Histogram"), row=1, col=1)

            # Scatter plot
            fig.add_trace(go.Scatter(x=self.df[self.df.columns[0]], y=self.df[self.df.columns[1]], mode='markers', name="Scatter"), row=1, col=2)

            # Box plot
            fig.add_trace(go.Box(y=self.df[self.df.columns[0]], name="Box Plot"), row=2, col=1)

            # Bar plot
            fig.add_trace(go.Bar(x=self.df[self.df.columns[0]][:10], y=self.df[self.df.columns[1]][:10], name="Bar Plot"), row=2, col=2)

            fig.update_layout(height=600, width=800, title_text="Data Visualizations")
            self.plot_view.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def run_query(self):
        query = self.query_input.toPlainText()
        if self.df is not None and query:
            try:
                result = self.df.query(query)
                self.analysis_text.setText(str(result))
            except Exception as e:
                self.analysis_text.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzer()
    window.show()
    sys.exit(app.exec_())