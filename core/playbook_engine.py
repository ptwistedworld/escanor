#!/usr/bin/env python3
"""
Playbook Engine
Handles execution of curated module sequences for routine tasks
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PlaybookEngine:
    """Manages and executes playbooks"""
    
    def __init__(self, module_manager):
        self.module_manager = module_manager
        self.playbook_path = Path(__file__).parent.parent / "playbooks"
        self.playbooks: Dict[str, Dict] = {}
        self.load_playbooks()
    
    def load_playbooks(self) -> None:
        """Load all playbooks from the playbooks directory"""
        if not self.playbook_path.exists():
            print(f"[!] Playbooks directory not found: {self.playbook_path}")
            return
        
        for playbook_file in self.playbook_path.glob("*.yaml"):
            try:
                with open(playbook_file, 'r') as f:
                    playbook_data = yaml.safe_load(f)
                    if playbook_data:
                        playbook_name = playbook_file.stem
                        self.playbooks[playbook_name] = playbook_data
            except Exception as e:
                print(f"[!] Error loading playbook {playbook_file}: {e}")
        
        # Also support JSON format
        for playbook_file in self.playbook_path.glob("*.json"):
            try:
                with open(playbook_file, 'r') as f:
                    playbook_data = json.load(f)
                    if playbook_data:
                        playbook_name = playbook_file.stem
                        self.playbooks[playbook_name] = playbook_data
            except Exception as e:
                print(f"[!] Error loading playbook {playbook_file}: {e}")
    
    def list_playbooks(self) -> List[str]:
        """List all available playbooks"""
        return list(self.playbooks.keys())
    
    def get_playbook_info(self, playbook_name: str) -> Optional[Dict]:
        """Get information about a specific playbook"""
        if playbook_name in self.playbooks:
            pb = self.playbooks[playbook_name]
            return {
                'name': pb.get('name', playbook_name),
                'description': pb.get('description', ''),
                'author': pb.get('author', 'Unknown'),
                'modules_count': len(pb.get('steps', [])),
                'created': pb.get('created', 'Unknown')
            }
        return None
    
    def execute_playbook(self, playbook_name: str, 
                        options: Optional[Dict] = None,
                        verbose: bool = False) -> Dict[str, Any]:
        """Execute a playbook
        
        Playbook steps can now specify actions for fine-grained control:
        
        steps:
          - module: "c2_frameworks/koadic"
            action: "generate_stager"  # Execute specific action
            options:
              STAGER_TYPE: "js/mshta"
            enabled: true
        """
        if playbook_name not in self.playbooks:
            print(f"[!] Playbook not found: {playbook_name}")
            print("[*] Use 'playbook list' to see available playbooks")
            return {'success': False, 'error': 'Playbook not found'}
        
        playbook = self.playbooks[playbook_name]
        results = {
            'playbook': playbook_name,
            'started_at': datetime.now().isoformat(),
            'steps_results': [],
            'success': True
        }
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"Executing Playbook: {playbook.get('name', playbook_name)}")
            print(f"Description: {playbook.get('description', 'No description')}")
            print(f"{'='*60}\n")
        
        steps = playbook.get('steps', [])
        
        for i, step in enumerate(steps, 1):
            module_name = step.get('module')
            step_action = step.get('action')  # New: support for actions
            step_options = step.get('options', {})
            enabled = step.get('enabled', True)
            
            if not enabled:
                if verbose:
                    print(f"\n[Step {i}/{len(steps)}] SKIPPED: {module_name}")
                continue
            
            # Merge global options with step options
            merged_options = {**options} if options else {}
            merged_options.update(step_options)
            
            if verbose:
                action_text = f" (action: {step_action})" if step_action else ""
                print(f"\n[Step {i}/{len(steps)}] Running: {module_name}{action_text}")
            
            # Execute the module with optional action
            result = self.module_manager.run_module(
                module_name, 
                options=merged_options,
                action=step_action,  # Pass action if specified
                verbose=verbose
            )
            
            results['steps_results'].append({
                'step': i,
                'module': module_name,
                'action': step_action,
                'result': result,
                'success': result is not None
            })
            
            if result is None:
                results['success'] = False
                
                # Check if this step is critical
                if step.get('critical', False):
                    if verbose:
                        print(f"[!] Critical step failed. Aborting playbook.")
                    results['aborted'] = True
                    break
            
            if verbose and result:
                print(f"[+] Step {i} completed successfully")
        
        results['completed_at'] = datetime.now().isoformat()
        
        if verbose:
            print(f"\n{'='*60}")
            if results['success']:
                print(f"[+] Playbook '{playbook_name}' completed successfully!")
            else:
                print(f"[!] Playbook '{playbook_name}' completed with errors")
            print(f"{'='*60}\n")
        
        return results
    
    def create_playbook(self, name: str, description: str, 
                       steps: List[Dict], author: str = "Escanor Team") -> bool:
        """Create a new playbook"""
        playbook_data = {
            'name': name,
            'description': description,
            'author': author,
            'created': datetime.now().isoformat(),
            'version': '1.0.0',
            'steps': steps
        }
        
        playbook_file = self.playbook_path / f"{name.lower().replace(' ', '_')}.yaml"
        
        try:
            with open(playbook_file, 'w') as f:
                yaml.dump(playbook_data, f, default_flow_style=False, sort_keys=False)
            
            self.playbooks[name.lower().replace(' ', '_')] = playbook_data
            print(f"[+] Playbook created: {playbook_file}")
            return True
        except Exception as e:
            print(f"[!] Error creating playbook: {e}")
            return False
    
    def validate_playbook(self, playbook_name: str) -> Dict[str, Any]:
        """Validate a playbook structure"""
        if playbook_name not in self.playbooks:
            return {'valid': False, 'errors': ['Playbook not found']}
        
        playbook = self.playbooks[playbook_name]
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['name', 'description', 'steps']
        for field in required_fields:
            if field not in playbook:
                errors.append(f"Missing required field: {field}")
        
        # Validate steps
        steps = playbook.get('steps', [])
        if not steps:
            warnings.append("Playbook has no steps")
        
        for i, step in enumerate(steps):
            if 'module' not in step:
                errors.append(f"Step {i+1}: Missing 'module' field")
            else:
                # Check if module exists
                module = self.module_manager.get_module(step['module'])
                if not module:
                    errors.append(f"Step {i+1}: Module not found: {step['module']}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
