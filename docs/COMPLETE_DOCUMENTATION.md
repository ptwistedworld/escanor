# Escanor Framework - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Architecture](#architecture)
6. [Modules](#modules)
7. [Interactive Shell](#interactive-shell)
8. [Playbooks](#playbooks)
9. [AI Integration (Optional)](#ai-integration)
10. [Reporting System](#reporting-system)
11. [Creating Custom Modules](#creating-custom-modules)
12. [Entra ID Assessment](#entra-id-assessment)
13. [C2 Framework Integration](#c2-framework-integration)
14. [Troubleshooting](#troubleshooting)

---

## Introduction

**Escanor** is an advanced, modular purple teaming framework designed for cybersecurity teams to perform comprehensive security assessments, penetration testing, and defensive validation. Named after the legendary hero known for overwhelming power, Escanor brings together offensive and defensive capabilities in a single, extensible platform.

### Key Principles

- **Modularity**: Easy to extend with new modules
- **Flexibility**: Works standalone or with AI assistance
- **Standardization**: Consistent reporting and output formats
- **Purple Teaming**: Balanced offensive and defensive perspectives
- **Cloud-Native**: Built-in support for Azure Entra ID assessments

---

## Features

### Core Capabilities

- **Interactive Shell**: Metasploit-style CLI with contextual help
- **Module System**: 14+ modules across 11 categories
- **Targeted Execution**: Run individual modules without loading playbooks
- **Playbook Engine**: Curated collections of modules for routine tasks
- **Automated Reporting**: Detailed text and JSON reports for every execution
- **AI Integration** (Optional): Multi-provider AI support (Ollama, OpenAI)

### Module Categories

1. **Reconnaissance** - Port scanning, web enumeration, vulnerability discovery
2. **Exploitation/Privesc** - Privilege escalation (GodPotato, SigmaPotato, PrintSpoofer)
3. **C2 Frameworks** - Empire, PoshC2, Koadic integration
4. **Evasion** - EDRSilencer for endpoint detection bypass testing
5. **Cloud/Entra** - Azure Entra ID assessments (CA policies, Device Code Flow, Service Principals)
6. **AI-Assisted** - AI-powered analysis and recommendations
7. **Persistence** - Persistence mechanism testing
8. **Lateral Movement** - Lateral movement simulations
9. **Exfiltration** - Data exfiltration testing

### Reporting

- Automatic report generation for every module execution
- Standardized format with metadata, findings, and recommendations
- Both human-readable (TXT) and machine-parseable (JSON) formats
- Report consolidation for multi-module assessments
- Sensitive data redaction in reports

---

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Git (for cloning)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/your-org/escanor-framework.git
cd escanor-framework

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 escanor.py --help
```

### Optional: AI Configuration

Escanor works perfectly without AI. To enable AI features:

```bash
# For Ollama (local LLM)
export ESCANOR_AI_PROVIDER=ollama
export ESCANOR_AI_URL=http://localhost:11434
export ESCANOR_AI_MODEL=llama3.2

# For OpenAI
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
escanor> help                    # Show all commands
escanor> list                    # List all modules
escanor> list cloud/entra       # List Entra-specific modules
escanor> search potato          # Search for modules
escanor> use reconnaissance/port_scan
escanor> set TARGET 192.168.1.1
escanor> run -v --operator "john.doe" --notes "Initial scan"
escanor> reports                # View generated reports
```

### One-Liner Execution

```bash
# Execute a module directly
python3 escanor.py --module reconnaissance/port_scan

# Or from the shell
escanor> execute exploitation/privesc/godpotato cmd="whoami"
```

### Run a Playbook

```bash
# From command line
python3 escanor.py --playbook purple_team

# From shell
escanor> playbook purple_team
```

---

## Architecture

```
escanor/
├── core/                      # Core framework components
│   ├── base_module.py         # Abstract base class for modules
│   ├── module_manager.py      # Module loading and execution
│   ├── interactive_shell.py   # CLI interface
│   ├── playbook_engine.py     # Playbook execution engine
│   └── module_result.py       # Result container class
├── modules/                   # All security modules
│   ├── reconnaissance/        # Recon modules
│   ├── exploitation/          # Exploitation modules
│   │   └── privesc/           # Privilege escalation
│   ├── c2_frameworks/         # C2 integrations
│   ├── evasion/               # Evasion testing
│   ├── cloud/entra/           # Azure Entra ID modules
│   └── ai_assisted/           # AI-powered modules
├── playbooks/                 # Pre-built playbooks
├── utils/                     # Utilities
│   └── result_reporter.py     # Report generation
├── lib/                       # Libraries
│   └── ai_integration.py      # AI provider integration
└── escanor.py                 # Main entry point
```

### Component Responsibilities

| Component | Purpose |
|-----------|---------|
| `BaseModule` | Abstract class defining module interface |
| `ModuleManager` | Loads, catalogs, and executes modules |
| `InteractiveShell` | Provides CLI with command parsing |
| `PlaybookEngine` | Orchestrates multi-module workflows |
| `ResultReporter` | Generates standardized reports |
| `AIIntegration` | Connects to AI providers (optional) |

---

## Modules

### Complete Module Inventory

#### Reconnaissance (3 modules)

| Module | Description |
|--------|-------------|
| `port_scan` | TCP/UDP port scanning with service detection |
| `web_scan` | Web application enumeration and directory brute-forcing |
| `vuln_scan` | Vulnerability assessment and CVE matching |

#### Exploitation/Privilege Escalation (3 modules)

| Module | Description |
|--------|-------------|
| `godpotato` | GodPotato privilege escalation exploit |
| `sigmapotato` | SigmaPotato token impersonation |
| `printspoofer` | PrintSpoofer named pipe impersonation |

#### C2 Frameworks (3 modules)

| Module | Description |
|--------|-------------|
| `empire_c2` | PowerShell Empire C2 integration |
| `poshc2` | PoshC2 framework coordination |
| `koadic` | Koadic COM-based post-exploitation |

#### Evasion (1 module)

| Module | Description |
|--------|-------------|
| `edrsilencer` | EDRSilencer for testing EDR bypass techniques |

#### Cloud/Entra ID (3 modules)

| Module | Description |
|--------|-------------|
| `ca_validator` | Conditional Access policy validation |
| `device_code_flow` | Device code authentication flow simulation |
| `sp_assessment` | Service Principal and Managed Identity assessment |

#### AI-Assisted (1 module)

| Module | Description |
|--------|-------------|
| `ai_analyze` | AI-powered result analysis and recommendations |

### Using Modules

#### Load and Configure

```
escanor> use cloud/entra/ca_validator
escanor> show options

Option               Value                          Required   Description
----------------------------------------------------------------------------------------------------
TENANT_ID                                           Yes        Azure Entra ID Tenant ID
CLIENT_ID                                           Yes        Service Principal Client ID
CLIENT_SECRET                                       No         Service Principal Client Secret
POLICY_IDS                                          No         Comma-separated policy IDs to test
TEST_USER                                           No         User principal name for testing
LOCATIONS                                           No         Comma-separated locations/IPs

escanor> set TENANT_ID your-tenant-id
escanor> set CLIENT_ID your-client-id
escanor> set CLIENT_SECRET your-secret
```

#### Execute with Reporting

```
escanor> run -v --operator "security-team" --notes "Q1 CA policy audit"

[*] Loading module: ca_validator
    Category: cloud/entra
    Description: Validate and test Conditional Access policies for misconfigurations

[*] Executing ca_validator...

[+] Module completed successfully
    Execution time: 2.34s
    Report written to: ./results/ca_validator_20250115_143022.txt
```

#### One-Liner Execution

```
escanor> execute cloud/entra/device_code_flow TENANT_ID=xxx CLIENT_ID=yyy SIMULATE_ATTACK=True
```

---

## Interactive Shell

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Display help information | `help` |
| `use <module>` | Select a module | `use recon/port_scan` |
| `run [opts]` | Execute selected module | `run -v --operator "team"` |
| `execute <module> [opts]` | Run module directly | `execute mod/name opt=val` |
| `set <opt> <val>` | Set module option | `set TARGET 10.0.0.1` |
| `show [options]` | Display module info | `show options` |
| `back` | Deselect current module | `back` |
| `list [category]` | List modules | `list cloud/entra` |
| `search <term>` | Search modules | `search potato` |
| `playbook <name>` | Execute playbook | `playbook purple_team` |
| `playbook list` | List playbooks | `playbook list` |
| `ai <query>` | AI-assisted query | `ai "analyze results"` |
| `reports` | List generated reports | `reports` |
| `report <num>` | View specific report | `report 1` |
| `reload` | Reload all modules | `reload` |
| `banner` | Redisplay banner | `banner` |
| `exit/quit` | Exit framework | `exit` |

### Run Command Options

```
run [OPTIONS]

Options:
  -v, --verbose           Detailed output during execution
  --no-report             Skip automatic report generation
  --operator <name>       Specify operator name for report
  --notes "<text>"        Add notes to the report

Examples:
  run -v
  run --operator "jane.doe" --notes "Weekly assessment"
  run --no-report
```

---

## Playbooks

Playbooks are YAML files that define sequences of modules to execute for common scenarios.

### Available Playbooks

| Playbook | Description | Modules |
|----------|-------------|---------|
| `basic_recon` | Fundamental reconnaissance | Port scan, web scan |
| `web_app_assessment` | Web application testing | Web scan, vuln scan |
| `purple_team` | Full purple team exercise | Multiple categories |
| `c2_framework_coordination` | C2 testing | Empire, PoshC2, Koadic |
| `edr_evasion_testing` | EDR bypass validation | EDRSilencer |
| `full_attack_simulation` | End-to-end attack simulation | All categories |

### Running Playbooks

```bash
# Command line
python3 escanor.py --playbook purple_team -v

# Interactive shell
escanor> playbook purple_team
escanor> playbook list
```

### Creating Custom Playbooks

Create a YAML file in `/playbooks/`:

```yaml
name: custom_assessment
description: Custom security assessment playbook
author: Your Team
version: 1.0

modules:
  - module: reconnaissance/port_scan
    options:
      TARGET: "192.168.1.0/24"
      PORTS: "1-1000"
    
  - module: cloud/entra/ca_validator
    options:
      TENANT_ID: "${ENV_TENANT_ID}"
      CLIENT_ID: "${ENV_CLIENT_ID}"
    
  - module: exploitation/privesc/godpotato
    options:
      cmd: "whoami"

post_execution:
  - generate_report: true
  - consolidate: true
```

---

## AI Integration (Optional)

Escanor functions completely without AI. AI features are optional enhancements.

### Supported Providers

- **Ollama** (Local, recommended for privacy)
- **OpenAI** (Cloud-based)

### Configuration

```bash
# Ollama setup
export ESCANOR_AI_PROVIDER=ollama
export ESCANOR_AI_URL=http://localhost:11434
export ESCANOR_AI_MODEL=llama3.2

# OpenAI setup
export ESCANOR_AI_PROVIDER=openai
export ESCANOR_AI_API_KEY=sk-...
```

### AI Capabilities

- **Module Suggestions**: Get AI recommendations for modules based on objectives
- **Result Analysis**: Automated analysis of module outputs
- **Report Generation**: AI-assisted report writing
- **Technique Explanation**: Learn about security concepts
- **Next Steps**: Get contextual recommendations

### Usage Examples

```
escanor> ai "What modules should I use to test MFA bypass?"
escanor> ai "Analyze these results and suggest mitigations"
escanor> ai "Explain the Golden Ticket attack technique"
```

---

## Reporting System

### Automatic Reports

Every module execution generates:
- **Text Report** (`*.txt`) - Human-readable detailed report
- **JSON Report** (`*.json`) - Machine-parseable data

### Report Structure

```
================================================================================
ESCANOR FRAMEWORK - MODULE EXECUTION REPORT
================================================================================

REPORT METADATA
----------------------------------------
Report ID:        20250115_143022
Module Name:      ca_validator
Timestamp:        2025-01-15 14:30:22
Operator:         security-team
Execution Time:   2.34 seconds

OPTIONS USED
----------------------------------------
TENANT_ID           : xxx-xxx-xxx
CLIENT_ID           : yyy-yyyy
CLIENT_SECRET       : ***REDACTED***

EXECUTION STATUS
----------------------------------------
Status: ✓ SUCCESS

RESULTS SUMMARY
----------------------------------------
Total Policies Tested    : 3
Total Issues Found       : 2
High Severity Issues     : 1
Medium Severity Issues   : 1
Risk Level              : High

DETAILED FINDINGS
----------------------------------------
[Finding #1]
Name: Require MFA for All Users
Risk Level: Low

Issues:
  [1] Severity: Medium
      Category: Configuration
      Issue: Policy not enforced for guest users
      ...

RECOMMENDATIONS
----------------------------------------
1. Enable Conditional Access for all users
2. Implement MFA requirements
...

================================================================================
END OF REPORT
================================================================================
```

### Managing Reports

```
# List all reports
escanor> reports

# View specific report
escanor> report 1

# Reports are stored in ./results/
ls -la results/
```

### Report Consolidation

Multiple reports can be consolidated into a single assessment document using the `ResultReporter.consolidate_reports()` method.

---

## Creating Custom Modules

### Module Template

```python
#!/usr/bin/env python3
"""
Custom Module Description
"""

from core.base_module import BaseModule
from typing import Dict, Any


class MyCustomModule(BaseModule):
    """Description of your module"""
    
    def __init__(self):
        super().__init__()
        self.name = "my_module"
        self.display_name = "My Custom Module"
        self.category = "custom_category"
        self.description = "What this module does"
        self.author = "Your Name"
        self.version = "1.0.0"
        
        self.options = {
            "TARGET": "",
            "PORT": "443",
        }
        self.required_options = ["TARGET"]
        
        self.option_descriptions = {
            "TARGET": "Target IP or hostname",
            "PORT": "Target port number",
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the module logic"""
        target = self.get_option("TARGET")
        port = self.get_option("PORT")
        
        self.log(f"Starting assessment of {target}:{port}")
        
        # Your logic here
        results = {
            "status": "success",
            "findings": [],
            "summary": {},
            "recommendations": []
        }
        
        return results


__all__ = ['MyCustomModule']
```

### Module Development Best Practices

1. **Inherit from BaseModule**: Always extend the base class
2. **Define Metadata**: Set name, description, author, version
3. **Specify Options**: Clear option names with descriptions
4. **Validate Input**: Use `validate_options()` method
5. **Log Activity**: Use `self.log()` for consistent logging
6. **Return Structured Data**: Follow the standard result format
7. **Handle Errors Gracefully**: Catch exceptions and report clearly

### Adding New Categories

1. Create directory: `modules/new_category/`
2. Add `__init__.py` file
3. Place module files in the directory
4. Module Manager auto-discovers new categories

---

## Entra ID Assessment

Escanor includes specialized modules for Azure Entra ID (formerly Azure AD) security assessments.

### Conditional Access Validator

Tests CA policies for misconfigurations:

```
escanor> use cloud/entra/ca_validator
escanor> set TENANT_ID your-tenant-id
escanor> set CLIENT_ID your-app-id
escanor> set CLIENT_SECRET your-secret
escanor> set POLICY_IDS "policy-1,policy-2"
escanor> run
```

**Checks Performed:**
- Policy state (enabled/disabled)
- MFA enforcement
- Device compliance requirements
- Location-based restrictions
- User scope coverage

### Device Code Flow Simulator

Simulates device code authentication attacks:

```
escanor> execute cloud/entra/device_code_flow TENANT_ID=xxx CLIENT_ID=yyy SIMULATE_ATTACK=True
```

**Capabilities:**
- Legitimate flow simulation
- Attack pattern simulation
- Detection point identification
- MITRE ATT&CK mapping

### Service Principal Assessor

Audits service principals and managed identities:

```
escanor> use cloud/entra/sp_assessment
escanor> set TENANT_ID your-tenant
escanor> set CLIENT_ID your-client
escanor> set INCLUDE_MANAGED_IDENTITIES True
escanor> set CREDENTIAL_AGE_THRESHOLD 90
escanor> run
```

**Assessment Areas:**
- Expired credentials
- Old credentials (configurable threshold)
- Overprivileged role assignments
- Broad permission scopes
- Disabled accounts with active credentials

---

## C2 Framework Integration

Escanor integrates with popular C2 frameworks for coordinated testing.

### Supported Frameworks

1. **Empire** (BC Security)
   - PowerShell-based post-exploitation
   - REST API integration
   
2. **PoshC2** (Nettitude)
   - PowerShell and Python C2
   - Proxy-aware operations
   
3. **Koadic** (OffsecGinger)
   - COM-based post-exploitation
   - Living-off-the-land techniques

### Usage Example

```
escanor> use c2_frameworks/empire_c2
escanor> set EMPIRE_HOST 192.168.1.100
escanor> set EMPIRE_PORT 1337
escanor> set USERNAME admin
escanor> set PASSWORD securepass
escanor> run
```

---

## Troubleshooting

### Common Issues

#### Module Not Found

```
[!] Module not found: module_name
```

**Solution:** 
- Use `list` to see available modules
- Check category path: `category/module_name`
- Use `search` to find modules by keyword

#### AI Not Working

```
[!] AI backend not available
```

**Solution:**
- AI is optional; framework works without it
- To enable: Set `ESCANOR_AI_*` environment variables
- For Ollama: Ensure service is running on configured URL

#### Report Not Generated

```
No report file created
```

**Solution:**
- Check `--no-report` flag wasn't used
- Verify write permissions in `./results/` directory
- Check disk space

#### Module Validation Failed

```
[!] Module validation failed
[!] Missing required option: OPTION_NAME
```

**Solution:**
- Use `show options` to see required fields
- Set all required options with `set OPTION value`

### Getting Help

```
escanor> help
escanor> search <keyword>
```

### Logs and Debugging

Enable verbose output:
```
escanor> run -v
```

Check module source:
```bash
cat modules/category/module_name.py
```

---

## Legal Disclaimer

**IMPORTANT**: Escanor is designed for legitimate security testing only.

- Always obtain proper written authorization before testing
- Only test systems you own or have explicit permission to assess
- Follow applicable laws and regulations
- Adhere to defined scope and rules of engagement
- This tool is provided "as is" without warranty

Unauthorized use of this framework against systems without permission is illegal and may result in criminal prosecution.

---

## Contributing

Contributions welcome! Please follow these guidelines:

1. Fork the repository
2. Create feature branch
3. Follow existing code style
4. Add tests for new modules
5. Update documentation
6. Submit pull request

---

## License

[Add your license information here]

---

## Support

For issues, questions, or contributions:
- GitHub Issues: [link]
- Documentation: `/docs/` directory
- Community: [forum/discord link]

---

**Escanor Framework** - Powered by excellence, forged for security.
