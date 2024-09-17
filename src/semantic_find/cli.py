"""Console script for semantic_find."""
import argparse
import semantic_find

def main():
    """Console script for semantic_find."""
    parser = argparse.ArgumentParser(description="Console script for semantic_find.")
    # Add arguments here, for example:
    # parser.add_argument('arg_name', type=str, help='Description of the argument')

    parser.add_argument("query", type=str, help="Query to search for")

    args = parser.parse_args()
    semantic_find.search(args.query)
    

if __name__ == "__main__":
    main()