#!/usr/bin/env python3
"""
Interactive Shell
Provides the main command-line interface for Escanor
"""

import sys
import shlex
from typing import Optional, Dict, Any
from core.module_manager import ModuleManager
from core.playbook_engine import PlaybookEngine
from lib.ai_integration import AIIntegration


class InteractiveShell:
    """Interactive command shell for Escanor"""
    
    def __init__(self, module_manager: ModuleManager, 
                 playbook_engine: PlaybookEngine,
                 ai_integration: AIIntegration):
        self.module_manager = module_manager
        self.playbook_engine = playbook_engine
        self.ai_integration = ai_integration
        self.current_module: Optional[str] = None
        self.prompt_prefix = "escanor"
        self.running = True
    
    def start(self) -> None:
        """Start the interactive shell"""
        print("\n[+] Starting Escanor Interactive Shell")
        print("[+] Type 'help' for available commands\n")
        
        while self.running:
            try:
                prompt = self._build_prompt()
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                self._process_command(command)
                
            except KeyboardInterrupt:
                print("\n[!] Use 'exit' to quit or Ctrl+D")
            except EOFError:
                print("\n[+] Exiting...")
                break
            except Exception as e:
                print(f"[!] Error: {e}")
    
    def _build_prompt(self) -> str:
        """Build the command prompt"""
        if self.current_module:
            return f"\033[1;31m{self.prompt_prefix}\033[0m:\033[1;34m{self.current_module}\033[0m> "
        return f"\033[1;31m{self.prompt_prefix}\033[0m> "
    
    def _process_command(self, command: str) -> None:
        """Process a user command"""
        parts = shlex.split(command)
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            'help': self._cmd_help,
            'use': self._cmd_use,
            'run': self._cmd_run,
            'set': self._cmd_set,
            'show': self._cmd_show,
            'back': self._cmd_back,
            'list': self._cmd_list,
            'playbook': self._cmd_playbook,
            'ai': self._cmd_ai,
            'reload': self._cmd_reload,
            'exit': self._cmd_exit,
            'quit': self._cmd_exit,
            'info': self._cmd_info,
            'execute': self._cmd_execute,
            'search': self._cmd_search,
            'banner': self._cmd_banner,
        }
        
        if cmd in commands:
            commands[cmd](args)
        else:
            print(f"[!] Unknown command: {cmd}. Type 'help' for assistance.")
    
    def _cmd_help(self, args: list) -> None:
        """Show help information"""
        help_text = """
Escanor Interactive Shell Commands
========================================

Core Commands:
  help              Show this help message
  use <module>      Select a module to use
  run               Execute the current module
  execute <module> [opts]  Run a module directly without loading (one-liner)
  set <opt> <val>   Set a module option
  show [options]    Show module options or info
  back              Deselect current module
  info              Show current module information

Module Management:
  list [category]   List modules (optionally by category)
  search <term>     Search modules by name or description
  reload            Reload all modules

Playbooks:
  playbook <name>   Execute a playbook
  playbook list     List available playbooks

AI Integration:
  ai <query>        Run AI-assisted command

Display:
  banner            Redisplay the Escanor banner

Session:
  exit/quit         Exit the framework

Examples:
  use reconnaissance/port_scan
  set TARGET 192.168.1.1
  set PORTS 1-1000
  run
  execute exploitation/privesc/godpotato cmd="whoami"
  search potato
  ai "suggest next steps for target 192.168.1.1"
        """
        print(help_text)
    
    def _cmd_use(self, args: list) -> None:
        """Select a module to use"""
        if not args:
            print("[!] Usage: use <module_name>")
            return
        
        module_name = args[0]
        module = self.module_manager.get_module(module_name)
        
        if module:
            self.current_module = module_name
            print(f"[+] Module loaded: {module.name}")
            print(f"    {module.description}")
        else:
            print(f"[!] Module not found: {module_name}")
            print("[*] Use 'list' to see available modules")
    
    def _cmd_run(self, args: list) -> None:
        """Execute the current module"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        verbose = '-v' in args or '--verbose' in args
        self.module_manager.run_module(self.current_module, verbose=True)
    
    def _cmd_set(self, args: list) -> None:
        """Set a module option"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        if len(args) < 2:
            print("[!] Usage: set <option> <value>")
            return
        
        option = args[0]
        value = ' '.join(args[1:])
        
        module = self.module_manager.get_module(self.current_module)
        if module:
            module.set_option(option, value)
            print(f"[+] {option} => {value}")
        else:
            print(f"[!] Error setting option")
    
    def _cmd_show(self, args: list) -> None:
        """Show module options or information"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        module = self.module_manager.get_module(self.current_module)
        if not module:
            return
        
        if not args or args[0].lower() == 'options':
            print(f"\nModule: {module.name}")
            print(f"Description: {module.description}\n")
            module.show_options()
        elif args[0].lower() == 'info':
            info = module.info()
            print("\nModule Information:")
            for key, value in info.items():
                print(f"  {key.capitalize()}: {value}")
    
    def _cmd_back(self, args: list) -> None:
        """Deselect current module"""
        self.current_module = None
        print("[+] Module deselected")
    
    def _cmd_list(self, args: list) -> None:
        """List available modules"""
        categories = self.module_manager.list_modules()
        
        if args and args[0].lower() in categories:
            # List specific category
            category = args[0].lower()
            print(f"\nModules in {category.upper()}:")
            for mod in categories[category]:
                module = self.module_manager.get_module(f"{category}/{mod}")
                if module:
                    print(f"  - {mod:<25} {module.description}")
        else:
            # List all
            print("\nAvailable Modules by Category:")
            for category, modules in sorted(categories.items()):
                print(f"\n  {category.upper()}:")
                for mod in modules:
                    module = self.module_manager.get_module(f"{category}/{mod}")
                    desc = module.description if module else ""
                    print(f"    - {mod:<25} {desc[:50]}")
    
    def _cmd_playbook(self, args: list) -> None:
        """Execute or list playbooks"""
        if not args:
            print("[!] Usage: playbook <name> or playbook list")
            return
        
        if args[0].lower() == 'list':
            playbooks = self.playbook_engine.list_playbooks()
            print("\nAvailable Playbooks:")
            for pb in playbooks:
                playbook_info = self.playbook_engine.get_playbook_info(pb)
                desc = playbook_info.get('description', '') if playbook_info else ''
                print(f"  - {pb:<25} {desc[:50]}")
        else:
            playbook_name = args[0]
            verbose = '-v' in args or '--verbose' in args
            self.playbook_engine.execute_playbook(playbook_name, verbose=verbose)
    
    def _cmd_ai(self, args: list) -> None:
        """Run AI-assisted command"""
        if not args:
            print("[!] Usage: ai <query>")
            return
        
        query = ' '.join(args)
        print("\n[*] Processing AI request...")
        result = self.ai_integration.process_command(query)
        print(f"\n[AI Response]:\n{result}")
    
    def _cmd_reload(self, args: list) -> None:
        """Reload all modules"""
        self.module_manager.reload_modules()
    
    def _cmd_exit(self, args: list) -> None:
        """Exit the shell"""
        print("\n[+] Shutting down Escanor...")
        self.running = False
    
    def _cmd_info(self, args: list) -> None:
        """Show current module information"""
        if not self.current_module:
            print("[!] No module selected")
            return
        
        module = self.module_manager.get_module(self.current_module)
        if module:
            info = module.info()
            print("\nCurrent Module Information:")
            for key, value in info.items():
                print(f"  {key.capitalize()}: {value}")

    def _cmd_execute(self, args: list) -> None:
        """Execute a module directly without loading it first (one-liner execution)"""
        if not args:
            print("[!] Usage: execute <module_name> [option=value ...]")
            print("    Example: execute exploitation/privesc/godpotato cmd=\"whoami\"")
            return
        
        module_name = args[0]
        module = self.module_manager.get_module(module_name)
        
        if not module:
            print(f"[!] Module not found: {module_name}")
            print("[*] Use 'list' to see available modules or 'search <term>' to find modules")
            return
        
        # Parse additional arguments as options
        options = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                options[key] = value
        
        # Set options on the module
        for opt_name, opt_value in options.items():
            module.set_option(opt_name, opt_value)
        
        print(f"\n[*] Executing module: {module_name}")
        if options:
            print(f"[*] Options: {options}")
        
        # Execute the module
        result = self.module_manager.run_module(module_name, verbose=True)
        
        if result and result.success:
            print("\n[+] Module execution completed successfully")
        elif result:
            print(f"\n[-] Module execution failed: {result.error}")

    def _cmd_search(self, args: list) -> None:
        """Search modules by name or description"""
        if not args:
            print("[!] Usage: search <search_term>")
            return
        
        search_term = ' '.join(args).lower()
        categories = self.module_manager.list_modules()
        
        results = []
        for category, modules in categories.items():
            for mod_name in modules:
                full_name = f"{category}/{mod_name}"
                module = self.module_manager.get_module(full_name)
                
                if module:
                    # Search in name, display_name, description, and category
                    searchable_text = f"{module.name} {module.display_name} {module.description} {module.category}".lower()
                    if search_term in searchable_text:
                        results.append((full_name, module))
        
        if results:
            print(f"\n[+] Found {len(results)} module(s) matching '{search_term}':\n")
            for full_name, module in results:
                print(f"  - {full_name:<40} {module.description[:50]}")
            print()
        else:
            print(f"\n[-] No modules found matching '{search_term}'")

    def _cmd_banner(self, args: list) -> None:
        """Redisplay the Escanor banner"""
        from escanor import print_banner
        print_banner()
