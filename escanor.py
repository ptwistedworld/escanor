#!/usr/bin/env python3
"""
Escanor - Advanced Purple Teaming Framework
Main entry point for the framework
"""

import sys
import argparse
from core.interactive_shell import InteractiveShell
from core.module_manager import ModuleManager
from core.playbook_engine import PlaybookEngine
from lib.ai_integration import AIIntegration


def print_banner():
    """Display the Escanor banner"""
    banner = r"""
  ______     __  __     ______     __   __     ______     ______    
 /\  ___\   /\ \/\ \   /\  __ \   /\ "-.\ \   /\  __ \   /\  _  \   
 \ \ \____  \ \ \_\ \  \ \  __ \  \ \ \-.  \  \ \  __ \  \ \ \L\ \  
  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_\ \_\  \ \____ \ 
   \/_____/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_/\/_/   \/___L\ \
                                                             /\____/
                                                             \_/__/ 
           Advanced Purple Teaming Framework v1.0
           Powered by AI | Modular | Extensible
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description="Escanor - Advanced Purple Teaming Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  escanor                    # Launch interactive shell
  escanor --module web_scan  # Run specific module
  escanor --playbook recon   # Execute reconnaissance playbook
  escanor --ai "analyze target"  # AI-assisted operation
        """
    )
    
    parser.add_argument('--module', '-m', type=str, help='Run a specific module')
    parser.add_argument('--playbook', '-p', type=str, help='Execute a playbook')
    parser.add_argument('--ai', '-a', type=str, help='AI-assisted command')
    parser.add_argument('--list-modules', action='store_true', help='List all available modules')
    parser.add_argument('--list-playbooks', action='store_true', help='List all available playbooks')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize core components
    module_manager = ModuleManager()
    playbook_engine = PlaybookEngine(module_manager)
    ai_integration = AIIntegration()
    
    if args.list_modules:
        print_banner()
        print("\n[+] Available Modules:")
        modules = module_manager.list_modules()
        for category, mods in modules.items():
            print(f"\n  {category.upper()}:")
            for mod in mods:
                print(f"    - {mod}")
        return
    
    if args.list_playbooks:
        print_banner()
        print("\n[+] Available Playbooks:")
        playbooks = playbook_engine.list_playbooks()
        for pb in playbooks:
            print(f"  - {pb}")
        return
    
    if args.module:
        module_manager.run_module(args.module, verbose=args.verbose)
        return
    
    if args.playbook:
        playbook_engine.execute_playbook(args.playbook, verbose=args.verbose)
        return
    
    if args.ai:
        result = ai_integration.process_command(args.ai)
        print(f"\n[AI Response]: {result}")
        return
    
    # Default: Launch interactive shell
    print_banner()
    
    shell = InteractiveShell(module_manager, playbook_engine, ai_integration)
    shell.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
