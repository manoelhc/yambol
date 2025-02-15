from __future__ import annotations
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import os
from yambol import db_types
import typing

def parse(filename: str) -> typing.Optional[db_types.Database]:
  with open(filename) as stream:
    data = load(stream, Loader=Loader)
    if check(data):
      return db_types.Database(
        load_types(data),
        load_tables(data)
      )
    else:
      raise Exception("Bad file structure")

def load_types(data: dict) -> typing.List[db_types.Type]:
  types = []
  default_values = db_types.Type.__annotations__
  for t in data['types']:
    t = default_values | t
    db_type = db_types.Type(**t)
    types.append(db_type)
  return types
  
def load_tables(data: dict) -> typing.List[db_types.Table]:
  tables = []
  default_values = db_types.Table.__annotations__
  for t in data['tables']:
    t = default_values | t
    db_table = db_types.Table(**t)
    for key in t.keys():
      setattr(db_table, key, t[key])
    tables.append(db_table)  
  return tables

def check(data: dict) -> bool:
  return 'types' in data and 'tables' in data
