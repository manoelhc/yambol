from yambol.db_types import Database

class Plugin:
  def __init__(self, db: Database):
    self.db = db
  def dump(self) -> str:
    pass