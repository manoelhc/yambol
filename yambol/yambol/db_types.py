from dataclasses import dataclass, field
import typing
from schema import Schema, And, Use, Optional, SchemaError
from typing import List, Literal
import inspect

@dataclass
class Type:
  name: str = ""
  id: bool = False
  check: str = ""
  inline: str = ""
  fk: str = ""
  index: bool = False
  # Strings to adzd at the top of the generated file
  top: list[str] = field(default_factory=list)
  # Strings to add before creating the entity
  before: list[str] = field(default_factory=list)
  # Strings to add after creating the entity
  after: list[str] = field(default_factory=list)
  # Strings to add at the bottom of the file
  bottom: list[str] = field(default_factory=list)
  # Strings to adzd at the top of the generated file
  top_once: list[str] = field(default_factory=list)
  # Strings to add before creating the entity
  before_once: list[str] = field(default_factory=list)
  # Strings to add after creating the entity
  after_once: list[str] = field(default_factory=list)
  # Strings to add at the bottom of the file
  bottom_once: list[str] = field(default_factory=list)
  
  def __init__(self, name, id=False, check="", inline="", fk="", index="", top=[], before=[], after=[], bottom=[], top_once=[], before_once=[], after_once=[], bottom_once=[]):
    if inspect.isclass(id):
      id = False
    self.name = name
    self.id = id
    self.check = check
    self.inline = inline
    self.fk = fk if fk else inline
    self.index = index
    self.top = top
    self.after = after
    self.before = before
    self.bottom = bottom
    self.top_once = top_once
    self.before_once = before_once
    self.after_once = after_once
    self.bottom_once = bottom_once


@dataclass
class Field:
  type: Type
  name: str = ""
  nullable: bool = False
  unique: bool = False
  id: bool = False
  
@dataclass
class ForeignKey:
  name: str = typing.Optional[str]
  type: Type = typing.Optional[Type]
  table: str = typing.Optional[str]
  field: Field = typing.Optional[Field]

@dataclass
class Table:
  name: str
  fields: typing.List[typing.Union[Field, ForeignKey]]

  def __init__(self, name: str, fields: dict):
    self.name = name
    all_fields = []
    for field in fields:
      if 'fk' in field and field['fk']:
        all_fields.append(ForeignKey(name, Field(**field)))
      else:
        all_fields.append(Field(**field))
    self.fields = all_fields
  
@dataclass
class Database:
  name: str
  types: typing.Dict[str, Type]
  tables: typing.List[Table]

  def __init__(self, name: str, types: list[dict], tables: list[dict]):
    self.name = name
    self.types = types
    self.tables = tables
  

schema = Schema(typing.List[Type])