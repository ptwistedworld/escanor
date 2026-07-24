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
            'reports': self._cmd_reports,
            'report': self._cmd_report,
            'action': self._cmd_action,
            'actions': self._cmd_actions,
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
  run [opts]        Execute the current module
                    Options: -v/--verbose, --no-report, --operator <name>, --notes "<text>"
  execute <module> [opts]  Run a module directly without loading (one-liner)
                           Usage: execute mod/name opt1=val1 opt2=val2
  set <opt> <val>   Set a module option
  show [options|actions]  Show module options or available actions
  back              Deselect current module
  info              Show current module information

Fine-Grained Actions:
  action <name>     Select a specific action within the loaded module
  actions           List all available actions in the current module
                    Actions allow precise control over module behavior

Module Management:
  list [category]   List modules (optionally by category)
  search <term>     Search modules by name or description
  reload            Reload all modules

Playbooks:
  playbook <name>   Execute a playbook
  playbook list     List available playbooks

AI Integration (Optional):
  ai <query>        Run AI-assisted command
                    Note: AI requires ESCANOR_AI_* environment variables

Reporting:
  reports           List generated reports
  report <id>       View a specific report

Display:
  banner            Redisplay the Escanor banner

Session:
  exit/quit         Exit the framework

Examples:
  use c2_frameworks/koadic
  actions                        # See available actions
  action generate_stager         # Select specific action
  set STAGER_TYPE js/mshta
  run -v --operator "red.team"
  
  use reconnaissance/port_scan
  set TARGET 192.168.1.1
  set PORTS 1-1000
  run -v --operator "john.doe" --notes "Initial scan"
  
  execute exploitation/privesc/godpotato cmd="whoami"
  search potato
  ai "suggest next steps for target 192.168.1.1"
  list cloud/entra
  playbook purple_team
  
Fine-Grained Attack Control:
  Modules now support multiple actions for precise control
  Example: A C2 module might have actions like:
    - generate_payload: Create a payload
    - start_listener: Start a listener
    - execute_module: Run a module on a zombie
    - list_zombies: List compromised hosts
    
  This allows you to run specific behaviors without running the entire module
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
        no_report = '--no-report' in args
        
        # Parse operator and notes from args
        operator = "unknown"
        notes = ""
        for i, arg in enumerate(args):
            if arg == '--operator' and i + 1 < len(args):
                operator = args[i + 1]
            elif arg == '--notes' and i + 1 < len(args):
                notes = args[i + 1]
        
        self.module_manager.run_module(
            self.current_module, 
            verbose=True,
            write_report=not no_report,
            operator=operator,
            notes=notes
        )
    
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
        """Show module options, actions, or information"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        module = self.module_manager.get_module(self.current_module)
        if not module:
            return
        
        if not args or len(args) == 0:
            # Default to showing options
            print(f"\nModule: {module.name}")
            print(f"Description: {module.description}\n")
            module.show_options()
        elif args[0].lower() == 'options':
            print(f"\nModule: {module.name}")
            print(f"Description: {module.description}\n")
            module.show_options()
        elif args[0].lower() == 'actions':
            module.show_actions()
        elif args[0].lower() == 'info':
            info = module.info()
            print("\nModule Information:")
            for key, value in info.items():
                print(f"  {key.capitalize()}: {value}")
        else:
            print(f"[!] Unknown show argument: {args[0]}")
            print("[*] Use 'show options', 'show actions', or 'show info'")
    
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
        no_report = '--no-report' in args
        operator = "unknown"
        notes = ""
        
        for arg in args[1:]:
            if arg == '--no-report':
                continue
            elif arg == '--operator' and args.index(arg) + 1 < len(args):
                operator = args[args.index(arg) + 1]
            elif arg == '--notes' and args.index(arg) + 1 < len(args):
                notes = args[args.index(arg) + 1]
            elif '=' in arg:
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
        
        # Execute the module with reporting
        result = self.module_manager.run_module(
            module_name, 
            verbose=True,
            write_report=not no_report,
            operator=operator,
            notes=notes
        )
        
        if result and result.get("status") == "success":
            print("\n[+] Module execution completed successfully")
        elif result:
            print(f"\n[-] Module execution failed: {result.get('error', 'Unknown error')}")

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

    def _cmd_reports(self, args: list) -> None:
        """List all generated reports"""
        from utils.result_reporter import get_reporter
        reporter = get_reporter()
        reports = reporter.list_reports()
        
        if not reports:
            print("\n[!] No reports found. Run a module to generate a report.")
            return
        
        print(f"\n{'='*80}")
        print("GENERATED REPORTS")
        print(f"{'='*80}")
        print(f"{'#':<5} {'Filename':<45} {'Size':<12} {'Created'}")
        print(f"{'-'*80}")
        
        for idx, report in enumerate(reports, 1):
            filename = report['filename']
            size = f"{report['size']} bytes"
            created = report['created'][:19]  # Trim to YYYY-MM-DD HH:MM:SS
            print(f"{idx:<5} {filename:<45} {size:<12} {created}")
        
        print(f"\nTotal: {len(reports)} report(s)")
        print("Use 'report <number>' to view a specific report")

    def _cmd_report(self, args: list) -> None:
        """View a specific report"""
        from utils.result_reporter import get_reporter
        reporter = get_reporter()
        reports = reporter.list_reports()
        
        if not reports:
            print("\n[!] No reports found.")
            return
        
        if not args:
            print("\n[!] Usage: report <number>")
            print("    Use 'reports' to list available reports")
            return
        
        try:
            report_num = int(args[0])
            if report_num < 1 or report_num > len(reports):
                print(f"[!] Invalid report number. Must be between 1 and {len(reports)}")
                return
            
            report = reports[report_num - 1]
            
            print(f"\n{'='*80}")
            print(f"VIEWING REPORT: {report['filename']}")
            print(f"{'='*80}\n")
            
            with open(report['path'], 'r', encoding='utf-8') as f:
                print(f.read())
                
        except ValueError:
            print("[!] Invalid report number. Please provide a numeric value.")
        except Exception as e:
            print(f"[!] Error reading report: {e}")

    def _cmd_action(self, args: list) -> None:
        """Select a specific action within the current module"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        if not args:
            print("[!] Usage: action <action_name>")
            print("[*] Use 'actions' to see available actions")
            return
        
        action_name = args[0]
        module = self.module_manager.get_module(self.current_module)
        
        if not module:
            print(f"[!] Module not found: {self.current_module}")
            return
        
        # Try to set the action
        if module.set_action(action_name):
            print(f"[+] Action selected: {action_name}")
            action_def = module.get_action(action_name)
            if action_def:
                print(f"    Description: {action_def.description}")
                if action_def.required_options:
                    print(f"    Required options: {', '.join(action_def.required_options)}")
        else:
            print(f"[!] Action '{action_name}' not found in module '{self.current_module}'")
            print("[*] Available actions:")
            for name, action_def in module.list_actions().items():
                print(f"    - {name}: {action_def.description}")

    def _cmd_actions(self, args: list) -> None:
        """List all available actions in the current module"""
        if not self.current_module:
            print("[!] No module selected. Use 'use <module>' first.")
            return
        
        module = self.module_manager.get_module(self.current_module)
        if not module:
            print(f"[!] Module not found: {self.current_module}")
            return
        
        module.show_actions()
