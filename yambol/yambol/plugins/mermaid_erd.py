from typing import Optional, List
from yambol.db_types import Database, Table, Field, ForeignKey, Type

class MermaidERDPlugin:
    def __init__(self, db: Database):
        self.db = db
        self.erd_parts = []

    def _find_primary_key(self, table: Table) -> Optional[Field]:
        for field in table.fields:
            if isinstance(field, Field) and field.name == "id":
                return field
        return None

    def _get_table_relationships(self, table: Table) -> List[str]:
        relationships = []
        for field_config in table.fields:
            if 'type' in field_config and isinstance(field_config['type'], dict):
                related_table_name = field_config['type']['name']
                relationships.append(related_table_name)
        return relationships

    def _add_table_to_erd(self, table: Table) -> None:
        table_def = f"  {table.name}"+ "{\n"
        relationship = ""
        for field in table.fields:
            if isinstance(field, Field):
                table_def += f"    {field.type.name.lower()} {field.name}\n"
            else:
                relationship += f"  {table.name} ||--o" + '{ ' + f"{field.table.name} : {field.field.name}\n"
                table_def += f"    {field.type.name.lower()} {field.name}\n"

        table_def += "  }\n"
        self.erd_parts.append(relationship + table_def)

    def _get_foreign_table(self, current_table: Table, field: Field) -> str:
        for rel_table in self.db.tables:
            if rel_table.name != current_table.name and any(f.name == field.foreign_key for f in rel_table.fields):
                return rel_table.name
        return ""

    def _add_relationships_to_erd(self) -> None:
        relationships = []
        for table in self.db.tables:
            for field_config in table.fields:
                if isinstance(field_config.type, Field):
                    related_tables = self._get_table_relationships(table)
                    for rel_table in related_tables:
                        relationship_line = f"  {table.name} " + "}o--||{{" + f" {rel_table} : \"has many\"\n"
                        relationships.append(relationship_line)

        # Remove duplicate relationships
        unique_relationships = list(set(relationships))
        self.erd_parts.extend(unique_relationships)

    def dump(self) -> str:
        for table in self.db.tables:
            self._add_table_to_erd(table)
        self._add_relationships_to_erd()

        # Combine all parts into the final ERD
        return f"---\ntitle: {self.db.name}\n---\n" + \
                "erDiagram\n" + "\n".join(self.erd_parts)