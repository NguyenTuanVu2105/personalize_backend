import json
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal


class JSONEncoder(json.JSONEncoder):
    def default(self, obj, stop=False):
        json_data = {}
        if not isinstance(obj, dict):
            try:
                obj = obj.__dict__
            except AttributeError:
                return obj
        for key, val in obj.items():
            if key.startswith("_"):
                continue
            if isinstance(val, (dict, OrderedDict)):
                json_data[key] = {}
                for sub_key, sub_val in val.items():
                    json_data[key][sub_key] = self.default(sub_val)
            elif isinstance(val, list):
                json_data[key] = []
                for sub_val in val:
                    json_data[key].append(self.default(sub_val))
            elif isinstance(val, (Decimal, datetime, bool, int, float)):
                json_data[key] = str(val)
            elif not isinstance(val, str):
                json_data[key] = val and self.default(val, True) if not stop else str(val)
            else:
                json_data[key] = val
        return json_data
