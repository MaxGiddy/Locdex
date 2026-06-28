import argparse
from .router import route_task

def chat_loop():
    print("Welcome to Locdex Mode A (Interactive Chat). Type 'exit' or 'quit' to leave.")
    print("Type 'ship it' when you are ready to open a PR.\n")
    
    # We will eventually pull thresholds from telemetry. For now, a mock dictionary.
    mock_category_thresholds = {
        ("python", "general"): 2
    }
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'ship it':
                print("[validator: tests ✓  lint ✓  AI safety review ✓] (Placeholder)")
                print("✓ Opened PR (Placeholder)\n")
                continue
                
            print("[router: evaluating task...]")
            
            # The context dictionary will eventually hold file paths, language, etc.
            context = {
                "language": "python",
                "system_prompt": "You are a focused coding assistant. Output raw code."
            }
            
            # Send the input through the Router instead of directly to the model
            routing_result = route_task(
                task=user_input, 
                category="general", 
                context=context, 
                category_thresholds=mock_category_thresholds
            )
            
            source = routing_result.get("source")
            
            if source == "local":
                print(f"[router: local model succeeded on attempt {routing_result['attempts']}... confidence {routing_result['confidence']}]")
                print("✓ Here's the change:")
                print(routing_result["result"]["diff"])
                
            elif source == "failed_local":
                print(f"[router: local model failed. Reason: {routing_result['escalation_reason']}]")
                print(f"[router: escalating to cloud... (Placeholder - Cloud not built yet)]")
                # Show what the local model tried to do before it failed
                print("✗ Best local attempt (Low Confidence):")
                print(routing_result["result"]["diff"])
                
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

def cli():
    parser = argparse.ArgumentParser(description="Locdex: Local-First Coding Agent")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat", help="Start an interactive coding session")

    args = parser.parse_args()

    if args.command == "chat":
        chat_loop()
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()