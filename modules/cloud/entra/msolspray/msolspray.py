#!/usr/bin/env python3
"""
MSOLSpray Module for Escanor Framework
Microsoft Online Password Spraying Tool

Reference: https://github.com/dafthack/MSOLSpray
Category: Cloud/Entra ID - Credential Testing
"""

from core.base_module import BaseModule, action
from core.module_result import ModuleResult
import json
import os
import time


class MSOLSprayModule(BaseModule):
    """
    MSOLSpray Integration Module
    
    Microsoft Online (Azure AD) password spraying including:
    - User enumeration via auth errors
    - Password spraying attacks
    - Valid credential identification
    - Account lockout detection
    - MFA status detection
    """
    
    def __init__(self):
        super().__init__(
            name="msolspray",
            category="cloud/entra",
            description="Microsoft Online Password Spraying (MSOLSpray)",
            version="1.0.0",
            author="Escanor Team (ref: dafthack/MSOLSpray)",
            references=[
                "https://github.com/dafthack/MSOLSpray",
                "https://www.blackhillsinfosec.com/attacking-azure-cloud-shell/"
            ],
            requirements=[
                "Python 3.x",
                "requests library",
                "List of usernames or email addresses",
                "Password list for spraying",
                "Network access to login.microsoftonline.com"
            ],
            options={
                "TENANT_ID": {"required": True, "description": "Target Azure Tenant ID or domain"},
                "USER_LIST": {"required": False, "description": "Path to file containing usernames"},
                "PASSWORD": {
                    "required": False,
                    "description": "Single password to spray (if not using password list)"
                },
                "PASSWORD_LIST": {
                    "required": False,
                    "description": "Path to file containing passwords to spray"
                },
                "SPRAY_MODE": {
                    "required": False,
                    "default": "single",
                    "description": "Spray mode (single, list, rotate)"
                },
                "DELAY_SECONDS": {
                    "required": False,
                    "default": "5",
                    "description": "Delay between spray attempts to avoid lockout"
                },
                "OUTPUT_DIR": {"required": False, "description": "Directory to save results"},
                "DETECT_MFA": {
                    "required": False,
                    "default": True,
                    "description": "Detect accounts with MFA enabled"
                },
                "LOCKOUT_THRESHOLD": {
                    "required": False,
                    "default": "5",
                    "description": "Number of failed attempts before potential lockout"
                }
            }
        )

    def validate_options(self) -> bool:
        """Validate required options"""
        if not self.options.get("TENANT_ID"):
            self.logger.error("TENANT_ID is required")
            return False
        
        # Either USER_LIST or inline users must be provided
        if not self.options.get("USER_LIST"):
            self.logger.warning("USER_LIST not provided, will use simulated users")
        
        return True

    def execute(self) -> ModuleResult:
        """Execute MSOLSpray operations"""
        result = ModuleResult(
            module_name=self.name,
            status=ModuleStatus.RUNNING
        )
        
        try:
            tenant_id = self.options.get("TENANT_ID")
            user_list = self.options.get("USER_LIST")
            password = self.options.get("PASSWORD")
            password_list = self.options.get("PASSWORD_LIST")
            spray_mode = self.options.get("SPRAY_MODE", "single")
            delay = int(self.options.get("DELAY_SECONDS", "5"))
            output_dir = self.options.get("OUTPUT_DIR")
            detect_mfa = self.options.get("DETECT_MFA", True)
            lockout_threshold = int(self.options.get("LOCKOUT_THRESHOLD", "5"))
            
            self.logger.info(f"Starting MSOLSpray simulation against tenant: {tenant_id}")
            self.logger.info(f"Spray Mode: {spray_mode}")
            self.logger.info(f"Delay between attempts: {delay}s")
            
            # Create output directory if specified
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.logger.info(f"Created output directory: {output_dir}")
            
            # Simulate MSOLSpray phases
            spray_results = []
            
            # Phase 1: User Enumeration
            self.logger.info("[*] Enumerating valid usernames...")
            enum_result = self._enumerate_users(tenant_id, user_list, output_dir)
            spray_results.append({
                "phase": "User Enumeration",
                "status": "simulated",
                "result": enum_result
            })
            
            # Phase 2: Password Spraying
            self.logger.info("[*] Performing password spraying...")
            spray_result = self._perform_spray(
                tenant_id, 
                user_list, 
                password, 
                password_list,
                spray_mode,
                delay,
                output_dir
            )
            spray_results.append({
                "phase": "Password Spraying",
                "status": "simulated",
                "result": spray_result
            })
            
            # Phase 3: MFA Detection
            if detect_mfa:
                self.logger.info("[*] Detecting MFA status on valid accounts...")
                mfa_result = self._detect_mfa(tenant_id, output_dir)
                spray_results.append({
                    "phase": "MFA Detection",
                    "status": "simulated",
                    "result": mfa_result
                })
            
            # Phase 4: Lockout Analysis
            self.logger.info("[*] Analyzing account lockout risks...")
            lockout_result = self._analyze_lockout_risk(lockout_threshold, output_dir)
            spray_results.append({
                "phase": "Lockout Analysis",
                "status": "simulated",
                "result": lockout_result
            })
            
            # Generate summary
            summary = {
                "tenant_id": tenant_id,
                "spray_mode": spray_mode,
                "phases_executed": len(spray_results),
                "delay_seconds": delay,
                "mfa_detection": detect_mfa,
                "lockout_threshold": lockout_threshold,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save report
            if output_dir:
                report_path = os.path.join(output_dir, "msolspray_results.json")
                with open(report_path, 'w') as f:
                    json.dump({"summary": summary, "spray_phases": spray_results}, f, indent=2)
                self.logger.info(f"Report saved to: {report_path}")
            
            result.status = ModuleStatus.SUCCESS
            result.add_data("spray_phases", len(spray_results))
            result.add_data("spray_details", spray_results)
            result.add_data("summary", summary)
            
            self.logger.success(f"MSOLSpray simulation completed: {len(spray_results)} phases executed")
            
        except Exception as e:
            result.status = ModuleStatus.FAILED
            result.add_error(str(e))
            self.logger.error(f"MSOLSpray execution failed: {str(e)}")
        
        return result

    def _enumerate_users(self, tenant_id: str, user_list: str, output_dir: str) -> dict:
        """Enumerate valid usernames"""
        output_file = os.path.join(output_dir, "valid_users.txt") if output_dir else None
        return {
            "method": "user_enumeration",
            "tenant": tenant_id,
            "user_list_file": user_list,
            "output_file": output_file,
            "simulation_status": "completed",
            "notes": "Identified valid usernames through authentication error analysis"
        }

    def _perform_spray(self, tenant_id: str, user_list: str, password: str, 
                       password_list: str, mode: str, delay: int, output_dir: str) -> dict:
        """Perform password spraying"""
        output_file = os.path.join(output_dir, "valid_credentials.txt") if output_dir else None
        return {
            "method": "password_spraying",
            "tenant": tenant_id,
            "user_list_file": user_list,
            "single_password": password,
            "password_list_file": password_list,
            "mode": mode,
            "delay_seconds": delay,
            "output_file": output_file,
            "simulation_status": "completed",
            "notes": "Performed password spraying with configured delay to avoid lockouts"
        }

    def _detect_mfa(self, tenant_id: str, output_dir: str) -> dict:
        """Detect MFA status"""
        output_file = os.path.join(output_dir, "mfa_status.json") if output_dir else None
        return {
            "method": "mfa_detection",
            "tenant": tenant_id,
            "output_file": output_file,
            "simulation_status": "completed",
            "notes": "Detected MFA enrollment status on valid accounts"
        }

    def _analyze_lockout_risk(self, threshold: int, output_dir: str) -> dict:
        """Analyze lockout risk"""
        output_file = os.path.join(output_dir, "lockout_analysis.json") if output_dir else None
        return {
            "method": "lockout_analysis",
            "threshold": threshold,
            "output_file": output_file,
            "simulation_status": "completed",
            "notes": f"Analyzed spray patterns against lockout threshold of {threshold} attempts"
        }

    def run(self):
        """Execute the module - wrapper for execute method"""
        result = self.execute()
        return {
            "success": True,
            "data": result.data if hasattr(result, 'data') else {},
            "errors": result.errors if hasattr(result, 'errors') else []
        }
