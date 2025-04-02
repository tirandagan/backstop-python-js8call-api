from .core import JS8CallAPI
from .grid_utils import lat_lon_to_grid_square

# Re-export constants for ease of use
JS8_NORMAL = JS8CallAPI.JS8_NORMAL
JS8_FAST = JS8CallAPI.JS8_FAST
JS8_TURBO = JS8CallAPI.JS8_TURBO
JS8_SLOW = JS8CallAPI.JS8_SLOW
JS8_ULTRA = JS8CallAPI.JS8_ULTRA

__version__ = '0.2.0'
__all__ = ['JS8CallAPI', 'lat_lon_to_grid_square', 
           'JS8_NORMAL', 'JS8_FAST', 'JS8_TURBO', 'JS8_SLOW', 'JS8_ULTRA'] 