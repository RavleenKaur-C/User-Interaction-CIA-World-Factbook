import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSlider
from PyQt6.QtCore import Qt
import argparse

class InteractiveBubbleChartApp(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df.drop(columns=['name', 'region'], errors='ignore') #remove name and region as they are not values that can be represented on this chart
        self.selected_indices = set()

        #convert columns to numeric and save numeric columns
        self.df = self.df.apply(pd.to_numeric, errors='coerce')
        self.numeric_columns = self.df.select_dtypes(include=[float, int]).columns.tolist()

        self.colorbar1 = None
        self.colorbar2 = None
        self.rect_selector1 = None
        self.rect_selector2 = None

        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle('Linked Bubble Charts with Legend, Color Bar, and Brushing')
        self.setGeometry(100, 100, 1800, 900)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        #horizontal layout for chart
        charts_layout = QHBoxLayout()
        controls_layout = QHBoxLayout()

        #create left and right chart
        self.left_canvas, self.left_ax = self.create_chart()
        self.right_canvas, self.right_ax = self.create_chart()

        charts_layout.addWidget(self.left_canvas)
        charts_layout.addWidget(self.right_canvas)

        #controls
        self.left_controls = self.create_controls(label="Left", controls_layout=controls_layout)
        self.right_controls = self.create_controls(label="Right", controls_layout=controls_layout)

        layout.addLayout(charts_layout)
        layout.addLayout(controls_layout)

        self.update_plots()

        #rectangale for each chart
        self.rect_selector1 = RectangleSelector(self.left_ax, lambda eclick, erelease: self.on_select(eclick, erelease, 'left'),
                                                useblit=True, interactive=True)
        self.rect_selector2 = RectangleSelector(self.right_ax, lambda eclick, erelease: self.on_select(eclick, erelease, 'right'),
                                                useblit=True, interactive=True)

        self.left_canvas.mpl_connect('button_press_event', self.reset_selection)
        self.right_canvas.mpl_connect('button_press_event', self.reset_selection)

    def create_chart(self):
        figure, ax = plt.subplots(figsize=(8, 6))
        canvas = FigureCanvas(figure)
        return canvas, ax

    def create_controls(self, label, controls_layout):
        control_layout = QVBoxLayout()

        x_select = QComboBox()
        x_select.addItems(self.numeric_columns)

        y_select = QComboBox()
        y_select.addItems(self.numeric_columns)

        color_select = QComboBox()
        color_select.addItems(self.df.columns)

        size_select = QComboBox()
        size_select.addItems(self.numeric_columns)

        scaling_slider = QSlider(Qt.Orientation.Horizontal)
        scaling_slider.setMinimum(100)
        scaling_slider.setMaximum(2000)
        scaling_slider.setValue(1300)

        control_layout.addWidget(QLabel(f'{label} X-axis:'))
        control_layout.addWidget(x_select)
        control_layout.addWidget(QLabel(f'{label} Y-axis:'))
        control_layout.addWidget(y_select)
        control_layout.addWidget(QLabel(f'{label} Color:'))
        control_layout.addWidget(color_select)
        control_layout.addWidget(QLabel(f'{label} Size:'))
        control_layout.addWidget(size_select)
        control_layout.addWidget(QLabel(f'{label} Scaling:'))
        control_layout.addWidget(scaling_slider)

        controls_layout.addLayout(control_layout)

        # connecting combo boxes and slider
        x_select.currentIndexChanged.connect(self.update_plots)
        y_select.currentIndexChanged.connect(self.update_plots)
        color_select.currentIndexChanged.connect(self.update_plots)
        size_select.currentIndexChanged.connect(self.update_plots)
        scaling_slider.valueChanged.connect(self.update_plots)

        return {
            'x_select': x_select,
            'y_select': y_select,
            'color_select': color_select,
            'size_select': size_select,
            'scaling_slider': scaling_slider
        }

    def update_plots(self):
        left_x = self.left_controls['x_select'].currentText()
        left_y = self.left_controls['y_select'].currentText()
        left_color = self.left_controls['color_select'].currentText()
        left_size = self.left_controls['size_select'].currentText()
        left_scale = self.left_controls['scaling_slider'].value() / 1000

        right_x = self.right_controls['x_select'].currentText()
        right_y = self.right_controls['y_select'].currentText()
        right_color = self.right_controls['color_select'].currentText()
        right_size = self.right_controls['size_select'].currentText()
        right_scale = self.right_controls['scaling_slider'].value() / 1000

        #update the plots
        self.plot_chart(self.left_ax, left_x, left_y, left_color, left_size, left_scale, self.left_canvas, side='left')
        self.plot_chart(self.right_ax, right_x, right_y, right_color, right_size, right_scale, self.right_canvas, side='right')

    def plot_chart(self, ax, x_attr, y_attr, color_attr, size_attr, scale_factor, canvas, side):
        ax.clear()

        x_data = pd.to_numeric(self.df[x_attr], errors='coerce').fillna(0)
        y_data = pd.to_numeric(self.df[y_attr], errors='coerce').fillna(0)
        size_data = pd.to_numeric(self.df[size_attr], errors='coerce').fillna(1)
        color_data = pd.Categorical(self.df[color_attr]).codes if self.df[color_attr].dtype == 'object' else self.df[color_attr]

        size_scaled = (size_data - size_data.min()) / (size_data.max() - size_data.min()) * scale_factor * 1000

        scatter = ax.scatter(x_data, y_data, s=size_scaled, c=color_data, cmap='viridis', alpha=1.0, edgecolor='w')
        ax.set_xlabel(x_attr)
        ax.set_ylabel(y_attr)

        #add the size legend
        self.add_size_legend(ax, size_attr, scale_factor)

        #add color bar
        if side == 'left':
            if self.colorbar1 is None:
                self.colorbar1 = self.left_canvas.figure.colorbar(scatter, ax=ax, label=color_attr)
            else:
                self.colorbar1.set_label(color_attr)
                self.colorbar1.update_normal(scatter)
        else:
            if self.colorbar2 is None:
                self.colorbar2 = self.right_canvas.figure.colorbar(scatter, ax=ax, label=color_attr)
            else:
                self.colorbar2.set_label(color_attr)
                self.colorbar2.update_normal(scatter)

        canvas.draw()

        #highlighting the points 
        self.highlight_selected()

    def add_size_legend(self, ax, size_attr, scale_factor):
        size_values = pd.to_numeric(self.df[size_attr], errors='coerce').fillna(0)

        #manually setting
        min_size = size_values.quantile(0.25)
        median_size = size_values.median()
        max_size = size_values.max()

        min_bubble_size = (min_size / max_size) * scale_factor * 1000
        median_bubble_size = (median_size / max_size) * scale_factor * 1000
        max_bubble_size = (max_size / max_size) * scale_factor * 1000

        legend_sizes = [min_bubble_size, median_bubble_size, max_bubble_size]
        legend_labels = [f'{min_size:.2f}', f'{median_size:.2f}', f'{max_size:.2f}']

        for size, label in zip(legend_sizes, legend_labels):
            ax.scatter([], [], s=size, color='gray', alpha=0.5, edgecolor='black', label=label)

        ax.legend(title=size_attr, title_fontsize='13', loc="upper right", frameon=True, fontsize='10', scatterpoints=1)

    def on_select(self, eclick, erelease, side):
        self.selected_indices.clear()
    
        x_min, x_max = sorted([eclick.xdata, erelease.xdata])
        y_min, y_max = sorted([eclick.ydata, erelease.ydata])
    
        if side == 'left':
            x_attr = self.left_controls['x_select'].currentText()
            y_attr = self.left_controls['y_select'].currentText()
        else:
            x_attr = self.right_controls['x_select'].currentText()
            y_attr = self.right_controls['y_select'].currentText()
    
        for i in range(len(self.df)):
            x_value = self.df.iloc[i][x_attr]
            y_value = self.df.iloc[i][y_attr]
            if x_min <= x_value <= x_max and y_min <= y_value <= y_max:
                self.selected_indices.add(i)
    
        self.highlight_selected()
    
        #hiding the selector
        if side == 'left':
            self.rect_selector1.set_visible(False)
            self.rect_selector1.set_active(False)
        else:
            self.rect_selector2.set_visible(False)
            self.rect_selector2.set_active(False)
    
        #redrawing canvas to make sure selector is gone
        if side == 'left':
            self.left_canvas.draw()
        else:
            self.right_canvas.draw()


    def reset_selection(self, event):
        self.selected_indices.clear()
    
        #reactiviating selector
        self.rect_selector1.set_active(True)
        self.rect_selector2.set_active(True)
    
        #bring back original plots
        self.update_plots()


    def highlight_selected(self):
        if self.selected_indices:
            self.apply_selection_highlight(self.left_ax, side='left')
            self.apply_selection_highlight(self.right_ax, side='right')

    def apply_selection_highlight(self, ax, side):
        if side == 'left':
            x_attr = self.left_controls['x_select'].currentText()
            y_attr = self.left_controls['y_select'].currentText()
            color_attr = self.left_controls['color_select'].currentText()
            size_attr = self.left_controls['size_select'].currentText()
            scale_factor = self.left_controls['scaling_slider'].value() / 1000
        else:
            x_attr = self.right_controls['x_select'].currentText()
            y_attr = self.right_controls['y_select'].currentText()
            color_attr = self.right_controls['color_select'].currentText()
            size_attr = self.right_controls['size_select'].currentText()
            scale_factor = self.right_controls['scaling_slider'].value() / 1000

        x_data = pd.to_numeric(self.df[x_attr], errors='coerce').fillna(0)
        y_data = pd.to_numeric(self.df[y_attr], errors='coerce').fillna(0)
        size_data = pd.to_numeric(self.df[size_attr], errors='coerce').fillna(1)
        color_data = pd.Categorical(self.df[color_attr]).codes if self.df[color_attr].dtype == 'object' else self.df[color_attr]

        size_scaled = (size_data - size_data.min()) / (size_data.max() - size_data.min()) * 1000

        #dimming not selected points
        colors = [color_data[i] for i in range(len(self.df))]
        alphas = [1.0 if i in self.selected_indices else 0.2 for i in range(len(self.df))]

        ax.clear()
        ax.scatter(x_data, y_data, s=size_scaled, c=colors, alpha=alphas, cmap='viridis', edgecolor='w')
        ax.set_xlabel(x_attr)
        ax.set_ylabel(y_attr)

        #ensuring legend is there
        self.add_size_legend(ax, size_attr, scale_factor)
        ax.figure.canvas.draw()


def main():
    parser = argparse.ArgumentParser(description="Linked bubble charts")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file name with path')
    args = parser.parse_args()
    dataset_path = args.input
    df = pd.read_csv(dataset_path)

    app = QApplication(sys.argv)
    main_window = InteractiveBubbleChartApp(df)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
