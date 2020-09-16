"""Conversion to JSON-serializable data structure.
"""
import datetime
from typing import Union, Dict, List

import numpy as np

from pdtable.table_metadata import TableOriginCSV

# Typing alias:
# JSON-like data structure of nested "objects" (dict), "arrays" (list), and JSON-native values
JsonData = Union[Dict[str, "JsonData"], List["JsonData"], str, float, int, bool, None]


_json_encodable_value_maps = {
    dict: lambda obj: {kk: to_json_serializable(obj[kk]) for kk in obj.keys()},
    list: lambda obj: [to_json_serializable(kk) for kk in obj],
    float: lambda obj: obj if (not np.isnan(obj)) else None,
    int: lambda obj: obj,
    str: lambda obj: obj,
    bool: lambda obj: obj,
    type(None): lambda obj: obj,
}


def to_json_serializable(obj) -> JsonData:
    """Converts object to a JSON-serializable data structure.
    """
    object_type = type(obj)
    if object_type in _json_encodable_value_maps:
        return _json_encodable_value_maps[object_type](obj)

    # Vanilla JSON encoder will choke on this value type.
    # Represent value as a JSON-encoder-friendly type.
    if isinstance(obj, np.ndarray):
        if f"{obj.dtype}" == "float64":
            return [val if (not np.isnan(val)) else None for val in obj.tolist()]
        else:
            return [to_json_serializable(val) for val in obj.tolist()]

    if isinstance(obj, TableOriginCSV):
        return str(obj._file_name)

    if isinstance(obj, datetime.datetime):
        jval = str(obj)
        return jval if jval != "NaT" else None

    raise NotImplemented(
        "Converting this type to a JSON-encodable type not yet implemented", type(obj)
    )
