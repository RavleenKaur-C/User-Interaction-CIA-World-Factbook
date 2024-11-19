import sys
import argparse
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QSlider, QSizePolicy)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class InteractiveBubbleChart(QMainWindow): #main application window
    def __init__(self, dataset): 
        super().__init__()
        self.dataset = dataset
        self.UI_setup() #intializing user interface

    def update_chart(self):
        # get selected attributes from the combobox
        x_attr = self.combo_x.currentText()
        y_attr = self.combo_y.currentText()
        radius_attr = self.combo_radius.currentText()
        color_attr = self.combo_color.currentText()
        size_scale = self.bubble_size_slider.value()  # get size from the slider in numeric form
    
        # filtered dataset has no rows with missing values
        filtered_data = self.dataset.dropna()
    
        # extracting values from the new df
        x = pd.to_numeric(filtered_data[x_attr], errors='coerce')
        y = pd.to_numeric(filtered_data[y_attr], errors='coerce')
        size = pd.to_numeric(filtered_data[radius_attr], errors='coerce')
        color = pd.to_numeric(filtered_data[color_attr], errors='coerce')
    
        #handling NaN values
        size = size.clip(lower=0)
    
        #scaling according to slider numeric value that was obtained
        size = size / size.max() * size_scale
    
        self.figure.clear()
    
        # creating the bubble chart
        ax = self.figure.add_subplot(111)
        scatter = ax.scatter(x, y, s=size, c=color, cmap='viridis', alpha=0.6)
    
        # adding the colorbar
        cbar = self.figure.colorbar(scatter)
        cbar.set_label(color_attr)
    
        ax.set_xlabel(x_attr)
        ax.set_ylabel(y_attr)
        ax.set_title(f'Bubble Chart of {x_attr} vs {y_attr} vs {radius_attr} vs {color_attr}')
    
        # adding bubble legend
        self.add_bubble_legend(ax, radius_attr, size_scale)
    
        self.canvas.draw()

    def UI_setup(self):
        self.setWindowTitle('Interactive Bubble Chart')

        # main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget) #in the center

        # layout for widgets and plot
        layout = QVBoxLayout(main_widget)

        # dropdown menus for selecting attributes
        self.combo_x = QComboBox(self)
        self.combo_y = QComboBox(self)
        self.combo_radius = QComboBox(self)
        self.combo_color = QComboBox(self)

        attributes = self.dataset.columns #populating drop down menu with all columnn titles from df
        for combo in [self.combo_x, self.combo_y, self.combo_radius, self.combo_color]:
            combo.addItems(attributes) #adding them to each combobox

        # setting an intial selection
        self.combo_x.setCurrentText('GDP_per_capita')
        self.combo_y.setCurrentText('military_expenditures')
        self.combo_radius.setCurrentText('population')
        self.combo_color.setCurrentText('life_expectancy')

        self.bubble_size_slider = self.create_slider('Bubble Size Scale', layout, min_val=100, max_val=2000, default_val=1300)

        # add labels and dropdowns to the layout
        combo_layout = QHBoxLayout() #Dropdown and labels are horizontally set
        combo_layout.addWidget(QLabel('X-Axis:')) 
        combo_layout.addWidget(self.combo_x)
        combo_layout.addWidget(QLabel('Y-Axis:'))
        combo_layout.addWidget(self.combo_y)
        combo_layout.addWidget(QLabel('Bubble Size:'))
        combo_layout.addWidget(self.combo_radius)
        combo_layout.addWidget(QLabel('Bubble Color:'))
        combo_layout.addWidget(self.combo_color)
        layout.addLayout(combo_layout) #adding the horizontally layout set up above to the main layout

        self.figure = plt.figure() #creating matplotlib figure
        self.canvas = FigureCanvas(self.figure) #creating canvas for the matplotlib
        layout.addWidget(self.canvas) #adding the canvas to the main layout

        # functions that are called when the users interact with the widgets
        self.combo_x.currentTextChanged.connect(self.update_chart)
        self.combo_y.currentTextChanged.connect(self.update_chart)
        self.combo_radius.currentTextChanged.connect(self.update_chart)
        self.combo_color.currentTextChanged.connect(self.update_chart)
        self.bubble_size_slider.valueChanged.connect(self.update_chart)
        # updating everytime it is changed

        # initial plot
        self.update_chart()

    def create_slider(self, label, layout, min_val, max_val, default_val):
        layout.addWidget(QLabel(label))  # Add label above the slider
        slider = QSlider(Qt.Orientation.Horizontal) #creating horizontal slider
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)  # Default scale
        layout.addWidget(QLabel('Bubble Size Scaling:'))
        layout.addWidget(slider)  # Add slider to the layout
        return slider

    def add_bubble_legend(self, ax, radius_attr, size_scale):

        size_values = pd.to_numeric(self.dataset[radius_attr], errors='coerce').fillna(0)  #convert to numeric and handle NaN
        first_quartile_value = size_values.quantile(0.25)        
        largest_value = size_values.max()
        median_value = size_values.median()
        
        legend_sizes = [first_quartile_value, median_value, largest_value] 
        legend_labels = [f'{int(val):,}' for val in legend_sizes] 
        max_value = largest_value 

        for size_val, label in zip(legend_sizes, legend_labels):  
            ax.scatter([], [], s=(size_val / max_value) * size_scale, color='gray', alpha=0.6, edgecolor='black', label=label)

        ax.legend(title=radius_attr, loc="upper right", frameon=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Interactive Bubble Chart")

    parser.add_argument('-i', '--input', type=str, required=True, help='Input file name with path')
    args = parser.parse_args()
    dataset_path = args.input
    dataset = pd.read_csv(dataset_path)

    app = QApplication(sys.argv)
    main_window = InteractiveBubbleChart(dataset)
    main_window.show()

    sys.exit(app.exec())
    