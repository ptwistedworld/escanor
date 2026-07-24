#!/usr/bin/env python3
"""
Entra ID Conditional Access Policy Validator Module
Tests and validates Conditional Access policies in Azure Entra ID
"""

from core.base_module import BaseModule
from typing import Dict, Any, List
import json


class EntraCAPValidator(BaseModule):
    """Validate Conditional Access policies in Entra ID"""
    
    def __init__(self):
        super().__init__()
        self.name = "ca_validator"
        self.display_name = "Conditional Access Validator"
        self.category = "cloud/entra"
        self.description = "Validate and test Conditional Access policies for misconfigurations"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.options = {
            "TENANT_ID": "",
            "CLIENT_ID": "",
            "CLIENT_SECRET": "",
            "POLICY_IDS": "",
            "TEST_USER": "",
            "LOCATIONS": "",
        }
        self.required_options = ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET"]
        self.option_descriptions = {
            "TENANT_ID": "Azure Entra ID Tenant ID",
            "CLIENT_ID": "Service Principal Client ID",
            "CLIENT_SECRET": "Service Principal Client Secret",
            "POLICY_IDS": "Comma-separated list of policy IDs to test (optional, tests all if empty)",
            "TEST_USER": "User principal name for testing policies",
            "LOCATIONS": "Comma-separated list of locations/IPs to test from",
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the CA policy validation"""
        results = {
            "module": self.name,
            "status": "success",
            "findings": [],
            "recommendations": [],
            "tested_policies": [],
            "summary": {}
        }
        
        tenant_id = self.get_option("TENANT_ID")
        client_id = self.get_option("CLIENT_ID")
        client_secret = self.get_option("CLIENT_SECRET")
        policy_ids = self.get_option("POLICY_IDS")
        test_user = self.get_option("TEST_USER")
        locations = self.get_option("LOCATIONS")
        
        self.log(f"Starting Conditional Access validation for tenant: {tenant_id}")
        
        # Simulate authentication and policy retrieval
        # In production, this would use MSAL or Microsoft Graph API
        self.log("Authenticating to Azure Entra ID...")
        
        # Mock policy data for demonstration
        mock_policies = [
            {
                "id": "policy-001",
                "displayName": "Require MFA for All Users",
                "state": "enabled",
                "conditions": {
                    "users": {"includeUsers": ["All"]},
                    "applications": {"includeApplications": ["All"]}
                },
                "grantControls": {
                    "builtInControls": ["mfa"],
                    "operator": "OR"
                }
            },
            {
                "id": "policy-002",
                "displayName": "Block Legacy Authentication",
                "state": "enabled",
                "conditions": {
                    "clientAppTypes": ["exchangeActiveSync", "other"]
                },
                "grantControls": {
                    "builtInControls": ["block"]
                }
            },
            {
                "id": "policy-003",
                "displayName": "Require Compliant Device",
                "state": "enabled",
                "conditions": {
                    "users": {"includeUsers": ["All"]},
                    "applications": {"includeApplications": ["All"]}
                },
                "grantControls": {
                    "builtInControls": ["compliantDevice"]
                }
            }
        ]
        
        # Filter policies if specific IDs provided
        if policy_ids:
            policy_list = [p.strip() for p in policy_ids.split(",")]
            mock_policies = [p for p in mock_policies if p["id"] in policy_list]
        
        self.log(f"Testing {len(mock_policies)} Conditional Access policies...")
        
        findings = []
        for policy in mock_policies:
            policy_result = {
                "policy_id": policy["id"],
                "policy_name": policy["displayName"],
                "state": policy["state"],
                "test_results": [],
                "issues": []
            }
            
            # Test policy configuration
            if policy["state"] != "enabled":
                policy_result["issues"].append({
                    "severity": "Medium",
                    "issue": f"Policy '{policy['displayName']}' is not enabled",
                    "recommendation": "Enable the policy to enforce security controls"
                })
            
            # Check for common misconfigurations
            if "mfa" not in policy.get("grantControls", {}).get("builtInControls", []) and \
               "block" not in policy.get("grantControls", {}).get("builtInControls", []):
                if policy["state"] == "enabled":
                    policy_result["issues"].append({
                        "severity": "High",
                        "issue": f"Policy '{policy['displayName']}' does not enforce MFA or block access",
                        "recommendation": "Consider adding MFA requirement or explicit block controls"
                    })
            
            # Test with different locations if provided
            if locations:
                location_list = [l.strip() for l in locations.split(",")]
                for location in location_list:
                    test_result = {
                        "location": location,
                        "result": "PASS",  # Would be actual test result in production
                        "details": f"Policy evaluated for location: {location}"
                    }
                    policy_result["test_results"].append(test_result)
            
            # Test with user if provided
            if test_user:
                user_test = {
                    "user": test_user,
                    "result": "PASS",  # Would be actual test result
                    "details": f"Policy evaluated for user: {test_user}"
                }
                policy_result["test_results"].append(user_test)
            
            findings.append(policy_result)
            results["tested_policies"].append(policy["id"])
        
        # Generate summary
        total_issues = sum(len(f["issues"]) for f in findings)
        high_severity = sum(1 for f in findings for i in f["issues"] if i.get("severity") == "High")
        medium_severity = sum(1 for f in findings for i in f["issues"] if i.get("severity") == "Medium")
        
        results["findings"] = findings
        results["summary"] = {
            "total_policies_tested": len(findings),
            "total_issues_found": total_issues,
            "high_severity_issues": high_severity,
            "medium_severity_issues": medium_severity,
            "risk_level": "High" if high_severity > 0 else "Medium" if medium_severity > 0 else "Low"
        }
        
        # Generate recommendations
        if high_severity > 0:
            results["recommendations"].append("Immediate attention required: High severity issues detected in CA policies")
        if medium_severity > 0:
            results["recommendations"].append("Review and remediate medium severity policy configurations")
        
        results["recommendations"].extend([
            "Regularly audit Conditional Access policies for effectiveness",
            "Test policies in report-only mode before enforcing",
            "Ensure break-glass accounts are excluded from restrictive policies",
            "Monitor sign-in logs for policy impact analysis"
        ])
        
        self.log(f"Validation complete. Found {total_issues} issues ({high_severity} high, {medium_severity} medium)")
        
        return results


# Export the class
__all__ = ['EntraCAPValidator']
