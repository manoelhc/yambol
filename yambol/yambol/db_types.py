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
  # Strings to adzd at the top of the generated file
  top: List[str] = field(default_factory=List)
  # Strings to add before creating the entity
  before: List[str] = field(default_factory=List)
  # Strings to add after creating the entity
  after: List[str] = field(default_factory=List)
  # Strings to add at the botton of the file
  botton: List[str] = field(default_factory=List)
  # Strings to adzd at the top of the generated file
  top_once: List[str] = field(default_factory=List)
  # Strings to add before creating the entity
  before_once: List[str] = field(default_factory=List)
  # Strings to add after creating the entity
  after_once: List[str] = field(default_factory=List)
  # Strings to add at the botton of the file
  botton_once: List[str] = field(default_factory=List)

@dataclass
class Field:
  type: Type
  name: str = ""
  nullable: bool = False
  unique: bool = False
  pk: bool = False
  
@dataclass
class ForeignKey:
  field: Field

@dataclass
class Table:
  name: str
  fields: typing.List[typing.Union[Field, ForeignKey]]

@dataclass
class Database:
  types: typing.List[Type]
  tables: typing.List[Table]

schema = Schema(typing.List[Type])