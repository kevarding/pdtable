# flake8: noqa

__version__ = "0.0.1"

CSV_SEP = ";"  # User can overwrite this default

from .proxy import Table
from .table_metadata import TableOrigin
from .store import TableBundle
from .units import UnitPolicy
from .utils import read_bundle_from_csv, normalized_table_generator
from .readers import read_csv, read_excel
from .writers._csv import write_csv
from .writers._excel import write_excel
