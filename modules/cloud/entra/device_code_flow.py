#!/usr/bin/env python3
"""
Entra ID Device Code Flow Simulation Module
Simulates device code authentication flow for testing and validation
"""

from core.base_module import BaseModule, action
from typing import Dict, Any
import json
import time
from datetime import datetime


class EntraDeviceCodeFlow(BaseModule):
    """Simulate and test Device Code authentication flow in Entra ID"""
    
    def __init__(self):
        super().__init__()
        self.name = "device_code_flow"
        self.display_name = "Device Code Flow Simulator"
        self.category = "cloud/entra"
        self.description = "Simulate device code authentication flow to test detection and response"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.options = {
            "TENANT_ID": "",
            "CLIENT_ID": "",
            "RESOURCE": "https://graph.microsoft.com",
            "SIMULATE_ATTACK": "False",
            "TARGET_USER": "",
            "DURATION": "300",
        }
        self.required_options = ["TENANT_ID", "CLIENT_ID"]
        self.option_descriptions = {
            "TENANT_ID": "Azure Entra ID Tenant ID",
            "CLIENT_ID": "Application Client ID",
            "RESOURCE": "Target resource for authentication (default: Microsoft Graph)",
            "SIMULATE_ATTACK": "Set to True to simulate malicious device code attack patterns",
            "TARGET_USER": "Target user principal name for simulation",
            "DURATION": "Simulation duration in seconds (default: 300)",
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the device code flow simulation"""
        results = {
            "module": self.name,
            "status": "success",
            "simulation_type": "device_code_flow",
            "timeline": [],
            "detection_points": [],
            "recommendations": [],
            "summary": {}
        }
        
        tenant_id = self.get_option("TENANT_ID")
        client_id = self.get_option("CLIENT_ID")
        resource = self.get_option("RESOURCE")
        simulate_attack = self.get_option("SIMULATE_ATTACK").lower() == "true"
        target_user = self.get_option("TARGET_USER")
        duration = int(self.get_option("DURATION"))
        
        self.log(f"Starting Device Code Flow simulation for tenant: {tenant_id}")
        self.log(f"Simulation type: {'Attack' if simulate_attack else 'Legitimate'}")
        
        start_time = datetime.now()
        results["timeline"].append({
            "timestamp": start_time.isoformat(),
            "event": "Simulation started",
            "details": f"Client ID: {client_id}, Resource: {resource}"
        })
        
        # Step 1: Request device code
        self.log("Step 1: Requesting device code from authorization endpoint...")
        device_code_request = {
            "timestamp": datetime.now().isoformat(),
            "event": "Device Code Request",
            "endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode",
            "parameters": {
                "client_id": client_id,
                "resource": resource,
                "scope": "openid profile email"
            },
            "response_simulation": {
                "device_code": "SIMULATED_DEVICE_CODE_12345",
                "user_code": "ABCDEFGH",
                "verification_uri": "https://microsoft.com/devicelogin",
                "expires_in": 900,
                "interval": 5
            }
        }
        results["timeline"].append(device_code_request)
        
        # Step 2: Display user code (simulated)
        self.log(f"Step 2: Device code obtained. User code: ABCDEFGH")
        self.log(f"        Visit: https://microsoft.com/devicelogin")
        
        user_prompt_event = {
            "timestamp": datetime.now().isoformat(),
            "event": "User Prompt Displayed",
            "user_code": "ABCDEFGH",
            "verification_uri": "https://microsoft.com/devicelogin",
            "expires_in_seconds": 900
        }
        results["timeline"].append(user_prompt_event)
        
        # Step 3: Simulate polling for token
        self.log("Step 3: Polling for access token...")
        poll_attempts = 0
        max_polls = min(10, duration // 5)
        
        while poll_attempts < max_polls:
            poll_attempts += 1
            poll_event = {
                "timestamp": datetime.now().isoformat(),
                "event": "Token Poll Attempt",
                "attempt": poll_attempts,
                "endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "status": "pending" if poll_attempts < 3 else "success"
            }
            results["timeline"].append(poll_event)
            
            if poll_attempts >= 3:
                # Simulate successful authentication
                token_granted = {
                    "timestamp": datetime.now().isoformat(),
                    "event": "Access Token Granted",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "scope": "openid profile email User.Read",
                    "id_token": "SIMULATED_ID_TOKEN",
                    "access_token": "SIMULATED_ACCESS_TOKEN"
                }
                results["timeline"].append(token_granted)
                self.log("Step 4: Access token successfully obtained!")
                break
            
            time.sleep(0.1)  # Simulated delay
        
        # Detection analysis
        self.log("Analyzing detection points...")
        
        detection_points = [
            {
                "stage": "Initial Request",
                "detectable": True,
                "indicators": [
                    "Unusual application registration",
                    "High volume of device code requests",
                    "Unknown client application"
                ],
                "mitre_attack": "T1185 - Browser Session Hijacking"
            },
            {
                "stage": "User Authentication",
                "detectable": True,
                "indicators": [
                    "Sign-in from unfamiliar location",
                    "Device not compliant with policies",
                    "Anomalous sign-in properties"
                ],
                "mitre_attack": "T1078 - Valid Accounts"
            },
            {
                "stage": "Token Usage",
                "detectable": True,
                "indicators": [
                    "Token used from unexpected IP",
                    "Access to sensitive resources",
                    "Unusual API call patterns"
                ],
                "mitre_attack": "T1550.001 - Use Alternate Authentication Material"
            }
        ]
        
        if simulate_attack:
            self.log("Attack simulation mode enabled - adding attack indicators...")
            detection_points.append({
                "stage": "Attack Pattern",
                "detectable": True,
                "indicators": [
                    "Phishing campaign correlation",
                    "Multiple failed auth attempts before success",
                    "Geographic impossibility (impossible travel)",
                    "Token requested outside business hours"
                ],
                "severity": "High",
                "mitre_attack": "T1566 - Phishing"
            })
            results["attack_indicators"] = [
                "Simulated phishing email with device code link",
                "Social engineering attempt detected",
                "Credential harvesting pattern identified"
            ]
        
        results["detection_points"] = detection_points
        
        # Generate recommendations
        results["recommendations"] = [
            "Enable Conditional Access policies requiring MFA for all users",
            "Implement device compliance requirements",
            "Monitor Azure AD sign-in logs for anomalous device code flows",
            "Configure risk-based policies to detect suspicious authentication",
            "Use Microsoft Defender for Identity to detect token abuse",
            "Implement session timeout policies",
            "Educate users about device code phishing attacks",
            "Enable Security Defaults or implement Zero Trust architecture"
        ]
        
        if simulate_attack:
            results["recommendations"].extend([
                "Deploy anti-phishing solutions",
                "Implement email authentication (SPF, DKIM, DMARC)",
                "Configure alert rules for suspicious device code requests",
                "Conduct regular user awareness training on authentication attacks"
            ])
        
        # Summary
        end_time = datetime.now()
        results["summary"] = {
            "simulation_duration_seconds": (end_time - start_time).total_seconds(),
            "total_events": len(results["timeline"]),
            "detection_points_identified": len(detection_points),
            "attack_mode": simulate_attack,
            "target_user": target_user if target_user else "Not specified",
            "risk_assessment": "High" if simulate_attack else "Low"
        }
        
        self.log(f"Simulation complete. Total events: {len(results['timeline'])}")
        self.log(f"Detection points identified: {len(detection_points)}")
        
        return results


# Export the class
__all__ = ['EntraDeviceCodeFlow']
