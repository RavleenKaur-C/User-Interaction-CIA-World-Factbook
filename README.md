# CIA World Factbook: Interactive Data Visualization

This project consists of 4 different visualizations; a bubble chart, an interactive bubble chart (with dropdowns), interactive bubble charts (with drop downs + linked brushing), and interactive bubble charts (with drop downs + tooltip). The dataset contains attributes for various countries, including "GDP per capita," "Birth Rate," "Military Expenditures," "Population," "Life Expectancy," and more. This project focuses on creating interactive visualizations that facilitate user exploration and understanding of the data.


## DATASET

The dataset (`CIA_world_factbook_2023.csv`) is a tabular dataset that provides country-level statistics across several dimensions, such as economic performance, demographics, and health metrics. The dataset includes multiple attributes for analysis and visualization.


## PREREQUISITES

- **Python 3.11** or higher

Required Libraries:
- **pandas** - 2.2.2
- **matplotlib** - 3.9.2
- **PyQt6** - 6.5.2 (for creating user interfaces)
- **argparse** - 1.1

Install the necessary libraries using:
```bash
pip install pandas matplotlib PyQt6 argparse
```
## TASK 1
Objective

Create a static bubble chart visualizing relationships between four attributes:

- GDP_per_capita (x-axis)
- Military_Expenditures (y-axis)
- Population (bubble size)
- Life_Expectancy (bubble color)
- 
Script: p2_bubbles.py

### API Call

```bash
python p2_bubbles.py -i <filename>
```
filename: the path for the csv file the dataset is stored in

### EXAMPLE
```bash
python p2_bubbles.py -i CIA_world_factbook_2023.csv
```

## TASK 2
Objective

Here, I enhance the static bubble chart by adding interactive dropdown menus that allow the user to dynamically select which attributes map to:
* x-axis
* y-axis
* bubble size
* bubble color
Additionally, a slider bar enables scaling of the bubble size. Changes to the dropdown or slider should instantly update the chart.

Script: p2_widgets.py

### API Call

```bash
python p2_widgets.py -i <dataset path>
```
filename: the path for the csv file the dataset is stored in

### EXAMPLE
```bash
python p2_widgets.py -i CIA_world_factbook_2023.csv
```

## TASK 3
Objective

This task includes two interactive bubble charts displayed side by side. Each chart visualizes different attributes based on user selections via dropdown menus. Linked brushing is also implemented where if any bubbles are highlighted on one of the bubble charts, the corresponding bubbles are also highlighted on the other bubble chart. This allows users to delve deeper into how different countries are placed on the bubble chart depending on the indicators chosen.

Script: p2_brushing.py

### API Call
```bash
python p2_brushing.py -i <dataset path>
```
filename: the path for the csv file the dataset is stored in

### EXAMPLE
```bash
python p2_brushing.py -i CIA_world_factbook_2023.csv
```

## TASK 4
Objective

The task was to have the same two bubble charts with dropdowns however now allowing users to have details on demand by implementing a tooltip feature. When the user hovers over a data point in the bubble chart, detailed information is displayed in a box display such as country name and attribute values for the selected data point. The corresponding data point of the selected data point on one bubble chart is also highlighted on the other.

Script: p2_brushing.py

### API Call
```bash
python p2_tooltip.py -i <dataset path>
```
filename: the path for the csv file the dataset is stored in

### EXAMPLE
```bash
python p2_tooltip.py -i CIA_world_factbook_2023.csv
```

