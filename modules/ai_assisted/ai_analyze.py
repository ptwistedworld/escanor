#!/usr/bin/env python3
"""
AI Assistant Module
Uses AI to analyze targets and suggest attack vectors
"""

from typing import Dict, Any
from core.base_module import BaseModule, action


class AIAssistant(BaseModule):
    """AI-powered analysis and recommendation module"""
    
    def __init__(self):
        super().__init__()
        self.name = "ai_analyze"
        self.category = "ai_assisted"
        self.description = "AI-powered target analysis and attack vector suggestions"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        
        self.options = {
            'TARGET': '',
            'CONTEXT': '',
            'OBJECTIVE': 'reconnaissance'
        }
        
        self.required_options = ['TARGET']
        
        self.option_descriptions = {
            'TARGET': 'Target IP, hostname, or URL',
            'CONTEXT': 'Additional context about the target (optional)',
            'OBJECTIVE': 'Assessment objective: reconnaissance, exploitation, or full'
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute AI analysis"""
        if not self.validate_options():
            return {'success': False, 'error': 'Missing required options'}
        
        target = self.options['TARGET']
        context = self.options.get('CONTEXT', '')
        objective = self.options.get('OBJECTIVE', 'reconnaissance')
        
        self.log(f"Starting AI analysis for {target}")
        
        results = {
            'target': target,
            'objective': objective,
            'analysis': {},
            'recommendations': [],
            'suggested_modules': []
        }
        
        print("\n[*] Initiating AI-powered analysis...")
        
        # Import AI integration
        try:
            from lib.ai_integration import AIIntegration
            ai = AIIntegration()
            
            # Build analysis query
            query = f"""Analyze this security assessment target for purple teaming:

Target: {target}
Objective: {objective}
Additional Context: {context if context else 'None provided'}

Provide:
1. Likely attack surface and entry points
2. Recommended testing approach (offensive and defensive)
3. Specific Escanor modules to use (list module names)
4. Common vulnerabilities for this type of target
5. Detection opportunities for blue team

Format response clearly with sections."""

            print("[*] Querying AI engine...")
            analysis = ai.process_command(query)
            
            results['analysis'] = {
                'full_response': analysis,
                'ai_provider': ai.provider,
                'model': ai.model
            }
            
            # Extract module suggestions (simplified parsing)
            lines = analysis.split('\n')
            for line in lines:
                line_lower = line.lower().strip()
                if 'port_scan' in line_lower:
                    results['suggested_modules'].append('reconnaissance/port_scan')
                if 'web_scan' in line_lower:
                    results['suggested_modules'].append('reconnaissance/web_scan')
                if 'vuln_scan' in line_lower:
                    results['suggested_modules'].append('reconnaissance/vuln_scan')
            
            # Remove duplicates
            results['suggested_modules'] = list(set(results['suggested_modules']))
            
            print(f"\n[+] AI Analysis Complete")
            print(f"    Provider: {ai.provider}/{ai.model}")
            print(f"    Suggested modules: {len(results['suggested_modules'])}")
            
            print("\n" + "="*60)
            print("AI ANALYSIS RESULTS:")
            print("="*60)
            print(analysis[:2000])  # Print first 2000 chars
            if len(analysis) > 2000:
                print("\n... [truncated, see full results in output]")
            print("="*60)
            
        except Exception as e:
            error_msg = f"[!] AI analysis failed: {e}"
            print(error_msg)
            results['error'] = error_msg
            
            # Fallback recommendations
            print("\n[*] Providing basic recommendations without AI:")
            results['recommendations'] = [
                "Start with reconnaissance/port_scan to identify open ports",
                "Use reconnaissance/web_scan if web services are found",
                "Run reconnaissance/vuln_scan on identified services",
                "Document all findings for both red and blue teams"
            ]
            results['suggested_modules'] = [
                'reconnaissance/port_scan',
                'reconnaissance/web_scan',
                'reconnaissance/vuln_scan'
            ]
            
            for rec in results['recommendations']:
                print(f"    → {rec}")
        
        results['success'] = True
        self.results = results
        return results
