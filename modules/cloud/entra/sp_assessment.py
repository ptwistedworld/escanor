#!/usr/bin/env python3
"""
Entra ID Service Principal Assessment Module
Assesses service principals and managed identities for security misconfigurations
"""

from core.base_module import BaseModule, action
from typing import Dict, Any, List
from datetime import datetime


class EntraSPAssessment(BaseModule):
    """Assess Service Principals and Managed Identities in Entra ID"""
    
    def __init__(self):
        super().__init__()
        self.name = "sp_assessment"
        self.display_name = "Service Principal Assessor"
        self.category = "cloud/entra"
        self.description = "Assess service principals and managed identities for security risks"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        self.options = {
            "TENANT_ID": "",
            "CLIENT_ID": "",
            "CLIENT_SECRET": "",
            "ASSESSMENT_TYPE": "all",
            "INCLUDE_MANAGED_IDENTITIES": "True",
            "CREDENTIAL_AGE_THRESHOLD": "90",
        }
        self.required_options = ["TENANT_ID", "CLIENT_ID"]
        self.option_descriptions = {
            "TENANT_ID": "Azure Entra ID Tenant ID",
            "CLIENT_ID": "Service Principal Client ID for authentication",
            "CLIENT_SECRET": "Service Principal Client Secret (optional if using managed identity)",
            "ASSESSMENT_TYPE": "Type of assessment: all, credentials, permissions, or configuration",
            "INCLUDE_MANAGED_IDENTITIES": "Include managed identities in assessment (True/False)",
            "CREDENTIAL_AGE_THRESHOLD": "Alert threshold for credential age in days (default: 90)",
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the service principal assessment"""
        results = {
            "module": self.name,
            "status": "success",
            "assessment_type": self.get_option("ASSESSMENT_TYPE"),
            "findings": [],
            "service_principals_assessed": [],
            "managed_identities_assessed": [],
            "recommendations": [],
            "summary": {}
        }
        
        tenant_id = self.get_option("TENANT_ID")
        client_id = self.get_option("CLIENT_ID")
        assessment_type = self.get_option("ASSESSMENT_TYPE") or "all"
        include_mi = (self.get_option("INCLUDE_MANAGED_IDENTITIES") or "True").lower() == "true"
        cred_threshold = int(self.get_option("CREDENTIAL_AGE_THRESHOLD") or "90")
        
        self.log(f"Starting Service Principal assessment for tenant: {tenant_id}")
        self.log(f"Assessment type: {assessment_type}")
        self.log(f"Include Managed Identities: {include_mi}")
        
        # Mock data for demonstration
        mock_service_principals = [
            {
                "id": "sp-001",
                "displayName": "Legacy Application SP",
                "appId": "app-legacy-001",
                "accountEnabled": True,
                "createdDateTime": "2020-01-15T00:00:00Z",
                "passwordCredentials": [
                    {
                        "keyId": "cred-001",
                        "displayName": "Primary Secret",
                        "startDateTime": "2023-01-01T00:00:00Z",
                        "endDateTime": "2024-01-01T00:00:00Z"
                    }
                ],
                "appRoles": [
                    {"id": "role-001", "value": "Directory.ReadWrite.All", "isEnabled": True}
                ],
                "oauth2PermissionScopes": []
            },
            {
                "id": "sp-002",
                "displayName": "Modern App Registration",
                "appId": "app-modern-002",
                "accountEnabled": True,
                "createdDateTime": "2024-01-10T00:00:00Z",
                "passwordCredentials": [],
                "appRoles": [
                    {"id": "role-002", "value": "User.Read", "isEnabled": True}
                ],
                "oauth2PermissionScopes": [
                    {"id": "scope-001", "value": "access_as_user", "isEnabled": True}
                ]
            },
            {
                "id": "sp-003",
                "displayName": "Overprivileged Service Account",
                "appId": "app-overpriv-003",
                "accountEnabled": True,
                "createdDateTime": "2021-06-01T00:00:00Z",
                "passwordCredentials": [
                    {
                        "keyId": "cred-003a",
                        "displayName": "Old Secret",
                        "startDateTime": "2022-01-01T00:00:00Z",
                        "endDateTime": "2023-01-01T00:00:00Z"
                    },
                    {
                        "keyId": "cred-003b",
                        "displayName": "Current Secret",
                        "startDateTime": "2024-01-01T00:00:00Z",
                        "endDateTime": "2025-01-01T00:00:00Z"
                    }
                ],
                "appRoles": [
                    {"id": "role-003", "value": "Directory.ReadWrite.All", "isEnabled": True},
                    {"id": "role-004", "value": "Application.ReadWrite.All", "isEnabled": True},
                    {"id": "role-005", "value": "RoleManagement.ReadWrite.Directory", "isEnabled": True}
                ],
                "oauth2PermissionScopes": []
            }
        ]
        
        mock_managed_identities = [
            {
                "id": "mi-001",
                "displayName": "VM-Production-MI",
                "type": "SystemAssigned",
                "accountEnabled": True,
                "resourceId": "/subscriptions/xxx/resourceGroups/prod/providers/Microsoft.Compute/virtualMachines/prod-vm-001",
                "roles": [
                    {"role": "Contributor", "scope": "/subscriptions/xxx/resourceGroups/prod"}
                ]
            },
            {
                "id": "mi-002",
                "displayName": "FunctionApp-MI",
                "type": "SystemAssigned",
                "accountEnabled": True,
                "resourceId": "/subscriptions/xxx/resourceGroups/dev/providers/Microsoft.Web/sites/dev-func-001",
                "roles": [
                    {"role": "Storage Blob Data Reader", "scope": "/subscriptions/xxx/resourceGroups/dev"}
                ]
            }
        ]
        
        findings = []
        sp_count = 0
        mi_count = 0
        
        # Assess Service Principals
        self.log(f"Assessing {len(mock_service_principals)} service principals...")
        
        for sp in mock_service_principals:
            sp_findings = {
                "object_id": sp["id"],
                "display_name": sp["displayName"],
                "type": "ServicePrincipal",
                "issues": [],
                "risk_level": "Low"
            }
            
            # Check for expired credentials
            for cred in sp.get("passwordCredentials", []):
                end_date = datetime.fromisoformat(cred["endDateTime"].replace("Z", "+00:00"))
                start_date = datetime.fromisoformat(cred["startDateTime"].replace("Z", "+00:00"))
                now = datetime.now(end_date.tzinfo)
                
                if end_date < now:
                    sp_findings["issues"].append({
                        "severity": "High",
                        "category": "Credential Management",
                        "issue": f"Expired credential found: {cred['displayName']}",
                        "details": f"Credential expired on {cred['endDateTime']}",
                        "recommendation": "Remove expired credentials immediately"
                    })
                    sp_findings["risk_level"] = "High"
                else:
                    # Check credential age
                    age_days = (now - start_date).days
                    if age_days > cred_threshold:
                        sp_findings["issues"].append({
                            "severity": "Medium",
                            "category": "Credential Management",
                            "issue": f"Old credential detected: {cred['displayName']}",
                            "details": f"Credential is {age_days} days old (threshold: {cred_threshold})",
                            "recommendation": "Rotate credentials regularly"
                        })
                        if sp_findings["risk_level"] == "Low":
                            sp_findings["risk_level"] = "Medium"
            
            # Check for high-privilege roles
            high_priv_roles = [
                "Directory.ReadWrite.All",
                "Application.ReadWrite.All",
                "RoleManagement.ReadWrite.Directory",
                "PrivilegedEligibilitySchedule.ReadWrite.AzureADGroup"
            ]
            
            privileged_roles = [r for r in sp.get("appRoles", []) if r["value"] in high_priv_roles]
            if len(privileged_roles) >= 2:
                sp_findings["issues"].append({
                    "severity": "High",
                    "category": "Privilege Escalation",
                    "issue": "Service principal has multiple high-privilege roles",
                    "details": f"Roles: {[r['value'] for r in privileged_roles]}",
                    "recommendation": "Apply principle of least privilege, reduce role assignments"
                })
                sp_findings["risk_level"] = "High"
            
            # Check if disabled but has credentials
            if not sp.get("accountEnabled", True) and sp.get("passwordCredentials", []):
                sp_findings["issues"].append({
                    "severity": "Medium",
                    "category": "Configuration",
                    "issue": "Disabled service principal with active credentials",
                    "details": "Consider removing credentials from disabled accounts",
                    "recommendation": "Clean up credentials from disabled service principals"
                })
            
            findings.append(sp_findings)
            results["service_principals_assessed"].append(sp["id"])
            sp_count += 1
        
        # Assess Managed Identities if enabled
        if include_mi:
            self.log(f"Assessing {len(mock_managed_identities)} managed identities...")
            
            for mi in mock_managed_identities:
                mi_findings = {
                    "object_id": mi["id"],
                    "display_name": mi["displayName"],
                    "type": "ManagedIdentity",
                    "identity_type": mi["type"],
                    "issues": [],
                    "risk_level": "Low"
                }
                
                # Check for overly broad permissions
                broad_scopes = ["/subscriptions/", "/"]
                for role_assignment in mi.get("roles", []):
                    scope = role_assignment.get("scope", "")
                    role = role_assignment.get("role", "")
                    
                    if any(scope.startswith(broad) for broad in broad_scopes):
                        if role in ["Contributor", "Owner"]:
                            mi_findings["issues"].append({
                                "severity": "High",
                                "category": "Permissions",
                                "issue": f"Managed identity has broad '{role}' permissions",
                                "details": f"Scope: {scope}",
                                "recommendation": "Restrict permissions to specific resources"
                            })
                            mi_findings["risk_level"] = "High"
                
                findings.append(mi_findings)
                results["managed_identities_assessed"].append(mi["id"])
                mi_count += 1
        
        # Generate summary
        total_issues = sum(len(f["issues"]) for f in findings)
        high_risk = sum(1 for f in findings if f["risk_level"] == "High")
        medium_risk = sum(1 for f in findings if f["risk_level"] == "Medium")
        
        results["findings"] = findings
        results["summary"] = {
            "total_objects_assessed": sp_count + mi_count,
            "service_principals_count": sp_count,
            "managed_identities_count": mi_count,
            "total_issues_found": total_issues,
            "high_risk_objects": high_risk,
            "medium_risk_objects": medium_risk,
            "overall_risk_level": "High" if high_risk > 0 else "Medium" if medium_risk > 0 else "Low"
        }
        
        # Generate recommendations
        results["recommendations"] = [
            "Implement regular credential rotation policies",
            "Use managed identities instead of service principal secrets where possible",
            "Apply principle of least privilege for all role assignments",
            "Monitor service principal sign-ins and API usage",
            "Set up alerts for privileged service principal activities",
            "Conduct quarterly access reviews for service principals",
            "Use certificate-based authentication instead of secrets",
            "Implement just-in-time access for privileged operations"
        ]
        
        self.log(f"Assessment complete. Assessed {sp_count} SPs and {mi_count} MIs")
        self.log(f"Found {total_issues} issues ({high_risk} high risk)")
        
        return results


# Export the class
__all__ = ['EntraSPAssessment']
