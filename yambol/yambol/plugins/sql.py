from yambol.plugin import Plugin
import itertools
import sys
from yambol.db_types import Table, ForeignKey, Type, Field, Database
from typing import Optional, List, Dict, Any

class SqlPlugin(Plugin):
    def __init__(self, db: Database) -> None:
        super().__init__(db)

    def dump(self) -> str:
        self._initialize_dump_vars()
        self._generate_sql_parts()
        return self._build_sql_output()

    def _initialize_dump_vars(self) -> None:        
        """Initialize variables for SQL generation."""
        self.onces_ = {
            "top": [f"CREATE DATABASE \"{self.db.name}\";"],
            "before": [],
            "after": [],
            "bottom": []
        }
        self.sql_sections = {
            "top": [],
            "before": [],
            "creates": [],
            "after": [],
            "bottom": []
        }

    def _generate_sql_parts(self) -> None:
        """Generate SQL parts from tables and their fields."""
        for table in self.db.tables:
            create_statements: List[str] = []
            for field in table.fields:
                inline_def = self._get_inline_definition(field)
                create_statements.append(
                    f"\"{field.name}\" {inline_def}"
                )
            
            self._add_create_table(table.name, create_statements)
            
    def _find_key(self, table: Table) -> Optional[ForeignKey]:
        """Find the primary key for a given table."""
        for field in table.fields:
            if isinstance(field, Field):
                return ForeignKey(
                    table=table.name,
                    field=field,
                    type=field.type
                )
        return None
    
    def _handle_kind_directives(self, kind: Type) -> None:
        """Handle directives from the kind (Type)."""
        for directive in ["top", "before", "after", "bottom"]:
            if getattr(kind, directive):
                data = getattr(kind, directive)
                if isinstance(data, list):
                    self.onces_[directive].append(data)
                
    
    def _get_inline_definition(self, field) -> str:
        """Get the inline definition for a field."""
        inline_def = ""
        if isinstance(field, Field):
            f_type = field.type.inline if isinstance(field.type, Type) else field.type
            inline_def += f" {f_type}"
            if not field.nullable:
                inline_def += " NOT NULL"
            if field.unique:
                inline_def += " UNIQUE"
            if field.id:
                inline_def += " PRIMARY KEY"
        else:
            f_type = field.type.fk
            if isinstance(field.field, Field):
                inline_def += f" {f_type} REFERENCES \"{field.table.name}\" (\"{field.field.name}\")"
            else:
                raise AttributeError(f"The foreign key from table {field.table.name} has not been identified.")

        return inline_def.strip()
    
    def _add_create_table(self, table_name: str, fields: List[str]) -> None:
        """Add CREATE TABLE statement to the SQL parts."""
        self.sql_sections["creates"].append(
            f"CREATE TABLE \"{self.db.name}\".\"{table_name}\" (\n    "
            f"{',\n    '.join(fields)}\n"
            f");"
        )
    
    def _build_sql_output(self) -> str:
        """Build the final SQL output string."""
        sections = {
            "top": [ *self.sql_sections["top"], *self.onces_["top"] ],
            "before": [ *self.sql_sections["before"], *self.onces_["before"] ],
            "creates": [ *self.sql_sections["creates"] ],
            "after": [ *self.sql_sections["after"], *self.onces_["after"] ],
            "bottom": [ *self.sql_sections["bottom"], *self.onces_["bottom"] ]
        }
        return "\n\n".join([
            "\n".join(sections[section])
            for section in ["top", "before", "creates", "after", "bottom"]
        ])