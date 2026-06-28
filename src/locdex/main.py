import argparse
import sys
from .local_model import run_local_with_confidence

def chat_loop():
    print("Welcome to Locdex Mode A (Interactive Chat). Type 'exit' or 'quit' to leave.")
    print("Type 'ship it' when you are ready to open a PR.\n")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'ship it':
                print("[validator: tests ✓  lint ✓  AI safety review ✓] (Placeholder)")
                print("✓ Opened PR (Placeholder)\n")
                continue
                
            print("[router: routing to local model...]")
            
            # Call the local model wrapper
            result = run_local_with_confidence(user_input, system="You are a focused coding assistant. Output raw code.")
            
            print(f"[confidence: {result['confidence']}]")
            print("✓ Here's the change:")
            print(result['diff'])
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

def cli():
    parser = argparse.ArgumentParser(description="Locdex: Local-First Coding Agent")
    subparsers = parser.add_subparsers(dest="command")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start an interactive coding session")

    args = parser.parse_args()

    if args.command == "chat":
        chat_loop()
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()