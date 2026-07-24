"""
Escanor Module: Empire C2 Integration
Integrates with BC-Security Empire Framework for post-exploitation operations.
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from core.base_module import BaseModule, action
from core.module_result import ModuleResult


class EmpireC2Module(BaseModule):
    """
    Module to interface with Empire C2 framework.
    Requires Empire to be installed and configured separately.
    """

    def __init__(self):
        super().__init__()
        self.name = "empire_c2"
        self.display_name = "Empire C2 Integration"
        self.description = "Interface with BC-Security Empire C2 framework for post-exploitation operations"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.category = "c2_frameworks"
        self.tags = ["c2", "empire", "post-exploitation", "powershell"]
        self.requirements = [
            "Empire framework installed (https://github.com/BC-SECURITY/Empire)",
            "Empire RESTful API enabled",
            "Python requests library"
        ]
        
        # Configuration options
        self.options = {
            "empire_host": {
                "value": "localhost",
                "required": False,
                "description": "Empire server host"
            },
            "empire_port": {
                "value": "1337",
                "required": False,
                "description": "Empire REST API port"
            },
            "username": {
                "value": "empireadmin",
                "required": False,
                "description": "Empire API username"
            },
            "password": {
                "value": "password123",
                "required": False,
                "description": "Empire API password"
            },
            "listener_name": {
                "value": "",
                "required": False,
                "description": "Name of the listener to use/create"
            },
            "stager_type": {
                "value": "multi/launcher",
                "required": False,
                "description": "Type of stager to generate"
            }
        }
        
        # Register actions
        self._register_actions()
    
    def _register_actions(self):
        """Register all available actions for this module."""
        
        @action(
            name="connect",
            description="Connect to Empire C2 and retrieve status",
            required_options=["empire_host", "empire_port", "username", "password"],
            tags=["recon", "status"]
        )
        def connect():
            return self._connect_to_empire()
        
        @action(
            name="list_listeners",
            description="List all active Empire listeners",
            required_options=["empire_host", "empire_port", "username", "password"],
            tags=["recon", "listeners"]
        )
        def list_listeners():
            return self._list_listeners()
        
        @action(
            name="list_agents",
            description="List all active Empire agents",
            required_options=["empire_host", "empire_port", "username", "password"],
            tags=["recon", "agents"]
        )
        def list_agents():
            return self._list_agents()
        
        @action(
            name="create_listener",
            description="Create a new Empire listener",
            required_options=["empire_host", "empire_port", "username", "password", "listener_name"],
            tags=["setup", "listener"]
        )
        def create_listener_action():
            name = self.get_option("listener_name")
            listener_type = self.get_option("stager_type") or "http"
            return self.create_listener(name, listener_type)
        
        @action(
            name="generate_stager",
            description="Generate a stager payload for a listener",
            required_options=["empire_host", "empire_port", "username", "password", "listener_name"],
            tags=["payload", "stager"]
        )
        def generate_stager_action():
            listener_name = self.get_option("listener_name")
            stager_type = self.get_option("stager_type") or "multi/launcher"
            return self.generate_stager(listener_name, stager_type)
        
        @action(
            name="execute_command",
            description="Execute a command on a specific agent",
            required_options=["empire_host", "empire_port", "username", "password"],
            tags=["execution", "command"]
        )
        def execute_command_action():
            self.log_warning("This action requires additional implementation based on agent ID")
            result = ModuleResult()
            result.success = False
            result.error = "Agent ID not specified. Use programmatic interface for agent-specific commands."
            return result

    def check_requirements(self) -> bool:
        """Check if Empire is accessible."""
        try:
            import requests
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            url = f"http://{host}:{port}/api/admin/login"
            
            # Try to connect
            response = requests.get(url, timeout=5)
            return response.status_code in [200, 401, 403]
        except ImportError:
            self.log_error("requests library not installed. Run: pip install requests")
            return False
        except Exception as e:
            self.log_error(f"Cannot connect to Empire: {str(e)}")
            return False

    def _connect_to_empire(self) -> ModuleResult:
        """Internal method to connect and get status."""
        result = ModuleResult()
        
        try:
            import requests
            
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            username = self.get_option("username")
            password = self.get_option("password")
            
            base_url = f"http://{host}:{port}"
            
            # Login to get token
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{base_url}/token", data=login_data, timeout=10)
            
            if login_response.status_code != 200:
                result.success = False
                result.error = "Failed to authenticate with Empire"
                result.data = {"status_code": login_response.status_code, "response": login_response.text}
                return result
            
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get listeners
            listeners_response = requests.get(f"{base_url}/api/listeners", headers=headers, timeout=10)
            listeners = listeners_response.json() if listeners_response.status_code == 200 else []
            
            # Get agents
            agents_response = requests.get(f"{base_url}/api/agents", headers=headers, timeout=10)
            agents = agents_response.json() if agents_response.status_code == 200 else []
            
            result.success = True
            result.data = {
                "listeners": listeners,
                "agents": agents,
                "message": f"Connected to Empire. Found {len(listeners)} listeners and {len(agents)} active agents."
            }
            
            self.log_success(f"Successfully connected to Empire C2")
            self.log_info(f"Active Agents: {len(agents)}")
            self.log_info(f"Listeners: {len(listeners)}")
            
        except ImportError:
            result.success = False
            result.error = "requests library not installed"
        except Exception as e:
            result.success = False
            result.error = str(e)
            self.log_error(f"Empire operation failed: {str(e)}")
        
        return result
    
    def _list_listeners(self) -> ModuleResult:
        """List all Empire listeners."""
        result = ModuleResult()
        
        try:
            import requests
            
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            username = self.get_option("username")
            password = self.get_option("password")
            
            base_url = f"http://{host}:{port}"
            
            # Login
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{base_url}/token", data=login_data, timeout=10)
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get listeners
            listeners_response = requests.get(f"{base_url}/api/listeners", headers=headers, timeout=10)
            
            if listeners_response.status_code == 200:
                listeners = listeners_response.json()
                result.success = True
                result.data = {"listeners": listeners, "count": len(listeners)}
                self.log_success(f"Found {len(listeners)} listeners")
            else:
                result.success = False
                result.error = f"Failed to retrieve listeners: {listeners_response.text}"
                
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        return result
    
    def _list_agents(self) -> ModuleResult:
        """List all Empire agents."""
        result = ModuleResult()
        
        try:
            import requests
            
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            username = self.get_option("username")
            password = self.get_option("password")
            
            base_url = f"http://{host}:{port}"
            
            # Login
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{base_url}/token", data=login_data, timeout=10)
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get agents
            agents_response = requests.get(f"{base_url}/api/agents", headers=headers, timeout=10)
            
            if agents_response.status_code == 200:
                agents = agents_response.json()
                result.success = True
                result.data = {"agents": agents, "count": len(agents)}
                self.log_success(f"Found {len(agents)} active agents")
            else:
                result.success = False
                result.error = f"Failed to retrieve agents: {agents_response.text}"
                
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        return result

    def run(self) -> ModuleResult:
        """Execute default Empire operations - connect and show status."""
        return self._connect_to_empire()

    def create_listener(self, name: str, listener_type: str = "http", options: Dict = None) -> ModuleResult:
        """Create a new Empire listener."""
        result = ModuleResult()
        
        try:
            import requests
            
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            username = self.get_option("username")
            password = self.get_option("password")
            
            base_url = f"http://{host}:{port}"
            
            # Login
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{base_url}/token", data=login_data, timeout=10)
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Create listener
            listener_options = options or {
                "Name": name,
                "Host": f"http://{host}",
                "Port": "8080",
                "DefaultProfile": f"/admin/get.php?news.php|/link.php?v={name}"
            }
            
            create_data = {
                "name": name,
                "options": listener_options
            }
            
            response = requests.post(f"{base_url}/api/listeners/{listener_type}", 
                                   json=create_data, 
                                   headers=headers, 
                                   timeout=10)
            
            if response.status_code == 200:
                result.success = True
                result.data = response.json()
                self.log_success(f"Listener '{name}' created successfully")
            else:
                result.success = False
                result.error = f"Failed to create listener: {response.text}"
                
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        return result

    def generate_stager(self, listener_name: str, stager_type: str = "multi/launcher") -> ModuleResult:
        """Generate a stager payload."""
        result = ModuleResult()
        
        try:
            import requests
            
            host = self.get_option("empire_host")
            port = self.get_option("empire_port")
            username = self.get_option("username")
            password = self.get_option("password")
            
            base_url = f"http://{host}:{port}"
            
            # Login
            login_data = {"username": username, "password": password}
            login_response = requests.post(f"{base_url}/token", data=login_data, timeout=10)
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Generate stager
            stager_data = {
                "name": f"{listener_name}_stager",
                "listener": listener_name,
                "language": "python" if "python" in stager_type else "powershell"
            }
            
            response = requests.post(f"{base_url}/api/stagers", 
                                   json=stager_data, 
                                   headers=headers, 
                                   timeout=10)
            
            if response.status_code == 200:
                result.success = True
                result.data = response.json()
                self.log_success(f"Stager generated for listener '{listener_name}'")
            else:
                result.success = False
                result.error = f"Failed to generate stager: {response.text}"
                
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        return result
