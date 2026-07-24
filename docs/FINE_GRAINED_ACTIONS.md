# Fine-Grained Actions Framework

## Overview

The Escanor framework now supports **fine-grained actions** within modules, giving you surgical precision to execute specific behaviors or attacks without running entire module workflows.

### Key Concepts

- **Module**: Container for related functionality (e.g., `empire_c2`, `poshc2`)
- **Action**: Specific behavior you want to execute (e.g., `list_agents`, `generate_stager`)
- **Playbook**: Curated templates orchestrating multiple actions

## Architecture

```
Module (Container)
├── Action 1: list_implants
├── Action 2: execute_command
├── Action 3: generate_payload
└── Action 4: get_history
```

## Usage Examples

### Interactive Shell

```bash
# Load a module
escanor> use c2_frameworks/poshc2

# View available actions
escanor: poshc2> actions

Available Actions:
  [!] action               Description                              Tags
  ────────────────────────────────────────────────────────────────────────
  [+] list_implants        List all active PoshC2 implants          recon, implants
  [+] list_tasks           List recent PoshC2 tasks                 recon, tasks
  [+] execute_command      Queue a command on implant               execution, command
  [+] generate_payload     Generate a PoshC2 payload                payload, generate
  [+] get_history          Get command history                      recon, history

# Select a specific action
escanor: poshc2> action execute_command

# Set required options
escanor: poshc2> set poshc2_database /var/lib/poshc2/poshc2.db
escanor: poshc2> set implant_id ABC123
escanor: poshc2> set command whoami

# Execute only that action
escanor: poshc2> run
```

### Playbook with Actions

```yaml
name: "C2 Operations"
description: "Execute specific C2 actions"

steps:
  - module: "c2_frameworks/poshc2"
    action: "list_implants"  # Specific action
    options:
      poshc2_database: "/var/lib/poshc2/poshc2.db"
  
  - module: "c2_frameworks/poshc2"
    action: "execute_command"
    options:
      poshc2_database: "/var/lib/poshc2/poshc2.db"
      implant_id: "{{implant_id}}"
      command: "whoami"
  
  - module: "c2_frameworks/empire_c2"
    action: "generate_stager"
    options:
      empire_host: "10.0.0.1"
      empire_port: "1337"
      listener_name: "http_listener"
```

### Programmatic Usage

```python
from core.module_manager import ModuleManager

mm = ModuleManager()

# Execute specific action
result = mm.run_module(
    "c2_frameworks/poshc2",
    action="execute_command",  # Specific action
    options={
        "poshc2_database": "/var/lib/poshc2/poshc2.db",
        "implant_id": "ABC123",
        "command": "whoami"
    }
)

print(result.data)
```

## Available Actions by Module

### C2 Frameworks

#### Empire C2 (`c2_frameworks/empire_c2`)
- `connect` - Connect to Empire C2 and retrieve status
- `list_listeners` - List all active Empire listeners
- `list_agents` - List all active Empire agents
- `create_listener` - Create a new Empire listener
- `generate_stager` - Generate a stager payload
- `execute_command` - Execute command on agent

#### PoshC2 (`c2_frameworks/poshc2`)
- `list_implants` - List all active PoshC2 implants
- `list_tasks` - List recent PoshC2 tasks
- `execute_command` - Queue command on implant
- `generate_payload` - Generate PoshC2 payload
- `get_history` - Get command history

#### Koadic (`c2_frameworks/koadic`)
- `list_modules` - List available Koadic modules
- `start_listener` - Start a listener
- `generate_stager` - Generate payloads
- `execute_module` - Execute on zombies
- `list_zombies` - List compromised hosts

### Evasion

#### EDRSilencer (`evasion/edrsilencer`)
- `list_techniques` - List available evasion techniques
- `apply_technique` - Apply specific evasion technique
- `test_evasion` - Test evasion capabilities
- `generate_payload` - Generate evasive payload

### Reconnaissance

#### Port Scanner (`reconnaissance/port_scan`)
- `scan_tcp` - TCP port scan
- `scan_udp` - UDP port scan
- `scan_common` - Scan common ports only
- `identify_services` - Identify services on open ports

#### Web Scanner (`reconnaissance/web_scan`)
- `scan_server` - Scan web server info
- `analyze_headers` - Analyze security headers
- `detect_tech` - Detect web technologies
- `check_ssl` - Check SSL/TLS configuration

#### Vulnerability Scanner (`reconnaissance/vuln_scan`)
- `scan_service` - Scan service for vulns
- `check_cve` - Check specific CVE
- `assess_risk` - Assess overall risk level

### Cloud - Entra ID

#### Service Principal Assessment (`cloud/entra/sp_assessment`)
- `assess_credentials` - Assess SP credentials
- `assess_permissions` - Assess SP permissions
- `assess_managed_identities` - Assess managed identities
- `full_assessment` - Complete assessment

#### Conditional Access Validator (`cloud/entra/ca_validator`)
- `validate_policy` - Validate single policy
- `test_user_access` - Test user access
- `check_misconfigurations` - Check for misconfigs

### Exploitation - Privilege Escalation

#### GodPotato (`exploitation/privesc/godpotato`)
- `escalate` - Execute privilege escalation
- `check_prerequisites` - Check requirements
- `execute_command` - Execute command as SYSTEM

#### PrintSpoofer (`exploitation/privesc/printspoofer`)
- `escalate` - Execute PrintSpoofer
- `interactive` - Run in interactive mode
- `check_spooler` - Check spooler service

## Creating Actions in Your Modules

### Step 1: Import the Action Decorator

```python
from core.base_module import BaseModule, action
```

### Step 2: Register Actions in `__init__`

```python
def __init__(self):
    super().__init__()
    # ... your existing init code ...
    
    # Make options not required by default (actions will specify)
    for opt in self.options.values():
        opt['required'] = False
    
    self._register_actions()

def _register_actions(self):
    """Register all available actions."""
    
    @action(
        name="list_resources",
        description="List all resources",
        required_options=["database_path"],
        tags=["recon", "list"]
    )
    def list_resources():
        return self._list_resources()
    
    @action(
        name="create_resource",
        description="Create a new resource",
        required_options=["database_path", "resource_name"],
        tags=["create", "setup"]
    )
    def create_resource_action():
        name = self.get_option("resource_name")
        return self.create_resource(name)
```

### Step 3: Create Internal Methods

```python
def _list_resources(self) -> ModuleResult:
    """Internal method to list resources."""
    result = ModuleResult()
    # ... implementation ...
    return result

def create_resource(self, name: str) -> ModuleResult:
    """Public method to create resource."""
    result = ModuleResult()
    # ... implementation ...
    return result
```

### Step 4: Update `run()` Method

```python
def run(self) -> ModuleResult:
    """Default behavior when no action specified."""
    return self._list_resources()  # Or any default action
```

## Best Practices

### 1. Action Naming
- Use verb-noun format: `list_agents`, `generate_payload`
- Be specific and descriptive
- Keep names consistent across similar modules

### 2. Required Options
- Only mark options as required at the action level
- Module-level options should be optional
- Each action specifies what it needs

### 3. Tags
- Use consistent tagging: `recon`, `execution`, `payload`, `setup`
- Helps with filtering and search
- Minimum 2 tags per action

### 4. Error Handling
- Return `ModuleResult` from all actions
- Set `success=False` and `error` on failure
- Log appropriately with `log_error`, `log_success`

### 5. Documentation
- Document each action's purpose
- Include example usage
- List required options clearly

## Migration Guide

### Before (Old Style)
```python
class MyModule(BaseModule):
    def __init__(self):
        self.options = {
            "TARGET": {"value": "", "required": True}
        }
    
    def run(self):
        # Does everything
        self.scan()
        self.exploit()
        self.post_exploit()
```

### After (Fine-Grained Actions)
```python
from core.base_module import BaseModule, action

class MyModule(BaseModule):
    def __init__(self):
        self.options = {
            "TARGET": {"value": "", "required": False}  # Not required!
        }
        self._register_actions()
    
    def _register_actions(self):
        @action(
            name="scan",
            description="Scan target",
            required_options=["TARGET"],
            tags=["recon"]
        )
        def scan_action():
            return self._scan()
        
        @action(
            name="exploit",
            description="Exploit target",
            required_options=["TARGET", "PAYLOAD"],
            tags=["exploitation"]
        )
        def exploit_action():
            return self._exploit()
    
    def run(self):
        # Default behavior
        return self._scan()
```

## Troubleshooting

### Action Not Found
```
Error: Action 'invalid_action' not found in module
```
**Solution**: Run `actions` command to see available actions

### Missing Required Options
```
Error: Missing required option: TARGET
```
**Solution**: Check action's required options with `show actions`

### Option Validation Failed
```
Error: Action validation failed
```
**Solution**: Ensure all required options are set before running

## Advanced Features

### Action Chaining in Playbooks

```yaml
steps:
  - module: "reconnaissance/port_scan"
    action: "scan_tcp"
    output_var: "scan_results"
  
  - module: "reconnaissance/web_scan"
    action: "scan_server"
    options:
      TARGET: "{{scan_results.open_ports[0].host}}"
      PORT: "{{scan_results.open_ports[0].port}}"
```

### Conditional Execution

```yaml
steps:
  - module: "c2_frameworks/poshc2"
    action: "list_implants"
    condition: "result.count > 0"
    next_action: "execute_command"
```

### Parallel Actions

```yaml
steps:
  - module: "reconnaissance/port_scan"
    action: "scan_tcp"
    parallel: true
  
  - module: "reconnaissance/web_scan"
    action: "scan_server"
    parallel: true
```

## Summary

The fine-grained actions framework provides:
- ✅ Surgical precision for specific behaviors
- ✅ Better playbook control
- ✅ Clear separation of concerns
- ✅ Easier testing and debugging
- ✅ Flexible module design
- ✅ Consistent interface across modules

Use `actions` command in any module to see what's available!
