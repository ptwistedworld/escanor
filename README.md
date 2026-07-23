# Escanor Framework

## Advanced Purple Teaming Framework

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

**Escanor** is an advanced, AI-powered purple teaming framework designed for cybersecurity teams to conduct comprehensive security assessments, penetration testing, and defensive analysis. Inspired by modern frameworks like KittySploit, Escanor enhances capabilities with modular architecture, playbook automation, and integrated AI assistance.

---

## 🚀 Features

### Core Capabilities
- **Modular Architecture**: Easily extendable module system organized by category
- **Interactive Shell**: Intuitive command-line interface with contextual help
- **Playbook Engine**: Curated module sequences for routine assessment tasks
- **AI Integration**: Smart analysis powered by Ollama, OpenAI, or other LLM backends
- **Purple Teaming**: Balanced offensive and defensive perspectives

### Module Categories
- **Reconnaissance**: Port scanning, web enumeration, vulnerability detection
- **Exploitation**: Safe exploitation modules for authorized testing
- **Persistence**: Post-exploitation persistence mechanisms (simulation)
- **Lateral Movement**: Network pivoting and movement simulation
- **Exfiltration**: Data exfiltration path analysis
- **AI-Assisted**: Intelligent analysis and recommendations
- **C2 Frameworks**: Integration with Empire, PoshC2, and Koadic
- **Evasion**: EDR/AV bypass techniques via EDRSilencer

### Key Features
1. **Easy Module Onboarding**: Create new modules by inheriting from `BaseModule`
2. **Template Playbooks**: Pre-built assessment workflows
3. **AI-Powered Insights**: Automated analysis and recommendations
4. **Comprehensive Logging**: Detailed operation tracking
5. **Extensible Design**: Plugin-friendly architecture

---

## 📋 Requirements

- Python 3.8+
- Linux/macOS/Windows (with WSL)
- Optional: Ollama or OpenAI API for AI features

### Dependencies

```bash
pip install pyyaml requests
```

For AI features:
- **Ollama** (local): Install from [ollama.ai](https://ollama.ai)
- **OpenAI** (cloud): Set `ESCANOR_AI_API_KEY` environment variable

---

## 🛠️ Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/escanor.git
cd escanor

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x escanor.py

# Run the framework
python3 escanor.py
```

### Environment Configuration (Optional)

```bash
# For Ollama (default)
export ESCANOR_AI_PROVIDER=ollama
export ESCANOR_AI_URL=http://localhost:11434
export ESCANOR_AI_MODEL=llama3.2

# For OpenAI
export ESCANOR_AI_PROVIDER=openai
export ESCANOR_AI_API_KEY=your-api-key-here

# For C2 Frameworks
export EMPIRE_HOST=localhost
export EMPIRE_PORT=1337
export POSHC2_DATABASE=/var/lib/poshc2/poshc2.db
export KOADIC_PATH=/opt/koadic
export EDRSILENCER_PATH=/opt/EDRSilencer
```

---

## 📖 Usage

### Interactive Shell

```bash
python3 escanor.py
```

Once in the shell:

```
escanor> help          # Show available commands
escanor> list          # List all modules
escanor> use reconnaissance/port_scan
escanor:reconnaissance/port_scan> set TARGET 192.168.1.1
escanor:reconnaissance/port_scan> set PORTS 1-1000
escanor:reconnaissance/port_scan> run
escanor:reconnaissance/port_scan> back
escanor> playbook basic_recon
escanor> ai "analyze target 192.168.1.1"
escanor> exit
```

### Command-Line Mode

```bash
# List modules
python3 escanor.py --list-modules

# List playbooks
python3 escanor.py --list-playbooks

# Run a specific module
python3 escanor.py --module reconnaissance/port_scan --verbose

# Execute a playbook
python3 escanor.py --playbook basic_recon --verbose

# AI-assisted query
python3 escanor.py --ai "What are common web vulnerabilities?"
```

---

## 📁 Project Structure

```
escanor/
├── escanor.py          # Main entry point
├── core/                    # Core framework components
│   ├── __init__.py
│   ├── base_module.py       # Base module class
│   ├── module_manager.py    # Module loading & execution
│   ├── interactive_shell.py # CLI interface
│   └── playbook_engine.py   # Playbook execution
├── modules/                 # Security modules
│   ├── reconnaissance/      # Recon modules
│   │   ├── port_scan.py
│   │   ├── web_scan.py
│   │   └── vuln_scan.py
│   ├── exploitation/        # Exploitation modules
│   ├── persistence/         # Persistence modules
│   ├── lateral_movement/    # Lateral movement modules
│   ├── exfiltration/        # Exfiltration modules
│   ├── ai_assisted/         # AI-powered modules
│   │   └── ai_analyze.py
│   ├── c2_frameworks/       # C2 Framework integrations
│   │   ├── empire_c2.py     # Empire C2 integration
│   │   ├── poshc2.py        # PoshC2 integration
│   │   └── koadic.py        # Koadic integration
│   └── evasion/             # EDR/AV evasion
│       └── edrsilencer.py   # EDRSilencer integration
├── playbooks/               # Assessment playbooks
│   ├── basic_recon.yaml
│   ├── web_app_assessment.yaml
│   ├── purple_team.yaml
│   ├── c2_framework_coordination.yaml
│   ├── edr_evasion_testing.yaml
│   └── full_attack_simulation.yaml
├── lib/                     # Library modules
│   ├── __init__.py
│   └── ai_integration.py    # AI backend integration
├── utils/                   # Utility functions
├── docs/                    # Documentation
└── requirements.txt         # Dependencies
```

---

## 🔧 Creating Custom Modules

### Module Template

```python
#!/usr/bin/env python3
"""
Your Module Description
"""

from typing import Dict, Any
from core.base_module import BaseModule


class YourModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "your_module"
        self.category = "your_category"
        self.description = "Module description"
        self.author = "Your Name"
        self.version = "1.0.0"
        
        self.options = {
            'TARGET': '',
            'OPTION2': 'default_value'
        }
        
        self.required_options = ['TARGET']
    
    def run(self) -> Dict[str, Any]:
        if not self.validate_options():
            return {'success': False, 'error': 'Missing required options'}
        
        # Your module logic here
        target = self.options['TARGET']
        
        results = {
            'target': target,
            'success': True
        }
        
        return results
```

### Adding Your Module

1. Create the file in the appropriate category folder
2. Ensure the class name matches the filename
3. The module will be auto-loaded on framework start

---

## 📚 Playbooks

Playbooks automate multi-module assessment workflows.

### Example Playbook (YAML)

```yaml
name: "Basic Reconnaissance"
description: "Initial reconnaissance playbook"
author: "Your Team"
version: "1.0.0"

steps:
  - module: "reconnaissance/port_scan"
    options:
      PORTS: "1-1000"
    enabled: true
    critical: true
    
  - module: "reconnaissance/web_scan"
    options:
      PORT: "80"
    enabled: true
    critical: false
```

### Available Playbooks

| Playbook | Description | Use Case |
|----------|-------------|----------|
| `basic_recon` | Basic reconnaissance | Initial target assessment |
| `web_app_assessment` | Web app security | Comprehensive web testing |
| `purple_team` | Full purple team | Red + Blue team exercises |
| `c2_framework_coordination` | C2 framework integration | Coordinated Empire, PoshC2, Koadic operations |
| `edr_evasion_testing` | EDR/AV evasion testing | Test bypass techniques with EDRSilencer |
| `full_attack_simulation` | End-to-end attack simulation | Complete purple team exercise |

---

## 🤖 AI Integration

Escanor supports multiple AI backends for intelligent analysis.

### Supported Providers

1. **Ollama** (Default - Local)
   - Free, runs locally
   - Supports various models (llama3.2, mistral, etc.)
   - No API costs

2. **OpenAI** (Cloud)
   - GPT-4, GPT-3.5-turbo
   - Requires API key
   - Higher accuracy

### AI Capabilities

- **Target Analysis**: Automated attack surface identification
- **Module Recommendations**: Suggest next steps based on findings
- **Results Interpretation**: Explain findings and severity
- **Report Generation**: Create professional assessment reports
- **Technique Explanation**: Learn about attack/defense techniques

### Example AI Commands

```
escanor> ai "Analyze this target: 192.168.1.1, it's a web server"
escanor> ai "What modules should I use for Active Directory assessment?"
escanor> ai "Explain SQL injection detection methods"
```

---

## 🎯 Purple Teaming Workflow

### Typical Engagement

1. **Planning Phase**
   ```
   escanor> ai "Help me plan an assessment for a financial institution"
   ```

2. **Reconnaissance**
   ```
   escanor> playbook basic_recon
   ```

3. **Analysis**
   ```
   escanor> use ai_assisted/ai_analyze
   escanor:ai_assisted/ai_analyze> set TARGET 192.168.1.1
   escanor:ai_assisted/ai_analyze> run
   ```

4. **Exploitation (Authorized)**
   ```
   escanor> use exploitation/[module]
   ```

5. **Reporting**
   ```
   escanor> ai "Generate a report from these findings: [paste results]"
   ```

---

## ⚠️ Legal Disclaimer

**Escanor is designed for legitimate security testing only.**

- Only use against systems you own or have explicit written authorization to test
- Unauthorized access to computer systems is illegal
- The developers are not responsible for misuse of this framework
- Always follow your organization's policies and applicable laws

---

## 📝 Documentation

See the `/docs` directory for detailed documentation:

- [Architecture Guide](docs/architecture.md)
- [Module Development](docs/module_development.md)
- [API Reference](docs/api_reference.md)
- [Playbook Guide](docs/playbooks.md)
- [AI Integration](docs/ai_integration.md)

---

## 🔗 Related Projects

Inspired by and compatible with concepts from:
- [KittySploit Framework](https://github.com/SIA-IOTechnology/Kittysploit-framework)
- [Empire C2](https://github.com/BC-SECURITY/Empire) - Post-exploitation framework
- [PoshC2](https://github.com/nettitude/PoshC2) - PowerShell and C# post-exploitation
- [Koadic](https://github.com/offsecginger/koadic) - COM-based post-exploitation
- [EDRSilencer](https://github.com/netero1010/EDRSilencer) - EDR/AV evasion techniques
- Metasploit Framework
- Covenant C2

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute
- Add new modules
- Improve existing modules
- Create playbooks
- Enhance documentation
- Report bugs and suggest features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- Escanor Development Team

---

## 🙏 Acknowledgments

- The cybersecurity community
- Open-source security tool developers
- Purple team practitioners worldwide

---

**Happy (Ethical) Hacking! 🛡️⚔️**
