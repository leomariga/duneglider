import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import aerosandbox as asb

import plotly.graph_objects as go
from ipywidgets import widgets
from IPython.display import display
from plotly.subplots import make_subplots
import aerosandbox.numpy as np
from dataclasses import dataclass

from dune_opt import OptScore

def plot_polars(aero, method_name='',):
    fig, ax = plt.subplots(3, 1, figsize=(7, 9), dpi=100)

    plt.sca(ax[0])
    p.plot_smooth(
        aero["alpha"],
        aero["CL"],
        label=method_name,
        function_of="x",
        alpha=0.7,
    )

    plt.sca(ax[1])
    p.plot_smooth(
        aero["alpha"],
        aero["CL/CD"],
        label=method_name,
        function_of="x",
        alpha=0.7,
    )

    plt.sca(ax[2])
    p.plot_smooth(
        aero["alpha"],
        aero["Cm"],
        label=method_name,
        function_of="x",
        alpha=0.7,
    )

    ax[0].set_title("Lift Polar")
    ax[0].set_xlabel("$\\alpha$ [deg]")
    ax[0].set_ylabel("$C_L$ [-]")

    ax[1].set_title("Drag Polar")
    ax[1].set_xlabel("$\\alpha$ [deg]")
    ax[1].set_ylabel("$C_L/C_D$ [-]")

    ax[2].set_title("Moment Polar")
    ax[2].set_xlabel("$\\alpha$ [deg]")
    ax[2].set_ylabel("$C_m$ [-]")

    ax[0].legend(
        title="Analysis Method",
        fontsize=8,
        framealpha=0.2,
    )
    p.show_plot(legend=False)

def plot_opt_score(optscore: OptScore):
    
    @dataclass
    class PlotPoint:
        max_clcd: float
        cl_in_alpha_max_clcd: float
        alpha_max_clcd: float
        score_p: float
        x: np.ndarray
        aero: {}
        airplane: asb.Airplane 
        id_local_min: int
        id_internal_local_min: int

    
    def get_points_local_min():
        plot_point_list = []
        for id_local_min_element in range(len(optscore.local_min_list)):
            local_min_element = optscore.local_min_list[id_local_min_element]

            id_local_min = id_local_min_element
            id_internal_local_min = 0
            score_p = local_min_element['fx']
            x = local_min_element['x']
            aero = local_min_element['aero']
            airplane = local_min_element['airplane']
            max_clcd = np.max(aero['CL/CD'])
            alpha_max_clcd = np.argmax(aero['CL/CD'])
            cl_in_alpha_max_clcd = aero['CL'][alpha_max_clcd]

            plot_point_list.append(PlotPoint(id_local_min = id_local_min,
                                            id_internal_local_min = id_internal_local_min,
                                            score_p = score_p,
                                            x = x,
                                            aero = aero,
                                            airplane = airplane,
                                            max_clcd = max_clcd,
                                            alpha_max_clcd = alpha_max_clcd,
                                            cl_in_alpha_max_clcd = cl_in_alpha_max_clcd))
            
        return plot_point_list


    lm_points = get_points_local_min()
    x_data = []
    y_data = []
    for lm in lm_points:
        x_data.append(lm['cl_in_alpha_max_clcd'])
        y_data.append(lm['max_clcd'])

    # Create the first scatter plot in FigureWidget
    fig1 = go.FigureWidget(data=[go.Scatter(x=x_data, y=y_data, mode='markers')])

    # Create the second plot in FigureWidget with an initial layout
    fig2 = go.FigureWidget(data=[go.Scatter(x=[0], y=[0], mode='lines', line=dict(color='red'))])

    # Display the first figure
    display(fig1)

    # Display the second figure
    display(fig2)

    # Define on_click callback to update the second plot
    def on_click(trace, points, state):
        if points.xs:
            x_coord = points.xs[0]
            y_coord = points.ys[0]

            # Update the second plot with a line from (0, 0) to the clicked point
            fig2.data[0].x = [0, x_coord]
            fig2.data[0].y = [0, y_coord]

    # Assign on_click callback to the scatter trace in the first figure
    fig1.data[0].on_click(on_click)