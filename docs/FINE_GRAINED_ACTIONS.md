# Fine-Grained Actions Framework

## Overview

The Escanor framework now supports **fine-grained actions** within modules, allowing you to execute specific behaviors or attacks without running an entire module's default functionality. This provides precise control over your operations.

## Key Concepts

### Modules vs Actions

- **Modules**: Contain related functionality (e.g., `c2_frameworks/koadic`)
- **Actions**: Specific operations within a module (e.g., `generate_stager`, `start_listener`, `list_zombies`)

### Benefits

1. **Precision**: Execute only the behavior you need
2. **Flexibility**: Mix and match actions from different modules
3. **Efficiency**: Skip unnecessary steps in your workflow
4. **Playbook Control**: Define exact actions in playbooks for curated templates

## Usage

### Interactive Shell Commands

#### List Available Actions

```bash
escanor> use c2_frameworks/koadic
escanor: c2_frameworks/koadic> actions

================================================================================
ACTIONS AVAILABLE IN MODULE: koadic
================================================================================

Action               Description                                     Tags
--------------------------------------------------------------------------------
   run               Execute the module's primary function           -
>>> generate_stager  Generate a stager payload for deployment        payload, offense
   start_listener    Start a Koadic listener to receive connections  setup, listener
   list_modules      List all available Koadic modules               recon, modules
   list_zombies      List all active zombies (compromised hosts)     recon, zombies
   execute_module    Execute a Koadic module on a specific zombie    execution, post-exploitation

Current action: none

Use 'action <name>' to select an action before running
================================================================================
```

#### Select and Execute an Action

```bash
escanor> use c2_frameworks/koadic
escanor: c2_frameworks/koadic> action generate_stager
[+] Action selected: generate_stager
    Description: Generate a stager payload for deployment
    Required options: listener_host, listener_port

escanor: c2_frameworks/koadic> set LISTENER_HOST 192.168.1.100
LISTENER_HOST => 192.168.1.100

escanor: c2_frameworks/koadic> set LISTENER_PORT 4444
LISTENER_PORT => 4444

escanor: c2_frameworks/koadic> set STAGER_TYPE js/mshta
STAGER_TYPE => js/mshta

escanor: c2_frameworks/koadic> run -v --operator "red.team"
```

#### One-Liner Execution

```bash
escanor> execute c2_frameworks/koadic LISTENER_HOST=192.168.1.100 LISTENER_PORT=4444 STAGER_TYPE=js/mshta
```

Note: For one-liner execution with actions, use the `--action` flag (coming soon) or load the module first.

### Programmatic Usage

```python
from core.module_manager import ModuleManager

mm = ModuleManager()

# Get module
module = mm.get_module("c2_frameworks/koadic")

# List available actions
actions = module.list_actions()
for name, action_def in actions.items():
    print(f"{name}: {action_def.description}")

# Set options
module.set_option("listener_host", "192.168.1.100")
module.set_option("listener_port", "4444")
module.set_option("stager_type", "js/mshta")

# Execute specific action
result = mm.run_module(
    "c2_frameworks/koadic",
    action="generate_stager",  # Specify the action
    verbose=True
)
```

## Creating Modules with Actions

### Example Module Structure

```python
from core.base_module import BaseModule

class MyModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "my_module"
        self.display_name = "My Custom Module"
        self.description = "Demonstrates fine-grained actions"
        self.category = "custom"
        
        # Define options
        self.options = {
            "target": {
                "value": "",
                "required": True,
                "description": "Target IP or hostname"
            },
            "port": {
                "value": "445",
                "required": False,
                "description": "Target port"
            }
        }
        
        # Register actions
        self.register_action(
            name="scan",
            description="Perform network scan",
            method_name="do_scan",
            required_options=["target"],
            optional_options=["port"],
            tags=["recon", "network"]
        )
        
        self.register_action(
            name="exploit",
            description="Launch exploit against target",
            method_name="do_exploit",
            required_options=["target"],
            tags=["offense", "exploit"]
        )
    
    def do_scan(self) -> dict:
        """Execute scan action"""
        target = self.get_option("target")
        port = self.get_option("port")
        
        # Scan logic here
        return {
            "success": True,
            "data": {"scanned": target, "port": port}
        }
    
    def do_exploit(self) -> dict:
        """Execute exploit action"""
        target = self.get_option("target")
        
        # Exploit logic here
        return {
            "success": True,
            "data": {"exploited": target}
        }
    
    def run(self) -> dict:
        """Default run method (also registered as 'run' action)"""
        return self.do_scan()
```

### Using the @action Decorator

```python
from core.base_module import BaseModule

class MyModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "decorated_module"
        # ... other initialization ...
    
    @action(name="quick_scan", 
            description="Quick network scan",
            required_options=["target"],
            tags=["fast", "recon"])
    def quick_scan(self) -> dict:
        # Implementation
        pass
    
    @action(name="deep_scan",
            description="Comprehensive network scan",
            required_options=["target", "ports"],
            tags=["thorough", "recon"])
    def deep_scan(self) -> dict:
        # Implementation
        pass
```

## Playbook Integration

Playbooks can now specify which action to execute for each step:

```yaml
name: "C2 Framework Coordination"
description: "Coordinated C2 operations with fine-grained control"
author: "Red Team"
created: "2024-01-01"

steps:
  - module: "c2_frameworks/koadic"
    action: "start_listener"  # Execute specific action
    description: "Start listener for callbacks"
    options:
      LISTENER_HOST: "192.168.1.100"
      LISTENER_PORT: "4444"
    enabled: true
    critical: true

  - module: "c2_frameworks/koadic"
    action: "generate_stager"  # Different action, same module
    description: "Generate payload for deployment"
    options:
      STAGER_TYPE: "js/mshta"
    enabled: true
    critical: false

  - module: "c2_frameworks/koadic"
    action: "list_zombies"  # Another action
    description: "Check for compromised hosts"
    options: {}
    enabled: true
    critical: false
```

## Action Definition Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Short identifier used in commands |
| `description` | string | Yes | Human-readable description |
| `method_name` | string | Yes | Method to call on the module |
| `required_options` | list | No | Options that must be set before execution |
| `optional_options` | list | No | Options that may be used |
| `tags` | list | No | Tags for categorization and search |

## Best Practices

### When to Use Actions

1. **Multiple Distinct Operations**: When a module performs several unrelated tasks
2. **Workflow Stages**: When operations have clear stages (setup → execute → cleanup)
3. **C2 Frameworks**: Perfect for C2 modules with distinct capabilities
4. **Tool Wrappers**: When wrapping external tools with multiple modes

### Naming Conventions

- Use verb-noun format: `generate_payload`, `start_listener`, `list_modules`
- Be descriptive but concise
- Use consistent terminology across modules

### Option Management

- Define action-specific required options
- Use `validate_options()` to check before execution
- Document option requirements in action descriptions

## Migration Guide

### Updating Existing Modules

If you have existing modules and want to add action support:

1. **Keep backward compatibility**: The default `run()` method is automatically registered as an action
2. **Add new actions incrementally**: Register additional actions in `__init__()`
3. **Update playbooks**: Add `action:` fields to playbook steps where needed

### Example Migration

**Before:**
```python
class OldModule(BaseModule):
    def run(self):
        # Does everything
        pass
```

**After:**
```python
class NewModule(BaseModule):
    def __init__(self):
        super().__init__()
        # Register granular actions
        self.register_action(
            name="phase1",
            description="Initial reconnaissance",
            method_name="do_recon"
        )
        self.register_action(
            name="phase2", 
            description="Exploitation",
            method_name="do_exploit"
        )
    
    def do_recon(self):
        # Recon logic
        pass
    
    def do_exploit(self):
        # Exploit logic
        pass
    
    def run(self):
        # Default behavior - can call both or just one
        return self.do_recon()
```

## Troubleshooting

### Common Issues

**"Action not found"**
- Check spelling of action name
- Use `actions` command to see available actions
- Ensure action is registered in module's `__init__()`

**"Missing required option"**
- Each action can have its own required options
- Use `show options` to see what's needed
- Set options before running the action

**"Method not found"**
- The `method_name` in action registration must match an actual method
- Check for typos in method names

## Advanced Features

### Dynamic Action Registration

```python
def __init__(self):
    super().__init__()
    
    # Register actions based on configuration
    if self.check_feature_available("advanced"):
        self.register_action(
            name="advanced_mode",
            description="Run with advanced features",
            method_name="run_advanced"
        )
```

### Action Chaining

Create playbooks that chain multiple actions from the same or different modules:

```yaml
steps:
  - module: "reconnaissance/port_scan"
    action: "scan_tcp"
    options:
      PORTS: "1-1000"
  
  - module: "exploitation/web_scanner"
    action: "scan_found_ports"
    options:
      USE_RESULTS_FROM: "reconnaissance/port_scan"
```

## Summary

Fine-grained actions give you surgical precision in your operations:

- **Modules** are containers for related functionality
- **Actions** are the specific behaviors you want to execute
- **Playbooks** orchestrate actions into curated workflows

This architecture separates concerns while maintaining flexibility, making the framework more versatile for both automated playbooks and manual operations.
