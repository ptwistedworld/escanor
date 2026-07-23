"""
Escanor Module: EDRSilencer Integration
Integrates with EDRSilencer for EDR/AV evasion techniques.
Provides capabilities to test and bypass endpoint detection responses.
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from core.base_module import BaseModule
from core.module_result import ModuleResult


class EDRSilencerModule(BaseModule):
    """
    Module to interface with EDRSilencer framework.
    Requires EDRSilencer to be installed and configured separately.
    """

    def __init__(self):
        super().__init__()
        self.name = "edrsilencer"
        self.display_name = "EDRSilencer Integration"
        self.description = "Interface with EDRSilencer for EDR/AV evasion and bypass testing"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.category = "evasion"
        self.tags = ["evasion", "edr", "av", "bypass", "silencer"]
        self.requirements = [
            "EDRSilencer installed (https://github.com/netero1010/EDRSilencer)",
            "Windows target environment (for actual testing)",
            "Administrative privileges on test systems"
        ]
        
        # Configuration options
        self.options = {
            "edrsilencer_path": {
                "value": "/opt/EDRSilencer",
                "required": True,
                "description": "Path to EDRSilencer installation directory"
            },
            "technique": {
                "value": "unhooking",
                "required": False,
                "description": "Evasion technique to apply (unhooking, patching, etc.)"
            },
            "target_process": {
                "value": "",
                "required": False,
                "description": "Target process name for evasion"
            },
            "output_format": {
                "value": "json",
                "required": False,
                "description": "Output format (json, text)"
            }
        }

    def check_requirements(self) -> bool:
        """Check if EDRSilencer is installed and accessible."""
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            
            if not os.path.exists(edrsilencer_path):
                self.log_error(f"EDRSilencer not found at {edrsilencer_path}")
                return False
            
            # Check for main scripts/binaries
            possible_executables = [
                os.path.join(edrsilencer_path, "EDRSilencer.py"),
                os.path.join(edrsilencer_path, "edrsilencer.py"),
                os.path.join(edrsilencer_path, "bin", "EDRSilencer"),
                os.path.join(edrsilencer_path, "EDRSilencer.exe")
            ]
            
            executable_found = False
            for exe in possible_executables:
                if os.path.exists(exe):
                    executable_found = True
                    self.log_info(f"Found EDRSilencer executable: {exe}")
                    break
            
            if not executable_found:
                self.log_warning("No EDRSilencer executable found, but path exists")
                self.log_info("Will attempt to use available scripts")
            
            self.log_info("EDRSilencer installation verified")
            return True
            
        except Exception as e:
            self.log_error(f"Requirement check failed: {str(e)}")
            return False

    def run(self) -> ModuleResult:
        """Execute EDRSilencer operations - list available techniques."""
        result = ModuleResult()
        
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            
            # Look for Python scripts
            python_scripts = []
            for file in os.listdir(edrsilencer_path):
                if file.endswith(".py") and not file.startswith("__"):
                    python_scripts.append(file)
            
            # Look for technique directories
            technique_dirs = []
            for item in os.listdir(edrsilencer_path):
                item_path = os.path.join(edrsilencer_path, item)
                if os.path.isdir(item_path) and item.lower() in ["techniques", "modules", "methods"]:
                    technique_dirs.append(item)
                    # List files in technique directory
                    tech_files = os.listdir(item_path)
                    self.log_info(f"Found technique directory '{item}' with {len(tech_files)} items")
            
            result.success = True
            result.data = {
                "python_scripts": python_scripts,
                "technique_directories": technique_dirs,
                "message": f"Found {len(python_scripts)} scripts and {len(technique_dirs)} technique directories"
            }
            
            self.log_success("Successfully accessed EDRSilencer")
            self.log_info(f"Available scripts: {', '.join(python_scripts[:10])}")
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"EDRSilencer operation failed: {str(e)}")
        
        return result

    def apply_technique(self, technique_name: str, target_process: str = None) -> ModuleResult:
        """Apply a specific EDR evasion technique."""
        result = ModuleResult()
        
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            output_format = self.get_option("output_format")
            
            # Search for the technique script
            technique_script = None
            for root, dirs, files in os.walk(edrsilencer_path):
                for file in files:
                    if file.endswith(".py") and technique_name.lower() in file.lower():
                        technique_script = os.path.join(root, file)
                        break
                if technique_script:
                    break
            
            if not technique_script:
                # Try to find in common locations
                possible_paths = [
                    os.path.join(edrsilencer_path, f"{technique_name}.py"),
                    os.path.join(edrsilencer_path, "techniques", f"{technique_name}.py"),
                    os.path.join(edrsilencer_path, "modules", f"{technique_name}.py")
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        technique_script = path
                        break
            
            if not technique_script or not os.path.exists(technique_script):
                result.success = False
                result.error = f"Technique script not found: {technique_name}"
                self.log_error(f"Could not find technique: {technique_name}")
                return result
            
            # Build command
            cmd = ["python3", technique_script]
            
            if target_process:
                cmd.extend(["--process", target_process])
            
            if output_format == "json":
                cmd.extend(["--format", "json"])
            
            # Execute
            self.log_info(f"Executing technique: {technique_script}")
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=edrsilencer_path
            )
            
            if process.returncode == 0:
                result.success = True
                result.data = {
                    "technique": technique_name,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "target_process": target_process,
                    "message": f"Technique '{technique_name}' executed successfully"
                }
                self.log_success(f"Technique '{technique_name}' applied successfully")
                
                if process.stdout:
                    self.log_info(f"Output: {process.stdout[:500]}")
            else:
                result.success = False
                result.error = process.stderr
                self.log_error(f"Technique execution failed: {process.stderr}")
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Technique execution timed out"
            self.log_error("EDRSilencer technique timed out")
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to apply technique: {str(e)}")
        
        return result

    def test_evasion(self, payload_type: str = "shellcode", techniques: List[str] = None) -> ModuleResult:
        """Test evasion capabilities against a simulated payload."""
        result = ModuleResult()
        
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            techniques = techniques or ["unhooking", "patching", "direct_syscall"]
            
            self.log_info(f"Testing evasion for payload type: {payload_type}")
            self.log_info(f"Techniques to test: {', '.join(techniques)}")
            
            evasion_results = {}
            
            for technique in techniques:
                technique_result = self.apply_technique(technique)
                evasion_results[technique] = {
                    "success": technique_result.success,
                    "error": technique_result.error,
                    "data": technique_result.data
                }
                
                if technique_result.success:
                    self.log_success(f"Technique '{technique}' test passed")
                else:
                    self.log_warning(f"Technique '{technique}' test failed: {technique_result.error}")
            
            result.success = True
            result.data = {
                "payload_type": payload_type,
                "techniques_tested": evasion_results,
                "summary": {
                    "total": len(techniques),
                    "successful": sum(1 for t in evasion_results.values() if t["success"]),
                    "failed": sum(1 for t in evasion_results.values() if not t["success"])
                },
                "message": f"Tested {len(techniques)} evasion techniques"
            }
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Evasion testing failed: {str(e)}")
        
        return result

    def generate_evasive_payload(self, payload_type: str = "shellcode", encoding: str = "base64") -> ModuleResult:
        """Generate an evasive payload using EDRSilencer techniques."""
        result = ModuleResult()
        
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            
            # Look for payload generation scripts
            payload_scripts = []
            for root, dirs, files in os.walk(edrsilencer_path):
                for file in files:
                    if file.endswith(".py") and any(keyword in file.lower() for keyword in ["payload", "generate", "shellcode"]):
                        payload_scripts.append(os.path.join(root, file))
            
            if not payload_scripts:
                result.success = False
                result.error = "No payload generation scripts found in EDRSilencer"
                self.log_error("Could not find payload generation capability")
                return result
            
            # Use the first available payload script
            payload_script = payload_scripts[0]
            self.log_info(f"Using payload script: {payload_script}")
            
            cmd = ["python3", payload_script, "--type", payload_type, "--encoding", encoding]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=edrsilencer_path
            )
            
            if process.returncode == 0:
                result.success = True
                result.data = {
                    "payload_type": payload_type,
                    "encoding": encoding,
                    "payload": process.stdout,
                    "message": f"Generated {payload_type} payload with {encoding} encoding"
                }
                self.log_success(f"Generated evasive payload: {payload_type}")
            else:
                result.success = False
                result.error = process.stderr
                self.log_error(f"Payload generation failed: {process.stderr}")
            
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = "Payload generation timed out"
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to generate payload: {str(e)}")
        
        return result

    def list_techniques(self) -> ModuleResult:
        """List all available EDR evasion techniques."""
        result = ModuleResult()
        
        try:
            edrsilencer_path = self.get_option("edrsilencer_path")
            
            techniques = []
            
            # Scan for technique files
            for root, dirs, files in os.walk(edrsilencer_path):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        # Extract technique name from filename
                        technique_name = file.replace(".py", "")
                        
                        # Try to read description from file
                        file_path = os.path.join(root, file)
                        description = ""
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read(1000)
                                # Look for docstring
                                if '"""' in content:
                                    start = content.find('"""') + 3
                                    end = content.find('"""', start)
                                    if end > start:
                                        description = content[start:end].strip().split('\n')[0]
                        except:
                            pass
                        
                        techniques.append({
                            "name": technique_name,
                            "file": file,
                            "path": file_path,
                            "description": description
                        })
            
            result.success = True
            result.data = {
                "techniques": techniques,
                "count": len(techniques),
                "message": f"Found {len(techniques)} available techniques"
            }
            
            self.log_info(f"Available EDR evasion techniques: {len(techniques)}")
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to list techniques: {str(e)}")
        
        return result
