"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import XueXi.views
import XueXi.DateEncoder
from XueXi.Setting import BaseConfig
from XueXi.accessdb import accessdb
#from XueXi.settings import BaseConfig
app.config.from_object(BaseConfig)
