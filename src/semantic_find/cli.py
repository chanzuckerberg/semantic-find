"""Console script for semantic_find."""
import argparse
import semantic_find

def main():
    """Console script for semantic_find."""
    parser = argparse.ArgumentParser(description="Console script for semantic_find.")
    
    # Adding subcommands: 'search' and 'insert'
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    
    # Subcommand for search
    search_parser = subparsers.add_parser("search", help="Search for a query")
    search_parser.add_argument("query", type=str, help="Query to search for")
    
    # Subcommand for insert
    insert_parser = subparsers.add_parser("insert", help="Insert a new entry")
    
    args = parser.parse_args()

    # Handling the commands
    if args.command == "search":
        semantic_find.search(args.query)
    elif args.command == "insert":
        semantic_find.insert3()
    

if __name__ == "__main__":
    main()