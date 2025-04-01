from yambol import parser
from yambol.plugins.sql import SqlPlugin
from yambol.plugins.mermaid_erd import MermaidERDPlugin
from yambol.plugins.ai_readme import AiReadme
import sys
from pprint import pp
import argparse



def main():
  p = argparse.ArgumentParser()
  p.add_argument('filename', help='File name')
  p.add_argument('-o', '--output', help='Output format: SQL, mermaid, Debug, markdown')
  
  args = p.parse_args()
  
  db = parser.parse(args.filename)
  if args.output is None or args.output.lower() == 'debug':
    pp(db)
  elif args.output.lower() == 'mermaid':
    print(MermaidERDPlugin(db).dump())
  elif args.output.lower() == 'sql':
    print(SqlPlugin(db).dump())
  elif args.output.lower() == 'markdown':
    print(AiReadme(db).dump())
  
  
main()