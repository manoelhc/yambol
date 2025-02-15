from yambol.plugin import Plugin

class SqlPlugin(Plugin):
  def dump(self) -> str:
    onces_top_idx = {}
    onces_before_idx = {}
    onces_after_idx = {}
    onces_bottom_idx = {}
    types_idx = {}
    for t in self.db.types:
      types_idx[t.name] = t
    top = []
    before = []
    creates = []
    after = []
    bottom = []
    for t in self.db.tables:
      create = []
      for f in t.fields:
        print(f)
        custype = f['type'] if 'type' in f else f.type.name

        kind = types_idx[custype]
        if kind.top:
          top = [*top, *kind.top]
        elif kind.before:
          before += kind.before
        elif kind.after:
          after += kind.after
        elif kind.bottom:
          bottom += kind.bottom
          
        if kind.top_once and kind.name not in onces_top_idx:
          onces_top_idx[kind.name] = kind.top_once
        elif kind.before_once and kind.name not in onces_before_idx:
          onces_before_idx[kind.name] = kind.before_once
        elif kind.onces_after and kind.name not in onces_after_idx:
          onces_after_idx[kind.name] = kind.onces_after
        elif kind.onces_bottom and kind.name not in onces_bottom_idx:
          onces_bottom_idx[kind.name] = kind.onces_bottom
          
        create.append(f"{f["name"]} {kind.inline}")
      creates.append(f"CREATE TABLE {t.name} (")
      creates.append(f"  {",\n  ".join(create)}")
      creates.append(");")
    
    return "\n".join([*onces_top_idx, *top]) + \
          "\n".join([*onces_before_idx, *before]) + \
          "\n".join(creates) + \
          "\n".join([*onces_after_idx, *after]) + \
          "\n".join([*onces_bottom_idx, *bottom])