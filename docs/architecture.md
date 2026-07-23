# Escanor Architecture Guide

## Overview

Escanor is built on a modular, extensible architecture designed for purple team operations.

## Core Components

### 1. Main Entry Point (`escanor.py`)
- Command-line argument parsing
- Initializes core components
- Launches interactive shell or runs single commands

### 2. Core Framework (`/core`)

#### BaseModule (`base_module.py`)
Abstract base class that all modules must inherit from:
- Standard interface for options, execution, and results
- Built-in validation and logging
- Metadata management (name, author, version)

#### ModuleManager (`module_manager.py`)
Dynamic module loading system:
- Auto-discovers modules in `/modules` directory
- Supports hot-reloading
- Case-insensitive module lookup
- Category-based organization

#### InteractiveShell (`interactive_shell.py`)
Rich CLI interface:
- Context-aware prompts
- Tab completion ready
- Command history support
- Color-coded output

#### PlaybookEngine (`playbook_engine.py`)
Workflow automation:
- YAML/JSON playbook support
- Sequential module execution
- Conditional step execution
- Result aggregation

### 3. Modules (`/modules`)

Organized by operational category:
- **reconnaissance**: Information gathering
- **exploitation**: Safe exploitation (authorized use)
- **persistence**: Post-exploitation simulation
- **lateral_movement**: Network pivoting
- **exfiltration**: Data movement analysis
- **ai_assisted**: AI-powered operations

### 4. Libraries (`/lib`)

#### AIIntegration (`ai_integration.py`)
Multi-provider AI support:
- Ollama (local, default)
- OpenAI (cloud)
- Extensible to other providers
- Context-aware prompting

### 5. Playbooks (`/playbooks`)

Pre-built assessment workflows in YAML format.

## Data Flow

```
User Input → InteractiveShell → ModuleManager → Module Execution
                ↓                              ↓
         PlaybookEngine                  Results
                ↓                              ↓
         Module Sequence              AI Analysis
```

## Extension Points

1. **New Modules**: Inherit from `BaseModule`
2. **New Categories**: Create folder in `/modules`
3. **AI Providers**: Extend `AIIntegration` class
4. **Playbooks**: Add YAML files to `/playbooks`

## Security Considerations

- Authorization checks before execution
- Input validation on all options
- Secure credential handling
- Audit logging capability
