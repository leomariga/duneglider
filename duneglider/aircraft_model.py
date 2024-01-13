import aerosandbox as asb
import aerosandbox.numpy as np
import aerosandbox.tools.pretty_plots as p
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class WingSection:
    """
    Define a wing section parameterized with sweep, tip chord and span.
    You can concatenate multiple WingSection by definiing the `init_point` and `init_chord` from previous WingSection or from a root element.

    Args:
        span_tip (float): Span from the tip of this wing section.
        sweep (float): Sweep angle from this wing section (from `init_point`).
        chord_tip (float): Chord from the tip of this wing section.
        airfoil (asb.Airfoil): Airfoil object from aerosandbox.
        init_point (np.ndarray): Point from where this section starts (usually root section or previous tip wing section).
        init_chord (float): Size of chord which this section starts (usually root section chord or previous tip wing section chord).

    """
    span_tip: float
    sweep: float
    chord_tip: float
    airfoil: asb.Airfoil
    init_point: np.ndarray
    init_chord: float

    def get_wing_tip_offset(self) -> np.ndarray:
        """
        Calculate the offset point of the tip of this wing section. Returns a global 3D coordinate.

        return:
            (np.ndarray): Offset point from the tip of the section
        """
        return np.array([self.init_point[0] + (self.span_tip*np.tan(self.sweep)),
                         self.init_point[1] + self.span_tip,
                         0])
    
    def get_area(self):
        """
        Calculate area of the wing.

        return:
            (float): Area of the wing
        """
        return (self.init_chord+self.chord_tip)*self.span_tip/2