import json
import logging
import os

logger = logging.getLogger('WRT.Config')



##
# Output variables
#print(os.environ.get('WEATHER_DATA'))
COURSES_FILE = os.getenv('WRT_BASE_PATH') + '/CoursesRoute.nc'  # path to file that acts as intermediate storage for courses per routing step
FIGURE_PATH = os.getenv('WRT_FIGURE_PATH')  # path to figure repository
PERFORMANCE_LOG_FILE = os.getenv('WRT_PERFORMANCE_LOG_FILE')  # path to log file which logs performance
INFO_LOG_FILE = os.getenv('WRT_INFO_LOG_FILE')  # path to log file which logs information
ROUTE_PATH = os.getenv('WRT_ROUTE_PATH')  # path to json file to which the route will be written
BASE_PATH = os.getenv('WRT_BASE_PATH')  # path towards the WeatherRoutingTool base directorycd w

##
# Input variables
DEFAULT_ROUTE = format.get_bbox_from_string(os.getenv('WRT_DEFAULT_ROUTE', '-99'))
DEPARTURE_TIME = os.getenv('WRT_DEPARTURE_TIME')  # start time of travelling
DEFAULT_MAP = format.get_bbox_from_string(os.getenv('WRT_DEFAULT_MAP', '-99'))
BOAT_SPEED = float(os.getenv('WRT_BOAT_SPEED', '-99'))  # (m/s)
BOAT_DRAUGHT = 10  # os.getenv('WRT_BOAT_DRAUGHT')  # (m)

##
# Constant settings for isobased algorithm
TIME_FORECAST = 3  # forecast hours weather
ROUTING_STEPS = 6#20  # number of routing steps
DELTA_TIME_FORECAST = 3  # time resolution of weather forecast (hours)
DELTA_FUEL = 1 * 1000  # amount of fuel per routing step (kg)

ROUTER_HDGS_SEGMENTS = 30  # total number of courses : put even number!!
ROUTER_HDGS_INCREMENTS_DEG = 6  # increment of headings
ROUTER_RPM_SEGMENTS = 1  # not used yet
ROUTER_RPM_INCREMENTS_DEG = 1  # not used yet
ISOCHRONE_EXPECTED_SPEED_KTS = 8  # not used yet
ISOCHRONE_PRUNE_SECTOR_DEG_HALF = 91  # angular range of azimuth angle that is considered for pruning (only one half!)
ISOCHRONE_PRUNE_SEGMENTS = 20  # total number of azimuth bins that are used for pruning in prune sector which is 2x

##
# configurations for local execution
WEATHER_DATA = os.getenv('WRT_WEATHER_DATA')  # path to weather data
DEPTH_DATA = os.getenv('WRT_DEPTH_DATA')  # path to depth data
CMEMS_USER = os.getenv('WRT_CMEMS_USER')
CMEMS_PASSWORD = os.getenv('WRT_CMEMS_PASSWORD')

# FIXME: update tests which use BASE_PATH!
MANDATORY_CONFIG_VARIABLES = ['COURSES_FILE', 'DEFAULT_MAP', 'DEFAULT_ROUTE', 'DEPARTURE_TIME', 'DEPTH_DATA',
                              'ROUTE_PATH', 'WEATHER_DATA']

RECOMMENDED_CONFIG_VARIABLES = {
    'BOAT_DRAUGHT': 10,
    'BOAT_SPEED': 6,
    'DATA_MODE': 'automatic'
}

# optional variables with default values
OPTIONAL_VARIABLES = {
    'ALGORITHM_TYPE': 'isofuel',
    'DELTA_FUEL': 3000,
    'DELTA_TIME_FORECAST': 3,
    'FIGURE_PATH': None,  # FIXME: write only if path is set (see routingalg_factory.py)
    'ISOCHRONE_PRUNE_SECTOR_DEG_HALF': 91,
    'ISOCHRONE_PRUNE_SEGMENTS': 20,
    'ISOCHRONE_PRUNE_GCR_CENTERED': True,
    'ISOCHRONE_PRUNE_BEARING': False,
    'ISOCHRONE_MINIMISATION_CRITERION': 'squareddist_over_disttodest',
    'ROUTER_HDGS_INCREMENTS_DEG': 6,
    'ROUTER_HDGS_SEGMENTS': 30,
    'ROUTING_STEPS': 60,
    'TIME_FORECAST': 90
}

class RequiredConfigError(RuntimeError):
    pass


class Config:

    def __init__(self, init_mode='from_json', file_name=None):
        # Details in README
        self.ALGORITHM_TYPE = None  # options: 'isofuel'
        self.BOAT_DRAUGHT = None  # in m
        self.BOAT_SPEED = None  # in m/s
        self.COURSES_FILE = None   # path to file that acts as intermediate storage for courses per routing step
        self.DATA_MODE = None  # options: 'automatic'
        self.DEFAULT_MAP = None  # bbox in which route optimization is performed (lat_min, lon_min, lat_max, lon_max)
        self.DEFAULT_ROUTE = None  # start and end point of the route (lat_start, lon_start, lat_end, lon_end)
        self.DELTA_FUEL = None  # amount of fuel per routing step (kg)
        self.DELTA_TIME_FORECAST = None  # time resolution of weather forecast (hours)
        self.DEPARTURE_TIME = None  # start time of travelling, format: 'yyyy-mm-ddThh:mmZ'
        self.DEPTH_DATA = None  # path to depth data
        self.FIGURE_PATH = None  # path to figure repository
        self.ISOCHRONE_PRUNE_SECTOR_DEG_HALF = None  # half of the angular range of azimuth angle considered for pruning
        self.ISOCHRONE_PRUNE_SEGMENTS = None  # total number of azimuth bins used for pruning in prune sector
        self.ISOCHRONE_PRUNE_GCR_CENTERED = None  # symmetry axis for pruning
        self.ISOCHRONE_PRUNE_BEARING = None  # definitions of the angles for pruning
        self.ISOCHRONE_MINIMISATION_CRITERION = None  # options: 'dist', 'squareddist_over_disttodest'
        self.ROUTER_HDGS_INCREMENTS_DEG = None  # increment of headings
        self.ROUTER_HDGS_SEGMENTS = None  # total number of headings : put even number!!
        self.ROUTE_PATH = None  # path to json file to which the route will be written
        self.ROUTING_STEPS = None  # number of routing steps
        self.TIME_FORECAST = None  # forecast hours weather
        self.WEATHER_DATA = None  # path to weather data

        if init_mode == 'from_json':
            assert file_name
            self.read_from_json(file_name)

        if os.getenv('CMEMS_USERNAME') is None or os.getenv('CMEMS_PASSWORD') is None:
            logger.warning("No CMEMS username and/or password provided! Note that these are necessary if "
                           "DATA_MODE='automatic' used.")

        if (os.getenv('WRT_DB_HOST') is None
                or os.getenv('WRT_DB_PORT') is None
                or os.getenv('WRT_DB_DATABASE') is None
                or os.getenv('WRT_DB_USERNAME') is None
                or os.getenv('WRT_DB_PASSWORD') is None):
            logger.warning("No complete database configuration provided! Note that it is needed for some "
                           "constraint modules.")

    def print(self):
        # ToDo: prettify output
        logger.info(self.__dict__)

    def read_from_json(self, json_file):

        with open(json_file) as f:
            config_dict = json.load(f)
            self._set_mandatory_config(config_dict)
            self._set_recommended_config(config_dict)
            self._set_optional_config(config_dict)

    def _set_mandatory_config(self, config_dict):
        for mandatory_variable in MANDATORY_CONFIG_VARIABLES:
            if mandatory_variable not in config_dict.keys():
                raise RequiredConfigError(f"'{mandatory_variable}' is mandatory!")
            else:
                setattr(self, mandatory_variable, config_dict[mandatory_variable])

    def _set_recommended_config(self, config_dict):
        for recommended_var, default_value in RECOMMENDED_CONFIG_VARIABLES.items():
            if recommended_var not in config_dict.keys():
                logger.warning(f"'{recommended_var}' was not provided in the config and is set to the default value")
                setattr(self, recommended_var, default_value)
            else:
                setattr(self, recommended_var, config_dict[recommended_var])

    def _set_optional_config(self, config_dict):
        for optional_var, default_value in OPTIONAL_VARIABLES.items():
            if optional_var not in config_dict.keys():
                setattr(self, optional_var, default_value)
            else:
                setattr(self, optional_var, config_dict[optional_var])


DATA_MODE = 'from_file'
#DATA_MODE = 'automatic'
