# CTkRadarChart
A simple widget for customtkinter to display radar chart, made with only tkinter canvas. Full custimasable widget, with resizability and themes.

## Installation
### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkRangeSlider?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/CTkRadarChart/archive/refs/heads/main.zip)

Download the source code, paste the `CTkRadarChart` folder in the directory where your program is present.

## Usage
```python
import customtkinter
from CTkRadarChart import *

root = customtkinter.CTk()

# Some labels that are shown at each axis
labels = ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency', 'Capacity']

# Create the RadarChart instance
chart = CTkRadarChart(root, labels=labels)
chart.pack()

# Add new data
chart.add_data("A", [90, 70, 90, 75, 60, 80])
chart.add_data("B", [60, 80, 70, 85, 75, 90])

root.mainloop()
```

_Note: data should be in a list, maximum value: 100, minimum value: 0_

## Arguments
| Parameters | Details |
|--------|----------|
| master	| root window, can be _CTk_ or _CTkFrame_|
| radius | the initial size of the radar chart |
| num_axes | number of axes in the chart |
| radial_lines | number of grid lines inside the chart |
| border_width | size of the data lines |
| fg_color | color of the background chart lines |
| bg_color | background color of the widget |
| text_color | color of the label text |
| labels | text shown at each axes |
| padding | adjust space inside the widget |
| font | font of the text labels |

## Methods
- **.add_data(tag, data, color, fill)**: adds new data line in the chart, tag: line name, data: list of values, color: color of line (optional, choses color randomly), fill: add color in the polygon (optional, true by default)
- **.delete_data(tag)**: delete a line from the chart
- **.update_data(tag, *args)**: update any tag data
- **.get(tag)**: return data and color of the chart, tag is optional
- **.configure(*args)**: change parameters of the radar chart
- **.cget(parameter)**: return the required parameter from the chart

Follow me for more stuff like this: [`Akascape`](https://github.com/Akascape/)
### That's all, hope it will help!
