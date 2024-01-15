import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import aerosandbox as asb

from IPython.display import display, clear_output
import aerosandbox.numpy as np
from dataclasses import dataclass
from dune_opt import OptScore

def plot_polars(aero, method_name='',):
    fig, ax = plt.subplots(3, 1, figsize=(9, 9), dpi=100)

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
        print(len(optscore.local_min_list))
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
    z_data = []
    for lm in lm_points:
        x_data.append(lm.cl_in_alpha_max_clcd)
        y_data.append(lm.max_clcd)
        z_data.append(lm.score_p)

    # Create a scatter plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(x_data, y_data, c=z_data, cmap='coolwarm')
    
    ax.set_title("Optimization score")
    ax.set_xlabel("$C_L$ [-]")
    ax.set_ylabel("$C_L / C_D$ [-]")

    # Function to execute on click event
    def on_click(event):
        if event.inaxes == ax:
            x_click, y_click = event.xdata, event.ydata
            distances = [(xi - x_click)**2 + (yi - y_click)**2 for xi, yi in zip(x_data, y_data)]
            min_distance_index = distances.index(min(distances))
            clear_output()
            idptn = min_distance_index
            print(f'Clicked on Point {min_distance_index + 1}')
            plot_opt_score(optscore)
            print(f"wing_root_chord: {lm_points[idptn].x[0]}")
            print(f"wing_tip_chord: {lm_points[idptn].x[1]}")
            print(f"wing_sweep: {lm_points[idptn].x[2]*180/np.pi}")
            airplane_clicked = lm_points[idptn].airplane
            airplaneplot = airplane_clicked.draw_three_view()
            plot_polars(lm_points[idptn].aero, "AeroBuildup method")

    # Connect the click event to the figure
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.colorbar(scatter)
    plt.show()




