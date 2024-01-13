import aerosandbox.numpy as np
from dataclasses import dataclass
import aerosandbox as asb

@dataclass
class OptScore:
    """
    Class to store optimization score.

    Args:
        local_min_list (list): List of dict containing x and fx of local minimum.
        global_min (dict): dict containing x and fx of global minimum.
    """
    temp_step_eval_list = []
    local_min_list = []
    global_min = {'x': np.array([0, 0, 0]),
                  'fx': 0,
                  'aero': {},
                  'airplane': asb.Airplane}
    
    def add_step_to_eval_list(self, x, fx, aero, airplane):
        """
        Add a evaluation step

        Args:
            x (ndarray): Array of x value of the optimization.
            fx (float): Score of the optimization.
        """
        self.temp_step_eval_list.append({'x': x,
                                         'fx': fx,
                                         'aero': aero,
                                         'airplane': airplane})

    def add_local_min(self, x, fx, aero, airplane):
        """
        Add a new local minimum point

        Args:
            x (ndarray): Array of x value of the optimization.
            fx (float): Score of the optimization.
        """
        self.local_min_list.append({ 'eval_list': self.temp_step_eval_list,
                                     'x': x,
                                     'fx': fx,
                                     'aero': aero,
                                     'airplane': airplane})
        # Clean temp eval list
        self.temp_step_eval_list = []
        
    def set_global_min(self, x, fx, aero, airplane):
        """
        Set the global minimum point

        Args:
            x (ndarray): Array of x value of the optimization.
            fx (float): Score of the optimization.
        """
        self.global_min = {'x': x, 'fx': fx, 'aero':aero, 'airplane': airplane}