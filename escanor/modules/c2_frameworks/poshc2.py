"""
Escanor Module: PoshC2 Integration
Integrates with Nettitude PoshC2 framework for PowerShell and C# post-exploitation.
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from core.base_module import BaseModule
from core.module_result import ModuleResult


class PoshC2Module(BaseModule):
    """
    Module to interface with PoshC2 framework.
    Requires PoshC2 to be installed and configured separately.
    """

    def __init__(self):
        super().__init__()
        self.name = "poshc2"
        self.display_name = "PoshC2 Integration"
        self.description = "Interface with Nettitude PoshC2 for PowerShell and C# post-exploitation operations"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.category = "c2_frameworks"
        self.tags = ["c2", "poshc2", "powershell", "post-exploitation", "dotnet"]
        self.requirements = [
            "PoshC2 installed (https://github.com/nettitude/PoshC2)",
            "PoshC2 database accessible",
            "Python sqlite3 library"
        ]
        
        # Configuration options
        self.options = {
            "poshc2_database": {
                "value": "/var/lib/poshc2/poshc2.db",
                "required": True,
                "description": "Path to PoshC2 SQLite database"
            },
            "poshc2_dir": {
                "value": "/opt/PoshC2",
                "required": False,
                "description": "PoshC2 installation directory"
            },
            "implant_id": {
                "value": "",
                "required": False,
                "description": "Specific implant ID to target"
            },
            "command": {
                "value": "",
                "required": False,
                "description": "Command to execute on implant"
            }
        }

    def check_requirements(self) -> bool:
        """Check if PoshC2 database is accessible."""
        try:
            import sqlite3
            db_path = self.get_option("poshc2_database")
            
            if not os.path.exists(db_path):
                self.log_error(f"PoshC2 database not found at {db_path}")
                return False
            
            # Try to connect and query
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            self.log_info(f"Found {len(tables)} tables in PoshC2 database")
            return True
            
        except ImportError:
            self.log_error("sqlite3 library not available")
            return False
        except Exception as e:
            self.log_error(f"Cannot access PoshC2 database: {str(e)}")
            return False

    def run(self) -> ModuleResult:
        """Execute PoshC2 operations."""
        result = ModuleResult()
        
        try:
            import sqlite3
            
            db_path = self.get_option("poshc2_database")
            implant_id = self.get_option("implant_id")
            
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all implants
            cursor.execute("SELECT * FROM implants ORDER BY last_seen DESC")
            implants = [dict(row) for row in cursor.fetchall()]
            
            # Get tasks
            cursor.execute("SELECT * FROM tasks ORDER BY timestamp DESC LIMIT 50")
            tasks = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            result.success = True
            result.data = {
                "implants": implants,
                "tasks": tasks,
                "message": f"Connected to PoshC2. Found {len(implants)} implants."
            }
            
            self.log_success(f"Successfully connected to PoshC2")
            self.log_info(f"Active Implants: {len(implants)}")
            
            if implant_id:
                # Filter for specific implant
                matching_implants = [i for i in implants if str(i.get('id', '')) == implant_id]
                if matching_implants:
                    self.log_info(f"Target implant {implant_id} found")
                    result.data["target_implant"] = matching_implants[0]
                else:
                    self.log_warning(f"Implant {implant_id} not found")
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"PoshC2 operation failed: {str(e)}")
        
        return result

    def execute_command(self, implant_id: str, command: str) -> ModuleResult:
        """Queue a command for execution on a specific implant."""
        result = ModuleResult()
        
        try:
            import sqlite3
            from datetime import datetime
            
            db_path = self.get_option("poshc2_database")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if implant exists
            cursor.execute("SELECT id FROM implants WHERE id = ?", (implant_id,))
            if not cursor.fetchone():
                result.success = False
                result.error = f"Implant {implant_id} not found"
                conn.close()
                return result
            
            # Insert task
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO tasks (implant_id, command, timestamp, executed) VALUES (?, ?, ?, 0)",
                (implant_id, command, timestamp)
            )
            conn.commit()
            conn.close()
            
            result.success = True
            result.data = {
                "implant_id": implant_id,
                "command": command,
                "timestamp": timestamp,
                "message": f"Command queued for implant {implant_id}"
            }
            self.log_success(f"Command queued for implant {implant_id}: {command}")
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to queue command: {str(e)}")
        
        return result

    def generate_payload(self, payload_type: str = "powershell", options: Dict = None) -> ModuleResult:
        """Generate a PoshC2 payload using the PoshC2 CLI."""
        result = ModuleResult()
        
        try:
            poshc2_dir = self.get_option("poshc2_dir")
            payload_script = os.path.join(poshc2_dir, "PayloadGeneration.py")
            
            if not os.path.exists(payload_script):
                # Try alternative path
                payload_script = subprocess.check_output(
                    ["which", "posh-c2"], 
                    stderr=subprocess.DEVNULL, 
                    text=True
                ).strip()
                
            if not payload_script or not os.path.exists(payload_script):
                result.success = False
                result.error = "PoshC2 payload generation script not found"
                return result
            
            # Build command
            cmd_options = options or {}
            cmd = ["python3", payload_script, "-p", payload_type]
            
            for key, value in cmd_options.items():
                cmd.extend([f"--{key}", str(value)])
            
            # Execute
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if process.returncode == 0:
                result.success = True
                result.data = {
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "message": f"Payload generated successfully"
                }
                self.log_success("Payload generated successfully")
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
            self.log_error(f"Payload generation failed: {str(e)}")
        
        return result

    def get_implant_history(self, implant_id: str = None) -> ModuleResult:
        """Retrieve command history for an implant."""
        result = ModuleResult()
        
        try:
            import sqlite3
            
            db_path = self.get_option("poshc2_database")
            
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if implant_id:
                cursor.execute(
                    "SELECT * FROM tasks WHERE implant_id = ? ORDER BY timestamp DESC",
                    (implant_id,)
                )
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY timestamp DESC LIMIT 100")
            
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            result.success = True
            result.data = {
                "tasks": tasks,
                "count": len(tasks),
                "message": f"Retrieved {len(tasks)} tasks"
            }
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Failed to retrieve task history: {str(e)}")
        
        return result
