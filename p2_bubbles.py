import matplotlib.pyplot as plt
import pandas as pd
import argparse

#dynamic for any attributes in any order
parser = argparse.ArgumentParser(description='Generate a bubble chart for EV data.')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file name with path')
args = parser.parse_args()

ev = pd.read_csv(args.input)
x = ev["GDP_per_capita"]
y = ev["military_expenditures"]
color = ev["life_expectancy"]
size = ev["population"]

size = size / size.max() * 1300 #scaling 

plt.figure(figsize=(10, 6))
scatter = plt.scatter(x=x, y=y, s=size, c=color, alpha=0.6, cmap='viridis') 

cbar = plt.colorbar(scatter)
cbar.set_label("Life Exepectancy")

legend_sizes = [1e5, 1e7, 1e9]  # population numbers 
legend_labels = [f'{int(val):,}' for val in legend_sizes]  #labels itself with commas in the legend (eg: 1e5 -> 100,000)
max_population = ev["population"].max()  # finding population max

for size_val, label in zip(legend_sizes, legend_labels): #putting together legend size and legend label
    #empty scatter plot
    #calculates s of each dummpy point in relation to population max
    plt.scatter([], [], s=(size_val / max_population) * 1300, color='gray', alpha=0.6, edgecolor='black', label=label) #creating dummy points that will not be visible 

plt.legend( #creating the legend
    title="Population", 
    loc="upper right",  
    frameon=True, 
    fontsize='small', 
    bbox_to_anchor=(1.05, 0.98),  #position and size of the legend
    ncol=1,  # cols in legend
    handlelength=3,  # Increase the length of the legend handles
    borderpad=2,  # Increase padding around the border to make the box bigger
)

plt.xlabel("GDP per Capita")
plt.ylabel("Military Expenditures")
plt.title(f'Bubble Chart representation of GDP per Capita, Military Expenditures, Life Expectancy, Population')

plt.show()