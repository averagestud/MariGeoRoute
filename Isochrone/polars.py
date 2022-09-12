"""
Boat polars file
Have TWA(True wind Angle) and TWS (True Wind speed) value for calculate boat speed and properties


"""
import numpy as np
""" Interpolation  a method of constructing new data points based on the range of a discrete set of known data points. 
The data must be defined on a regular grid; the grid spacing however may be uneven. Linear and nearest-neighbor
 interpolation are supported """
from scipy.interpolate import RegularGridInterpolator

from utils import knots_to_mps #Convert  knot value in meter per second


def boat_properties(filepath):
    """
    Load boat properties from boat file.

            Parameters:
                    filepath (string): Path to polars file polar VO7O

            Returns:
                    boat (dict): Dict with function and raw polars
    """
    polars = np.genfromtxt(filepath, delimiter=';')
    polars = np.nan_to_num(polars) #Replace with NAN value with the zero or infinity values

    ws = polars[0, 1:]
    wa = polars[1:, 0]
    values = polars[1:, 1:]

    # internally we use only meters per second
    ws = knots_to_mps(ws)
    values = knots_to_mps(values)

    f = RegularGridInterpolator(
        (ws, wa), values.T,
        bounds_error=False,
        fill_value=None
    )
    return {'func': f, 'polars': polars}


def boat_speed_function(boat, wind):
    """
    Vectorized boat speed function.

            Parameters:
                    boat (dict): Boat dict with wind function
                    wind (dict): Wind dict with TWA and TWS arrays

            Returns:
                    boat_speed (array): Array of boat speeds
    """
    twa = wind['twa']
    tws = wind['tws']
     #Assert to check the condition if false give assertion error
    assert twa.shape == tws.shape, "Input shape mismatch"
    func = boat['func']

    # get rid of negative and above 180
    twa = np.abs(twa)# mathematical function helps user to calculate absolute value of each element
    twa[twa > 180] = 360. - twa[twa > 180]
    #twa[twa > 27] = 56. - twa[twa > 27]

    # init boat speed vector
    boat_speed = func((tws, twa))
    #boat_speed=abs(boat_speed)
    return boat_speed


