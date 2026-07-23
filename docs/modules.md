# Escanor Framework - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Architecture](#architecture)
5. [Core Components](#core-components)
6. [Modules Reference](#modules-reference)
7. [Playbooks Reference](#playbooks-reference)
8. [AI Integration](#ai-integration)
9. [Creating Custom Modules](#creating-custom-modules)
10. [Creating Playbooks](#creating-playbooks)
11. [API Reference](#api-reference)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)

---

## Introduction

### What is Escanor?

**Escanor** is an advanced, AI-powered purple teaming framework designed for cybersecurity teams to conduct comprehensive security assessments, penetration testing, and defensive analysis. Inspired by modern frameworks like KittySploit, Escanor enhances capabilities with:

- **Modular Architecture**: Easily extendable module system organized by category
- **Interactive Shell**: Intuitive command-line interface with contextual help
- **Playbook Engine**: Curated module sequences for routine assessment tasks
- **AI Integration**: Smart analysis powered by Ollama, OpenAI, or other LLM backends
- **Purple Teaming**: Balanced offensive and defensive perspectives

### Key Features

| Feature | Description |
|---------|-------------|
| **Interactive Shell** | Full-featured CLI with context-aware prompts |
| **Module System** | Hot-reloadable modules in 6 categories |
| **Playbook Engine** | YAML-based workflow automation |
| **AI Assistance** | Multi-provider LLM integration |
| **Extensible** | Plugin-friendly architecture |
| **Logging** | Comprehensive operation tracking |

### Supported Categories

1. **Reconnaissance** - Information gathering and scanning
2. **Exploitation** - Safe exploitation modules (authorized use only)
3. **Persistence** - Post-exploitation simulation
4. **Lateral Movement** - Network pivoting simulation
5. **Exfiltration** - Data movement analysis
6. **AI-Assisted** - Intelligent analysis and recommendations

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Linux/macOS/Windows (with WSL)

### Step-by-Step Installation

```bash
# Clone the repository
git clone https://github.com/your-org/escanor.git
cd escanor

# Install dependencies
pip install -r requirements.txt

# Make executable (Linux/macOS)
chmod +x escanor.py

# Verify installation
python3 escanor.py --help
```

### Dependencies

The framework requires the following Python packages:

```txt
pyyaml>=6.0
requests>=2.28.0
```

Install them with:
```bash
pip install pyyaml requests
```

### Optional: AI Backend Setup

#### Option 1: Ollama (Local, Recommended)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. Configure environment:
   ```bash
   export ESCANOR_AI_PROVIDER=ollama
   export ESCANOR_AI_URL=http://localhost:11434
   export ESCANOR_AI_MODEL=llama3.2
   ```

#### Option 2: OpenAI (Cloud)

1. Get an API key from [OpenAI](https://platform.openai.com)
2. Configure environment:
   ```bash
   export ESCANOR_AI_PROVIDER=openai
   export ESCANOR_AI_API_KEY=your-api-key-here
   ```

---

## Quick Start

### Launch Interactive Shell

```bash
python3 escanor.py
```

### Basic Commands

```
escanor> help              # Show all commands
escanor> list              # List all available modules
escanor> list recon        # List reconnaissance modules
escanor> use port_scan     # Load a module
escanor:port_scan> set TARGET 192.168.1.1
escanor:port_scan> set PORTS 1-1000
escanor:port_scan> show options
escanor:port_scan> run
escanor:port_scan> back    # Return to main shell
escanor> exit
```

### Running Playbooks

```bash
# List available playbooks
python3 escanor.py --list-playbooks

# Execute a playbook
python3 escanor.py --playbook basic_recon

# Or from within the shell
escanor> playbook basic_recon
```

### AI-Assisted Operations

```bash
# From command line
python3 escanor.py --ai "What are common web vulnerabilities?"

# From interactive shell
escanor> ai "Analyze the scan results for 192.168.1.1"
```

---

## Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │Interactive  │  │Command-Line │  │  Playbook       │ │
│  │Shell        │  │Arguments    │  │  Engine         │ │
│  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘ │
└─────────┼────────────────┼──────────────────┼──────────┘
          │                │                  │
┌─────────▼────────────────▼──────────────────▼──────────┐
│                   Core Framework                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Module Manager                      │   │
│  │  • Dynamic Loading  • Hot Reload  • Validation  │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                      Modules                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Recon     │ │Exploit   │ │Persist   │ │Lateral   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐                             │
│  │Exfil     │ │AI Assist │                             │
│  └──────────┘ └──────────┘                             │
└─────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  External Services                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │Ollama (LLM) │  │OpenAI (LLM) │  │Target Systems   │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
escanor/
├── escanor.py              # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── core/                  # Core framework components
│   ├── __init__.py
│   ├── base_module.py     # Base module class
│   ├── module_manager.py  # Module loading & execution
│   ├── interactive_shell.py  # CLI interface
│   └── playbook_engine.py # Playbook execution
├── modules/               # Security modules
│   ├── reconnaissance/    # Recon modules
│   │   ├── port_scan.py
│   │   ├── web_scan.py
│   │   └── vuln_scan.py
│   ├── exploitation/      # Exploitation modules
│   ├── persistence/       # Persistence modules
│   ├── lateral_movement/  # Lateral movement modules
│   ├── exfiltration/      # Exfiltration modules
│   └── ai_assisted/       # AI-powered modules
│       └── ai_analyze.py
├── playbooks/             # Assessment playbooks
│   ├── basic_recon.yaml
│   ├── web_app_assessment.yaml
│   └── purple_team.yaml
├── lib/                   # Library modules
│   ├── __init__.py
│   └── ai_integration.py  # AI backend integration
├── utils/                 # Utility functions
│   └── __init__.py
└── docs/                  # Documentation
    ├── architecture.md
    └── modules.md
```

---

## Core Components

### 1. BaseModule (`core/base_module.py`)

Abstract base class that all modules must inherit from.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Unique module identifier |
| `category` | str | Module category |
| `description` | str | Human-readable description |
| `author` | str | Module author |
| `version` | str | Module version |
| `options` | dict | Configurable options |
| `required_options` | list | Mandatory options |

#### Methods

| Method | Description |
|--------|-------------|
| `validate()` | Validates all required options |
| `execute(verbose=False)` | Runs the module logic |
| `get_info()` | Returns module metadata |
| `set_option(name, value)` | Sets an option value |

### 2. ModuleManager (`core/module_manager.py`)

Dynamic module loading and management system.

#### Features

- Auto-discovers modules in `/modules` directory
- Supports hot-reloading without restart
- Case-insensitive module lookup
- Category-based organization
- Thread-safe operations

#### Usage

```python
from core.module_manager import ModuleManager

manager = ModuleManager()
modules = manager.list_modules()  # Dict of categories -> modules
module = manager.get_module('port_scan')
manager.run_module('port_scan', verbose=True)
```

### 3. InteractiveShell (`core/interactive_shell.py`)

Rich command-line interface for the framework.

#### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show help message | `help` |
| `use` | Select a module | `use port_scan` |
| `run` | Execute current module | `run` |
| `set` | Set module option | `set TARGET 192.168.1.1` |
| `show` | Display options/info | `show options` |
| `back` | Deselect module | `back` |
| `info` | Show module info | `info` |
| `list` | List modules | `list recon` |
| `reload` | Reload all modules | `reload` |
| `playbook` | Execute playbook | `playbook basic_recon` |
| `ai` | AI-assisted query | `ai "analyze results"` |
| `exit` | Exit framework | `exit` |

### 4. PlaybookEngine (`core/playbook_engine.py`)

Workflow automation engine for executing module sequences.

#### Playbook Format

```yaml
name: basic_recon
description: Basic reconnaissance workflow
steps:
  - module: port_scan
    options:
      TARGET: "{{ target }}"
      PORTS: "1-1000"
  - module: web_scan
    options:
      TARGET: "{{ target }}"
      PORT: "80"
  - module: vuln_scan
    options:
      TARGET: "{{ target }}"
```

#### Features

- Sequential module execution
- Variable substitution with `{{ variable }}`
- Conditional step execution
- Result aggregation
- Error handling and rollback

### 5. AIIntegration (`lib/ai_integration.py`)

Multi-provider AI/LLM integration layer.

#### Supported Providers

| Provider | Type | Configuration |
|----------|------|---------------|
| Ollama | Local | `ESCANOR_AI_URL`, `ESCANOR_AI_MODEL` |
| OpenAI | Cloud | `ESCANOR_AI_API_KEY` |

#### Environment Variables

```bash
ESCANOR_AI_PROVIDER=ollama        # or 'openai'
ESCANOR_AI_URL=http://localhost:11434
ESCANOR_AI_MODEL=llama3.2
ESCANOR_AI_API_KEY=sk-...
```

---

## Modules Reference

### Reconnaissance Modules

#### PortScanner

Scans target for open ports.

**Options:**
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `TARGET` | Yes | - | Target IP or hostname |
| `PORTS` | No | 1-1000 | Port range to scan |
| `TIMEOUT` | No | 1 | Connection timeout (seconds) |

**Example:**
```
escanor> use port_scan
escanor:port_scan> set TARGET 192.168.1.1
escanor:port_scan> set PORTS 1-1000
escanor:port_scan> run
```

#### WebScanner

Enumerates web application information.

**Options:**
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `TARGET` | Yes | - | Target URL |
| `PORT` | No | 80 | Target port |
| `PATHS` | No | / | Paths to enumerate |

#### VulnerabilityScanner

Performs basic vulnerability detection.

**Options:**
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `TARGET` | Yes | - | Target IP or URL |
| `SCAN_TYPE` | No | basic | Scan type (basic/full) |

### AI-Assisted Modules

#### AIAssistant

Provides AI-powered analysis and recommendations.

**Options:**
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `TARGET` | No | - | Target for analysis |
| `CONTEXT` | No | - | Additional context |
| `QUERY` | Yes | - | Analysis query |

**Example:**
```
escanor> use ai_assistant
escanor:ai_assistant> set TARGET 192.168.1.1
escanor:ai_assistant> set QUERY "What vulnerabilities might exist?"
escanor:ai_assistant> run
```

### Empty Categories (Ready for Extension)

- **exploitation/** - Add safe exploitation modules
- **persistence/** - Add persistence simulation modules
- **lateral_movement/** - Add lateral movement modules
- **exfiltration/** - Add exfiltration analysis modules

---

## Playbooks Reference

### basic_recon

Basic reconnaissance workflow for initial assessment.

**Steps:**
1. Port scan (ports 1-1000)
2. Web scan (if HTTP detected)
3. Vulnerability scan

**Usage:**
```bash
python3 escanor.py --playbook basic_recon
```

### web_app_assessment

Comprehensive web application assessment.

**Steps:**
1. Port scan (web ports)
2. Web enumeration
3. Technology detection
4. Vulnerability scanning
5. AI analysis

**Usage:**
```bash
python3 escanor.py --playbook web_app_assessment
```

### purple_team

Full purple team engagement workflow.

**Steps:**
1. Reconnaissance phase
2. Exploitation simulation
3. Persistence simulation
4. Lateral movement simulation
5. Exfiltration analysis
6. AI-powered report generation

**Usage:**
```bash
python3 escanor.py --playbook purple_team
```

---

## AI Integration

### Configuration

Set environment variables before running:

```bash
# For Ollama (local)
export ESCANOR_AI_PROVIDER=ollama
export ESCANOR_AI_URL=http://localhost:11434
export ESCANOR_AI_MODEL=llama3.2

# For OpenAI (cloud)
export ESCANOR_AI_PROVIDER=openai
export ESCANOR_AI_API_KEY=sk-your-key-here
```

### Using AI Features

#### Direct Query

```bash
python3 escanor.py --ai "Explain common SQL injection techniques"
```

#### In Interactive Shell

```
escanor> ai "What are the next steps after finding port 80 open?"
```

#### In Modules

AI-assisted modules automatically use configured provider.

### Supported AI Tasks

- Vulnerability analysis
- Attack path recommendations
- Report generation
- Threat intelligence correlation
- Defensive control suggestions

---

## Creating Custom Modules

### Module Template

Create a new file in the appropriate category folder:

```python
#!/usr/bin/env python3
"""
Your Module Description
"""

from typing import Dict, Any, Optional
from core.base_module import BaseModule


class YourModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "your_module"
        self.category = "your_category"
        self.description = "Detailed module description"
        self.author = "Your Name"
        self.version = "1.0.0"
        
        # Define configurable options
        self.options: Dict[str, Any] = {
            'TARGET': '',
            'OPTION2': 'default_value',
            'OPTION3': True
        }
        
        # Specify required options
        self.required_options: list = ['TARGET']
    
    def validate(self) -> bool:
        """Validate all required options are set"""
        return super().validate()
    
    def execute(self, verbose: bool = False) -> Optional[Dict[str, Any]]:
        """
        Execute the module logic
        
        Args:
            verbose: Enable verbose output
            
        Returns:
            Dictionary with results or None on failure
        """
        if not self.validate():
            return None
        
        target = self.options.get('TARGET')
        
        if verbose:
            print(f"[*] Executing against {target}")
        
        # Your module logic here
        result = {
            'status': 'success',
            'data': []
        }
        
        if verbose:
            print(f"[+] Execution complete")
        
        return result
```

### Module Best Practices

1. **Always validate** options before execution
2. **Handle errors gracefully** with informative messages
3. **Use verbose mode** for detailed output
4. **Return structured data** for playbook integration
5. **Document options** clearly in docstrings
6. **Test thoroughly** before deployment

### Registering Modules

Modules are auto-discovered based on:
- Location in `/modules/<category>/` folder
- Class inheriting from `BaseModule`
- Proper `name` and `category` attributes

No manual registration required!

---

## Creating Playbooks

### Playbook Structure

Playbooks are YAML files in `/playbooks/`:

```yaml
name: my_custom_playbook
description: Description of what this playbook does
author: Your Name
version: "1.0"

# Optional: Global variables
variables:
  default_timeout: 5
  scan_type: basic

steps:
  - name: Initial Port Scan
    module: port_scan
    options:
      TARGET: "{{ target }}"
      PORTS: "1-1000"
      TIMEOUT: "{{ default_timeout }}"
    
  - name: Web Enumeration
    module: web_scan
    options:
      TARGET: "{{ target }}"
      PORT: "80"
    condition: "previous_step.status == 'success'"
    
  - name: AI Analysis
    module: ai_assistant
    options:
      TARGET: "{{ target }}"
      QUERY: "Analyze findings and suggest next steps"
```

### Variable Substitution

Use `{{ variable_name }}` for dynamic values:

- Passed via command line
- Defined in playbook `variables` section
- From previous step results

### Conditional Execution

Add conditions to steps:

```yaml
condition: "previous_step.status == 'success'"
condition: "'80' in previous_step.data.open_ports"
```

### Testing Playbooks

```bash
# Dry run (if implemented)
python3 escanor.py --playbook my_playbook --dry-run

# Verbose execution
python3 escanor.py --playbook my_playbook --verbose
```

---

## API Reference

### BaseModule Class

```python
class BaseModule:
    # Properties
    name: str
    category: str
    description: str
    author: str
    version: str
    options: Dict[str, Any]
    required_options: List[str]
    
    # Methods
    def validate(self) -> bool
    def execute(self, verbose: bool = False) -> Optional[Dict]
    def get_info(self) -> Dict
    def set_option(self, name: str, value: Any) -> bool
```

### ModuleManager Class

```python
class ModuleManager:
    # Methods
    def __init__(self)
    def list_modules(self) -> Dict[str, List[str]]
    def get_module(self, name: str) -> Optional[BaseModule]
    def run_module(self, name: str, verbose: bool = False) -> Optional[Dict]
    def reload_modules(self)
```

### PlaybookEngine Class

```python
class PlaybookEngine:
    # Methods
    def __init__(self, module_manager: ModuleManager)
    def list_playbooks(self) -> List[str]
    def execute_playbook(self, name: str, 
                        variables: Dict = None,
                        verbose: bool = False) -> Dict
```

### AIIntegration Class

```python
class AIIntegration:
    # Methods
    def __init__(self)
    def query(self, prompt: str, context: str = None) -> str
    def analyze(self, data: Dict, query: str) -> str
    def is_available(self) -> bool
```

---

## Troubleshooting

### Common Issues

#### Module Not Found

```
[!] Module not found: port_scan
```

**Solution:**
- Check module exists in `/modules/reconnaissance/`
- Verify class inherits from `BaseModule`
- Run `reload` in interactive shell

#### AI Not Available

```
[!] AI backend not available
```

**Solution:**
- Ensure Ollama is running: `ollama serve`
- Check environment variables are set
- Verify API key for OpenAI

#### Permission Denied

```
PermissionError: [Errno 13]
```

**Solution:**
- Run with appropriate privileges
- On Linux, may need `sudo` for raw socket operations

#### Import Errors

```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Debug Mode

Enable verbose output for debugging:

```bash
python3 escanor.py --verbose --list-modules
```

Or in interactive shell:
```
escanor> set VERBOSE true
```

### Logs

Check logs in the current directory or configured log path.

---

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write tests
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Add unit tests

### Adding New Categories

1. Create folder in `/modules/`
2. Add `__init__.py`
3. Place modules inside
4. Update documentation

### Reporting Issues

Use GitHub Issues with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

---

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Inspired by KittySploit framework
- Built for purple team operations
- Community-driven development

---

**Escanor Framework v1.0.0**  
*For authorized security testing only*
