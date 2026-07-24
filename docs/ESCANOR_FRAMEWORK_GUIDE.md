# 🦁 ESCANOR FRAMEWORK
## The Lion's Den of Purple Teaming

> *"Like the sun at its zenith, Escanor brings overwhelming light to the darkest corners of your security posture."*

---

## 📖 TABLE OF CONTENTS

```
├── 1. WHAT IS ESCANOR?
├── 2. GETTING STARTED
├── 3. THE ARSENAL (MODULES)
├── 4. INTERACTIVE SHELL
├── 5. PLAYBOOKS
├── 6. REPORTING ENGINE
├── 7. AI INTEGRATION (OPTIONAL)
├── 8. MODULE DEVELOPMENT
├── 9. INTEGRATED TOOLS REFERENCE
└── 10. TROUBLESHOOTING
```

---

## 1. 🌟 WHAT IS ESCANOR?

**Escanor** is a **purple teaming powerhouse** designed for modern cybersecurity teams who need to:

- 🔴 **Attack** like a red team
- 🔵 **Defend** like a blue team  
- 🟣 **Validate** like a purple team

### Core Principles

| Principle | Description |
|-----------|-------------|
| 🎯 MODULARITY | Plug-and-play architecture |
| 🔄 FLEXIBILITY | Works standalone or with AI |
| 📊 STANDARDIZATION | Consistent outputs |
| ☁️ CLOUD-NATIVE | Built-in Entra ID support |
| 🔒 RESPONSIBLE | Authorized testing only |

---

## 2. 🚀 GETTING STARTED

### Quick Install

```bash
git clone https://github.com/your-org/escanor-framework.git
cd escanor-framework
pip install -r requirements.txt
python3 escanor.py --help
```

### Quick Launch

```bash
# Interactive Shell
python3 escanor.py

# Direct Module
python3 escanor.py -m reconnaissance/port_scan

# Playbook
python3 escanor.py -p purple_team
```

---

## 3. 🗡️ THE ARSENAL (MODULES)

**Total:** 19 modules across 9 categories

### Module Categories

| Category | Modules | Purpose |
|----------|---------|---------|
| 📡 Reconnaissance | 3 | Network/web scanning |
| 💥 Exploitation | 3 | Privilege escalation |
| 🎮 C2 Frameworks | 3 | Command & control |
| ☁️ Cloud/Entra | 7 | Azure AD assessment |
| 👻 Evasion | 1 | EDR bypass testing |
| 🤖 AI-Assisted | 1 | Intelligent analysis |
| 📦 Persistence | * | Extensible |
| ↔️ Lateral Movement | * | Extensible |
| 📤 Exfiltration | * | Extensible |

### Key Modules

#### Cloud/Entra ID (7 modules)
- `ca_validator` - Conditional Access testing
- `device_code_flow` - Auth flow simulation
- `token_tactics` - JWT manipulation (ref: TokenTacticsV2)
- `modlishka` - Reverse proxy phishing (ref: Modlishka)
- `msolspray` - Password spraying (ref: MSOLSpray)
- `roadtools` - Azure AD enum (ref: ROADtools)
- `bark` - BloodHound collection (ref: BARK)
- `sp_assessment` - Service Principal audit

#### Exploitation (3 modules)
- `godpotato` - Windows privesc (ref: GodPotato)
- `sigmapotato` - Advanced potato (ref: SigmaPotato)
- `printspoofer` - Spooler abuse (ref: PrintSpoofer)

#### C2 Frameworks (3 modules)
- `empire_c2` - PowerShell C2 (ref: Empire)
- `poshc2` - Python/PS C2 (ref: PoshC2)
- `koadic` - COM-based C2 (ref: Koadic)

---

## 4. 🖥️ INTERACTIVE SHELL

### Essential Commands

| Command | Description | Example |
|---------|-------------|---------|
| `use` | Load module | `use cloud/entra/ca_validator` |
| `run` | Execute | `run -v --operator "alice"` |
| `execute` | One-liner | `execute recon/port_scan TARGET=10.0.0.1` |
| `set` | Configure | `set PORTS 1-1000` |
| `list` | Browse | `list cloud/entra` |
| `search` | Find | `search potato` |
| `playbook` | Run playbook | `playbook purple_team` |
| `reports` | List reports | `reports` |
| `ai` | AI query | `ai "suggest next steps"` |

### Run Options

```bash
run [-v] [--no-report] [--operator <name>] [--notes "<text>"]
```

---

## 5. 📚 PLAYBOOKS

### Pre-Built Playbooks (8 total)

| Playbook | Modules | Purpose |
|----------|---------|---------|
| `basic_recon` | 3 | Initial scanning |
| `web_app_assessment` | 4 | Web security |
| `purple_team` | 5 | Full exercise |
| `c2_framework_coordination` | 3 | C2 testing |
| `edr_evasion_testing` | 2 | EDR validation |
| `full_attack_simulation` | 8 | End-to-end |
| `entra_id_assessment` | 8 | Azure audit |
| `advanced_persistent_threat` | Phased | APT sim |

### Create Custom Playbook

```yaml
name: "My Assessment"
description: "Custom workflow"
steps:
  - module: "reconnaissance/port_scan"
    options:
      TARGET: "10.0.0.1"
    enabled: true
```

---

## 6. 📊 REPORTING ENGINE

Every execution generates:
- **TXT report** - Human-readable
- **JSON report** - Machine-parseable

### Report Features
- Automatic generation
- Sensitive data redaction
- Operator attribution
- Timestamp tracking
- Standardized format

### Location
```
/workspace/results/
├── YYYYMMDD_HHMMSS_module.txt
└── YYYYMMDD_HHMMSS_module.json
```

---

## 7. 🤖 AI INTEGRATION (OPTIONAL)

**AI is completely optional** - framework works without it.

### Providers
- Ollama (local)
- OpenAI GPT-4/3.5
- Custom endpoints

### Configuration
```bash
export ESCANOR_AI_PROVIDER=ollama
export ESCANOR_AI_URL=http://localhost:11434
export ESCANOR_AI_MODEL=llama3.2
```

---

## 8. 🔨 MODULE DEVELOPMENT

### Base Structure

```python
from core.base_module import BaseModule

class MyModule(BaseModule):
    def __init__(self):
        super().__init__(
            name="my_module",
            category="my_category",
            description="What it does",
            options={"TARGET": {"required": True}}
        )
    
    def execute(self):
        # Your logic
        return result
```

---

## 9. 🔗 INTEGRATED TOOLS REFERENCE

### External Tools Integrated

| Tool | Reference | Category |
|------|-----------|----------|
| TokenTacticsV2 | github.com/f-bader/TokenTacticsV2 | Cloud |
| Modlishka | github.com/drk1wi/Modlishka | Cloud |
| BARK | github.com/BloodHoundAD/BARK | Cloud |
| ROADtools | github.com/dirkjanm/roadtools | Cloud |
| MSOLSpray | github.com/dafthack/MSOLSpray | Cloud |
| GodPotato | github.com/BeichenDream/GodPotato | Exploit |
| SigmaPotato | github.com/tylerdotrar/SigmaPotato | Exploit |
| PrintSpoofer | github.com/itm4n/PrintSpoofer | Exploit |
| Empire | github.com/BC-SECURITY/Empire | C2 |
| PoshC2 | github.com/nettitude/PoshC2 | C2 |
| Koadic | github.com/offsecginger/koadic | C2 |
| EDRSilencer | github.com/netero1010/EDRSilencer | Evasion |

### Inspiration
- **KittySploit** - github.com/SIA-IOTechnology/Kittysploit-framework

---

## 10. 🔧 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Module not found | Run `reload`, check spelling |
| AI not working | Verify env vars, AI is optional |
| No report | Check `--no-report` flag |
| Permission denied | Check privileges |

---

## QUICK REFERENCE

```
LAUNCH:
  python3 escanor.py              # Shell
  python3 escanor.py -m <module>  # Direct
  python3 escanor.py -p <playbook># Playbook

ESSENTIAL COMMANDS:
  use <module>        # Load
  run                 # Execute
  execute <m> opt=v   # One-liner
  set <opt> <val>     # Configure
  list                # Browse
  search <term>       # Find
  reports             # List reports
```

---

## ACKNOWLEDGMENTS

Escanor integrates tools from amazing open-source projects:
- TokenTacticsV2, Modlishka, BARK, ROADtools, MSOLSpray
- GodPotato, SigmaPotato, PrintSpoofer
- Empire, PoshC2, Koadic
- EDRSilencer
- Inspired by KittySploit

---

🦁 *"The lion does not concern himself with the opinions of sheep."*

**Escanor Framework v2.0.0 - Solar Flare Edition**
