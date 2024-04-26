"""
CTkRadarChart
Author: Akash Bora (Akascape)
"""

import tkinter as tk
import math
from typing import Union, Tuple, Optional, Any
import random
import customtkinter
from customtkinter.windows.widgets.appearance_mode import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling import CTkScalingBaseClass

class CTkRadarChart(tk.Canvas, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    """ A class for displaying radar chart in customtkinter """
    def __init__(self,
                 master: Any,
                 radius: int=400,
                 num_axes: int=6,
                 radial_lines: int=5,
                 border_width: int=2,
                 padding: int=30,
                 labels: list=[],
                 font: Optional[Union[tuple, customtkinter.CTkFont]] = None,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 **kwargs):
        
        self.master = master
        self.bg_color = master.cget("fg_color") if (bg_color=="transparent" or bg_color is None) else bg_color
    
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="widget")
        
        self.radius = self._apply_widget_scaling(radius)
        self.font = font
        self.border_width = self._apply_widget_scaling(border_width)
        
        self.fg_color = customtkinter.ThemeManager.theme["CTkButton"]["border_color"] if fg_color is None else text_color
        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.num_axes = num_axes
        self.radial_lines = radial_lines
        
        if self.num_axes<=2:
            raise ValueError("Axes number must be greater or equal to 3")

        if self.radial_lines<=0:
            self.radial_lines = 1

        super().__init__(master, bg=self.master._apply_appearance_mode(self.bg_color),
                         highlightthickness=0, width=self.radius, height=self.radius,
                         borderwidth=0, **kwargs)
        
        self.data = []
        self.colors = []
        self.fills = []
        self.tags = []
        
        self.labels = labels if labels is not None else [''] * num_axes
        
        self.padding = padding  # Padding from the left side
        self.center = (self.radius + self.padding, self.radius + self.padding)
        self.draw_chart()

        # Bind the resize event
        self.bind("<Configure>", self.resize, add="+")

    def draw_chart(self):
        self.delete("all")  # Clear the canvas
        self.draw_background()
        for data in self.data:
            if len(data)!=self.num_axes:
                data.append(0)

        for dataset, color, fill in zip(self.data, self.colors, self.fills):
            self.draw_dataset(dataset, color, fill)
        self.draw_labels()
        
    def draw_background(self):
        # Draw the axes and background lines
        for i in range(self.num_axes):
            angle = 2 * math.pi * i / self.num_axes
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            self.create_line(self.center[0], self.center[1], x, y,
                             fill=self.master._apply_appearance_mode(self.fg_color))
            self.draw_polygon(i, outline=self.master._apply_appearance_mode(self.fg_color))

    def draw_polygon(self, i, outline):
        points = []
        for j in range(1, self.radial_lines+1):  # Draw 5 concentric polygons for the background
            current_points = []
            for k in range(self.num_axes):
                angle = 2 * math.pi * k / self.num_axes
                x = self.center[0] + (self.radius * j / self.radial_lines) * math.cos(angle)
                y = self.center[1] + (self.radius * j / self.radial_lines) * math.sin(angle)
                current_points.extend([x, y])
            self.create_polygon(current_points, outline=outline, fill='', width=1)

    def draw_dataset(self, dataset, color, fill):
        # Draw the data
        data_points = []
        for i, value in enumerate(dataset[:self.num_axes]):
            angle = 2 * math.pi * i / self.num_axes
            x = self.center[0] + self.radius * value / 100 * math.cos(angle)
            y = self.center[1] + self.radius * value / 100 * math.sin(angle)
            data_points.extend([x, y])
    
        outline_color = self.master._apply_appearance_mode(color)

        fill_color = ''
        if fill:
            fill_color = outline_color
            
        self.create_polygon(data_points, outline=outline_color, fill=fill_color, stipple='gray12',
                            width=self.border_width)

    def draw_labels(self):
        # Draw labels at each corner
        for i, label in enumerate(self.labels[:self.num_axes]):
            angle = 2 * math.pi * i / self.num_axes
            x = self.center[0] + (self.radius + 10) * math.cos(angle)
            y = self.center[1] + (self.radius + 10) * math.sin(angle)
            self.create_text(x, y, text=label, font=self.font, anchor='center',
                             fill=self.master._apply_appearance_mode(self.text_color))

    def resize(self, event):
        # Update the center and radius based on the new window size
        self.radius = min(event.width - self.padding * 2, event.height - self.padding * 2) // 2
        self.center = (event.width // 2, event.height // 2)
        self.draw_chart()

    def add_data(self, tag, data=[], color=None, fill=True):
        # Add new data to the chart
        if type(data) is not list:
            raise ValueError("Chart data must be in a list.")

        if tag in self.tags:
            self.delete_data(tag)
            
        for value in data:
            if value>100:
                data[data.index(value)] = 100
            elif value<0:
                data[data.index(value)] = 0
        
        if color is None:
            # select a random color
            color = outline_color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        
        self.data.append(data)
        self.colors.append(color)
        self.fills.append(fill)
        self.tags.append(tag)
        self.draw_chart()

    def delete_data(self, tag):
        # delete the tag data from chart
        if tag not in self.tags:
            return
        index = self.tags.index(tag)
        self.data.pop(index)
        self.fills.pop(index)
        self.colors.pop(index)
        self.tags.pop(index)
        self.draw_chart()

    def update_data(self, tag, data=None, color=None, fill=None):
        # update a tag data 
        if tag not in self.tags:
            return
        
        index = self.tags.index(tag)
        if data is not None:
            self.data[index] = data
        if color is not None:
            self.colors[index] = color
        if fill is not None:
            self.fills[index] = kwargs["fill"]
            
        self.add_data(tag=tag, data=self.data[index], color=self.colors[index], fill=self.fills[index])
        
    def _set_appearance_mode(self, mode_string):
        super().config(bg=self.master._apply_appearance_mode(self.bg_color))
        self.draw_chart()

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        super()._set_scaling(new_widget_scaling, new_window_scaling)
        self.radius = self._apply_widget_scaling(self.radius)
        super().config(width=self.radius, height=self.radius)
        self.border_width = self._apply_widget_scaling(self.border_width)
        self.draw_chart()

    def configure(self, **kwargs):
        # configurable options
        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            
        if "bg_color" in kwargs:
            self.bg_color = kwargs.pop("bg_color")
            super().config(bg=self.master._apply_appearance_mode(self.bg_color))
            
        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            
        if "font" in kwargs:
            self.font = kwargs.pop("font")

        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")

        if "radial_lines" in kwargs:
            self.radius_lines = kwargs.pop("radial_lines")
            if self.radial_lines<=0:
                self.radial_lines = 1
                
        if "radius" in kwargs:
            self.radius = kwargs.pop("radius")
            super().config(width=self.radius, height=self.radius)

        if "num_axes" in kwargs:
            self.num_axes = kwargs.pop("num_axes")

        if "labels" in kwargs:
            self.labels = kwargs.pop("labels")

        if "padding" in kwargs:
            self.padding = kwargs.pop("padding")
            
        super().config(**kwargs)
        self.draw_chart()

    def cget(self, param):
        # return required parameter
        if params=="fg_color":
            return self.fg_color
            
        if params=="bg_color":
            return self.bg_color
            
        if params=="border_width":
            return self.border_width
            
        if params=="font":
            return self.font

        if params=="text_color":
            return self.text_color

        if params=="radial_lines":
            return self.radius_lines
                
        if params=="radius":
            return self.radius 

        if params=="num_axes":
            return self.num_axes

        if params=="labels":
            return self.labels

        if params=="data":
            return self.get()

        if params=="padding":
            return self.padding
        
        return super().cget(param)

    def get(self, tag=None):
        # get values from the chart
        if tag:
            index = self.tags.index(tag)
            return self.data[index], self.colors[index]
        
        data = {}
        for tag in self.tags:
            index = self.tags.index(tag)
            data.update({tag:{'data':self.data[index],'color':self.colors[index]}})
        return data
