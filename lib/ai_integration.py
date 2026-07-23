#!/usr/bin/env python3
"""
AI Integration Module
Provides AI-powered capabilities for smarter operations
Supports multiple AI backends: OpenAI, Ollama, Local LLMs
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class AIIntegration:
    """AI integration for enhanced operations"""
    
    def __init__(self):
        self.provider = os.getenv('ESCANOR_AI_PROVIDER', 'ollama')
        self.api_key = os.getenv('ESCANOR_AI_API_KEY', '')
        self.api_url = os.getenv('ESCANOR_AI_URL', 'http://localhost:11434')
        self.model = os.getenv('ESCANOR_AI_MODEL', 'llama3.2')
        self.enabled = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if AI backend is available"""
        # For now, assume available - in production, would ping the service
        return True
    
    def process_command(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Process a natural language command using AI
        Returns AI-generated response or suggestion
        """
        if not self.enabled:
            return "[!] AI backend not available. Configure ESCANOR_AI_* environment variables."
        
        # Build prompt with context
        system_prompt = """You are an expert cybersecurity assistant integrated into Escanor, 
a purple teaming framework. Help users with security assessments, penetration testing, 
and defensive strategies. Always emphasize ethical use and proper authorization."""

        user_prompt = self._build_prompt(query, context)
        
        try:
            if self.provider == 'ollama':
                response = self._query_ollama(system_prompt, user_prompt)
            elif self.provider == 'openai':
                response = self._query_openai(system_prompt, user_prompt)
            else:
                response = self._query_generic(system_prompt, user_prompt)
            
            return response
        except Exception as e:
            return f"[!] AI processing error: {e}"
    
    def _build_prompt(self, query: str, context: Optional[Dict] = None) -> str:
        """Build the prompt with optional context"""
        prompt = f"User Query: {query}\n\n"
        
        if context:
            prompt += "Context:\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
        
        prompt += "\nProvide a concise, actionable response relevant to cybersecurity operations."
        return prompt
    
    def _query_ollama(self, system: str, user: str) -> str:
        """Query Ollama local LLM"""
        try:
            import requests
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "stream": False
            }
            
            response = requests.post(
                f"{self.api_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('message', {}).get('content', 'No response from AI')
            else:
                return f"[!] Ollama API error: {response.status_code}"
                
        except ImportError:
            return "[!] 'requests' library not installed. Run: pip install requests"
        except requests.exceptions.ConnectionError:
            return "[!] Cannot connect to Ollama. Ensure it's running on the configured URL."
        except Exception as e:
            return f"[!] Ollama query failed: {e}"
    
    def _query_openai(self, system: str, user: str) -> str:
        """Query OpenAI API"""
        if not self.api_key:
            return "[!] OpenAI API key not configured. Set ESCANOR_AI_API_KEY"
        
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            else:
                return f"[!] OpenAI API error: {response.status_code}"
                
        except ImportError:
            return "[!] 'requests' library not installed."
        except Exception as e:
            return f"[!] OpenAI query failed: {e}"
    
    def _query_generic(self, system: str, user: str) -> str:
        """Generic fallback for other providers"""
        # This could be extended for other providers like Anthropic, Google, etc.
        return "[!] Selected AI provider not fully implemented. Use 'ollama' or 'openai'."
    
    def suggest_modules(self, objective: str) -> List[str]:
        """Get AI suggestions for modules based on objective"""
        query = f"""Given this objective: '{objective}'
        
Suggest which Escanor modules would be most appropriate to use.
List module names only, one per line, in recommended execution order.
Consider both offensive and defensive perspectives for purple teaming."""
        
        response = self.process_command(query)
        
        # Parse module names from response
        suggested = []
        for line in response.split('\n'):
            line = line.strip().lower()
            if line and not line.startswith(('[', '#', '-')):
                # Clean up the line
                cleaned = line.replace('*', '').replace('.', '').strip()
                if cleaned:
                    suggested.append(cleaned)
        
        return suggested[:10]  # Return top 10 suggestions
    
    def analyze_results(self, results: Dict[str, Any]) -> str:
        """Analyze module results and provide insights"""
        query = f"""Analyze these security assessment results and provide:
1. Key findings summary
2. Risk level assessment (Low/Medium/High/Critical)
3. Recommended next steps
4. Defensive recommendations

Results:
{json.dumps(results, indent=2, default=str)}
"""
        return self.process_command(query)
    
    def generate_report(self, assessment_data: Dict[str, Any]) -> str:
        """Generate a comprehensive report from assessment data"""
        query = f"""Generate a professional cybersecurity assessment report including:
- Executive Summary
- Methodology
- Findings (with severity ratings)
- Technical Details
- Recommendations
- Conclusion

Assessment Data:
{json.dumps(assessment_data, indent=2, default=str)}

Format the report in markdown."""
        
        return self.process_command(query)
    
    def explain_technique(self, technique: str) -> str:
        """Explain a cybersecurity technique or concept"""
        query = f"""Explain the following cybersecurity technique/concept:
'{technique}'

Include:
- What it is
- How it works
- When to use it (legitimate purposes)
- Detection methods
- Mitigation strategies
- MITRE ATT&CK mapping if applicable"""
        
        return self.process_command(query)
    
    def validate_authorization(self, target: str) -> bool:
        """
        Prompt user to confirm authorization for target
        Returns True if confirmed, raises exception otherwise
        """
        print(f"\n{'='*60}")
        print("⚠️  AUTHORIZATION REQUIRED ⚠️")
        print(f"{'='*60}")
        print(f"Target: {target}")
        print("\nBefore proceeding, confirm you have:")
        print("  ✓ Written authorization from the target owner")
        print("  ✓ Proper legal clearance for this assessment")
        print("  ✓ Defined scope and rules of engagement")
        print("\nThis framework is for LEGITIMATE security testing only.")
        print(f"{'='*60}\n")
        
        confirm = input("Type 'AUTHORIZED' to confirm: ").strip()
        return confirm.upper() == 'AUTHORIZED'


# Convenience function for quick AI queries
def ai_query(query: str) -> str:
    """Quick AI query without instantiating the class"""
    ai = AIIntegration()
    return ai.process_command(query)
