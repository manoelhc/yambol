from yambol import parser
from yambol.plugins.sql import SqlPlugin
import sys

def main():
  db = parser.parse(sys.argv[1])
  SqlPlugin(db).dump()
  
main()