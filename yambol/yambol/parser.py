from __future__ import annotations
from yaml import load, dump
import sys
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
      types = load_types(data)
      return db_types.Database(
        data["name"],
        types,
        load_tables(data, types)
      )
    else:
      raise Exception("Bad file structure")

def load_types(data: dict) -> typing.List[db_types.Type]:
  types = {}
  default_values = db_types.Type.__annotations__
  for t in data['types']:
    t = default_values | t
    db_type = db_types.Type(**t)
    if not isinstance(db_type.fk, str) or len(db_type.fk) == 0:
      db_type.fk = db_type.inline
    if db_type.name in types:
      raise KeyError(f"The type {db_type.name} has been already defined.")
    types[db_type.name] = db_type
  return types

def find_type(types=dict[str, db_types.Type], name=str):
  if name in types:
    return types[name]
  return db_types.Type(name=name, inline=name)

def assembly_table(dict_table: dict, types: dict[str, db_types.Type]):
  db_table = db_types.Table(**dict_table)
  for key in dict_table.keys():
    setattr(db_table, key, dict_table[key])
  fields = []
  
  for field in db_table.fields:
    if 'type' in field and 'fields' in field['type']:
      new_field = db_types.ForeignKey()
      new_field.name = field['name']
      sub_table = db_types.Table(**field['type'])
      for sub_field in sub_table.fields:
        fk_type = get_fk_type(types, field['type'])
        new_field.type = fk_type
        fk_field = get_fk_field(fk_type, sub_field)
        if fk_field:
          new_field.field = fk_field
      new_field.table = sub_table
      if not new_field.field:
        raise ValueError(f"There's no clear field for {new_field.name}: {new_field}")
      field = new_field
    elif 'name' in field and isinstance(field['type'], str):
      field = db_types.Field(**field)
      found_type = find_type(types, field.type)
      field.type = found_type
      field.id = found_type.id
    fields.append(field)
  db_table.fields = fields
  return db_table

def load_tables(data: dict, types=dict[str, db_types.Type]) -> typing.List[db_types.Table]:
  tables = []
  for t in data['tables']:
    db_table = assembly_table(t, types)
    tables.append(db_table)  
  return tables

def get_fk_type(types: dict[str, db_types.Type], raw_table: dict):
  if 'fields' in raw_table:
    for field in raw_table['fields']:
      if isinstance(field['type'], str):
        field_type = find_type(types, field['type'])
      else:
        field_type = get_fk_type(types, field['type'])
      if field_type.id:
        return field_type
  raise ValueError(f"The table {raw_table['name']} doesn't have an 'id' field.")

def get_fk_field(type, field):
  if field.type == type.name:
    return field
  return None

def check(data: dict) -> bool:
  return 'types' in data and 'tables' in data
