# ☀️ ESCANOR // PURPLE TEAM FRAMEWORK
> **"The sun never sets on Escanor."**  
> *A modular, AI-enhanced offensive security framework for Red, Blue, and Purple teams.*

---

## 🚀 Tactical Overview

**Escanor** is not just another scanner; it is a unified command center for simulating advanced persistent threats (APTs). It bridges the gap between discrete security tools and cohesive attack simulations. By integrating industry-standard frameworks (Empire, PoshC2, Koadic) with cutting-edge Azure/Entra ID tools (TokenTacticsV2, roadtools, MSOLSpray) and privilege escalation utilities (GodPotato, PrintSpoofer), Escanor provides a single interface for end-to-end attack chain execution.

### 💡 Core Capabilities
*   **🧩 Modular Architecture**: Drop-in modules for Recon, Exploitation, C2, Evasion, and Cloud.
*   **🤖 Optional AI Brain**: Embed LLMs (Ollama/OpenAI) for dynamic analysis and report summarization (*fully optional, works standalone*).
*   **📜 Playbook Engine**: Curated attack chains for routine assessments or custom scenarios.
*   **🎯 Precision Execution**: Run individual modules with granular control or execute full playbooks.
*   **📝 Automated Reporting**: Every action generates detailed, standardized TXT and JSON reports in `./results/`.
*   **☁️ Hybrid Cloud/On-Prem**: Seamless transition from Azure Entra ID abuse to On-Prem AD domination.

---

## 🛠️ Integration Matrix

Escanor acts as the orchestration layer for the following battle-tested tools:

| Category | Integrated Tool | Purpose | Escanor Module |
| :--- | :--- | :--- | :--- |
| **C2 Frameworks** | **Empire** (BC-Security) | Post-exploitation agent | `c2_frameworks/empire_c2` |
| | **PoshC2** (Nettitude) | PowerShell/C# C2 | `c2_frameworks/poshc2` |
| | **Koadic** | COM-based C2 | `c2_frameworks/koadic` |
| **Azure/Entra ID** | **TokenTacticsV2** | OAuth token abuse & lateral movement | `cloud/entra/token_tactics` |
| | **roadtools** | Entra ID enumeration & analysis | `cloud/entra/roadtools_enum` |
| | **MSOLSpray** | Password spraying against Azure AD | `cloud/entra/msolspray` |
| | **BARK** | BloodHound Automated Collection | `ad/bark_collector` |
| **Phishing/Proxy** | **Modlishka** | Reverse proxy phishing & MFA bypass | `phishing/modlishka_proxy` |
| **PrivEsc (Win)** | **GodPotato** | Local Privilege Escalation | `exploitation/privesc/godpotato` |
| | **SigmaPotato** | Alternative LPE vector | `exploitation/privesc/sigmapotato` |
| | **PrintSpoofer** | Printer bug exploitation | `exploitation/privesc/printspoofer` |
| **Evasion** | **EDRSilencer** | Disable EDR hooks/drivers | `evasion/edrsilencer` |

---

## ⚡ Quick Start: Operator's Guide

### 1. Installation
Ensure Python 3.9+ is installed. No complex dependencies are required for the core framework.

```bash
git clone https://github.com/YOUR_ORG/Escanor.git
cd Escanor
pip install -r requirements.txt  # Optional: only for AI features and specific libs
```

### 2. Launch the Shell
Enter the interactive command center:
```bash
python3 escanor.py
```

You will be greeted by the Escanor prompt:
```text
      _______  __   __  _______  __    _  ___   _ 
     |       ||  | |  ||   _   ||  |  | ||   | | |
     |    ___||  |_|  ||  |_|  ||   |_| ||   |_| |
     |   | __ |       ||       ||       ||      _|
     |   ||  ||       ||       ||  _    ||     |_ 
     |   |_| ||   _   ||   _   || | |   ||    _  |
     |_______||__| |__||__| |__||_|  |__||___| |_|
     
     [ESCANOR v2.0] :: Purple Team Operations Center
     Type 'help' for commands, 'modules' to list capabilities.

escanor> 
```

### 3. Execution Modes

#### 🎯 Mode A: Targeted Module Execution
Run a specific tool with custom arguments. Ideal for precise testing.

```bash
# Example: Spray passwords against Entra ID
escanor> execute cloud/entra/msolspray USER_FILE=users.txt PASS_FILE=pass.txt TENANT=contoso.onmicrosoft.com --operator "RedTeamAlpha" --notes "Initial access attempt"

# Example: Launch Modlishka for MFA phishing
escanor> execute phishing/modlishka_proxy TARGET_URL=https://office365.com LISTEN_PORT=443 PHISH_DOMAIN=login-secure.com

# Example: Enumerate Azure AD with roadtools
escanor> execute cloud/entra/roadtools_enum METHOD=graph OUTPUT_FORMAT=json
```

#### 📜 Mode B: Playbook Execution
Execute a curated sequence of modules for a specific scenario.

```bash
# List available playbooks
escanor> playbooks

# Run the Azure Breach Simulation
escanor> run playbook azure_breach_simulation --operator "BlueTeamLead" --notes "Q3 Assessment"

# Run the Full Hybrid Attack (Cloud -> OnPrem)
escanor> run playbook ad_cloud_hybrid
```

### 4. Reviewing Results
Escanor automatically generates reports for every execution.

```bash
# List recent reports
escanor> reports

# View the latest report in detail
escanor> report 1

# Reports are saved to ./results/ as both .txt (human-readable) and .json (machine-parseable)
```

---

## 📂 Directory Structure

```text
Escanor/
├── escanor.py              # Main entry point
├── core/                   # Framework engine
│   ├── base_module.py      # Abstract base for all modules
│   ├── module_manager.py   # Dynamic loading & execution
│   ├── interactive_shell.py# CLI interface
│   ├── playbook_engine.py  # YAML playbook parser
│   └── module_result.py    # Standardized result object
├── modules/                # Operational capabilities
│   ├── reconnaissance/     # Nmap, Web scanners
│   ├── exploitation/       # GodPotato, PrintSpoofer
│   ├── c2_frameworks/      # Empire, PoshC2, Koadic wrappers
│   ├── cloud/entra/        # TokenTactics, roadtools, MSOLSpray
│   ├── ad/                 # BARK, BloodHound integrations
│   ├── phishing/           # Modlishka
│   └── evasion/            # EDRSilencer
├── playbooks/              # Curated attack chains
│   ├── azure_breach_simulation.yml
│   ├── ad_cloud_hybrid.yml
│   └── ...
├── utils/
│   └── result_reporter.py  # Report generation logic
├── lib/
│   └── ai_integration.py   # Optional AI logic
├── results/                # Auto-generated reports (TXT/JSON)
└── docs/
    └── COMPLETE_DOCUMENTATION.md
```

---

## 🧠 AI Integration (Optional)

Escanor stands fully functional without AI. However, for enhanced analysis, you can enable LLM support.

**Configuration via Environment Variables:**
```bash
export ESCANOR_AI_PROVIDER="ollama"  # or "openai"
export ESCANOR_AI_MODEL="llama3"     # or "gpt-4o"
export ESCANOR_AI_ENDPOINT="http://localhost:11434" # For Ollama
# export ESCANOR_API_KEY="sk-..."    # For OpenAI
```

**Capabilities when enabled:**
*   **Smart Suggestions**: AI recommends next steps based on module output.
*   **Report Summarization**: Converts technical logs into executive summaries.
*   **Contextual Help**: Explains complex flags or attack vectors in real-time.

---

## 📝 Reporting Standard

Every operation generates a timestamped report in `./results/`.

**Format Example (`results/20231027_143022_msolspray.txt`):**
```text
==============================================================================
ESCANOR OPERATION REPORT
==============================================================================
ID:          OP-20231027-001
Module:      cloud/entra/msolspray
Operator:    RedTeamAlpha
Timestamp:   2023-10-27 14:30:22 UTC
Duration:    4m 12s
Notes:       Initial access attempt against dev tenant
Status:      COMPLETED (3 Valid Credentials Found)
------------------------------------------------------------------------------
EXECUTION LOG:
[+] Target: contoso.onmicrosoft.com
[+] Loaded 500 users, 20 passwords.
[+] SUCCESS: user.jenkins@contoso.onmicrosoft.com : Summer2023!
[+] SUCCESS: svc_backup@contoso.onmicrosoft.com : Backup1234$
[+] FAILED: 498 attempts blocked or invalid.
------------------------------------------------------------------------------
AI ANALYSIS (If Enabled):
"The successful spray indicates weak password policies for service accounts. 
Recommend immediate rotation and implementation of Conditional Access policies."
==============================================================================
```

---

## ⚠️ Legal Disclaimer

**Escanor** is a dual-use security framework intended strictly for authorized security testing, purple teaming exercises, and educational purposes. 
*   **Authorization**: Ensure you have explicit written permission from the owner of any target system before scanning or attacking.
*   **Liability**: The authors and contributors assume no liability for misuse of this software. Use at your own risk.
*   **Compliance**: Adhere to all local, state, and federal laws regarding computer fraud and abuse.

---

## 🤝 Contributing

We welcome new modules, playbooks, and improvements. 
1.  Fork the repository.
2.  Create a new module inheriting from `BaseModule`.
3.  Submit a Pull Request with a test playbook.

**"In the face of absolute power, we remain vigilant."**

---
*Built for the modern Purple Team. Powered by Python. Enhanced by Intelligence.*
