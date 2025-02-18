from yambol.plugin import Plugin
import itertools
from yambol.db_types import Table, ForeignKey, Type, Field
import types
from typing import Optional

class SqlPlugin(Plugin):
  def dump(self) -> str:
    onces_top_idx = []
    onces_before_idx = []
    onces_after_idx = []
    onces_bottom_idx = []
    types_idx = {}
    for t in self.db.types:
      types_idx[t.name] = t
    top = []
    before = []
    creates = []
    after = []
    bottom = []
    fk = None
    pk = None
    for t in self.db.tables:
      create = []
      for f in t.fields:
        field = Field(**f)
        if 'type' in f and not isinstance(f['type'], dict):
          kind = types_idx[f['type']]
        else:
          fk_table = Table(**f['type'])
          fk = find_key(types_idx, Table(**f['type']))
          kind = types_idx[fk.field.type]

        if kind:
          if not isinstance(kind.top, types.GenericAlias):
            top = [*top, *kind.top]
          elif not isinstance(kind.before, types.GenericAlias):
            before = [*before, *kind.before]
          elif not isinstance(kind.after, types.GenericAlias):
            after = [*after, *kind.after]
          elif not isinstance(kind.bottom, types.GenericAlias):
            bottom = [*bottom, *kind.bottom]
            
          if not isinstance(kind.top_once, types.GenericAlias):
            onces_top_idx = [*top, *kind.top_once]
          elif not isinstance(kind.before_once, types.GenericAlias):
            onces_before_idx = [*top, *kind.before_once]
          elif not isinstance(kind.after_once, types.GenericAlias):
            onces_after_idx = [*top, *kind.after_once]
          elif not isinstance(kind.bottom_once, types.GenericAlias):
            onces_bottom_idx = [*top, *kind.bottom_once]
        if fk:
          inline = f"{fk.type.fk} REFERENCES {fk.table}({fk.field.name})"
        else:
          inline = kind.inline if isinstance(kind, Type) else kind
        if field.pk:
          inline = f"{inline} PRIMARY KEY"
        create.append(f"{f["name"]} {inline}")
      creates.append(f"CREATE TABLE {t.name} (")
      creates.append(f"  {",\n  ".join(create)}")
      creates.append(");")
    
    return "\n".join([*onces_top_idx, *top]) + \
          "\n".join([i for i in itertools.chain(onces_before_idx, before)]) + \
          "\n".join(creates) + \
          "\n".join([i for i in itertools.chain(onces_after_idx, after)]) + \
          "\n".join([i for i in itertools.chain(onces_bottom_idx, bottom)])
          
def find_key(types_idx, table: Table) -> Optional[ForeignKey]:
  for field in table.fields:
    if field.pk:
      return ForeignKey(types_idx[field.type], table.name, field)
  return None
def fk_dictionary(field):
  type = field.type
  inline = type.fk if isinstance(type, Type) else type
  return inline