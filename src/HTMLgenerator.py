from bs4 import BeautifulSoup
import sqlite3
import re
import math

import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

from pages.bbg_expanded import *
from pages.buildings import *
from pages.city_states import *
from pages.governor import *
from pages.great_people import *
from pages.leaders import *
from pages.misc import *
from pages.names import *
from pages.natural_wonder import *
from pages.religion import *
from pages.units import *
from pages.world_wonder import *