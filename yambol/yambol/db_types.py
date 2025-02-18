from dataclasses import dataclass, field
import typing
from schema import Schema, And, Use, Optional, SchemaError
from typing import List

@dataclass
class Type:
  name: str = ""
  id: bool = False
  check: str = ""
  inline: str = ""
  fk: bool = False
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

@dataclass
class Field:
  type: Type
  name: str = ""
  nullable: bool = False
  unique: bool = False
  pk: bool = False
  
@dataclass
class ForeignKey:
  type: str
  table: str
  field: Field

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
  types: typing.List[Type]
  tables: typing.List[Table]

schema = Schema(typing.List[Type])