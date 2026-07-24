#!/usr/bin/env python3
"""
Result Reporter Module
Writes detailed, standardized reports of module execution results to text files
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ResultReporter:
    """Handles writing standardized result reports to files"""
    
    def __init__(self, output_dir: str = "./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_format = "text"  # Can be extended to support json, markdown, html
    
    def generate_report_id(self) -> str:
        """Generate a unique report ID based on timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def write_result(self, 
                     module_name: str, 
                     results: Dict[str, Any], 
                     options_used: Optional[Dict] = None,
                     execution_time: Optional[float] = None,
                     operator: str = "unknown",
                     notes: str = "") -> str:
        """
        Write a detailed result report to a text file
        
        Returns the path to the generated report
        """
        report_id = self.generate_report_id()
        filename = f"{module_name}_{report_id}.txt"
        filepath = self.output_dir / filename
        
        report_content = self._format_report(
            module_name=module_name,
            results=results,
            options_used=options_used or {},
            execution_time=execution_time,
            operator=operator,
            notes=notes,
            report_id=report_id
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Also save JSON version for programmatic access
        json_filepath = self.output_dir / f"{module_name}_{report_id}.json"
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "report_id": report_id,
                "module_name": module_name,
                "timestamp": datetime.now().isoformat(),
                "options_used": options_used or {},
                "execution_time_seconds": execution_time,
                "operator": operator,
                "notes": notes,
                "results": results
            }, f, indent=2, default=str)
        
        return str(filepath)
    
    def _format_report(self, 
                       module_name: str,
                       results: Dict[str, Any],
                       options_used: Dict,
                       execution_time: Optional[float],
                       operator: str,
                       notes: str,
                       report_id: str) -> str:
        """Format the report content as standardized text"""
        
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("ESCANOR FRAMEWORK - MODULE EXECUTION REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Report Metadata
        lines.append("REPORT METADATA")
        lines.append("-" * 40)
        lines.append(f"Report ID:        {report_id}")
        lines.append(f"Module Name:      {module_name}")
        lines.append(f"Timestamp:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Operator:         {operator}")
        if execution_time is not None:
            lines.append(f"Execution Time:   {execution_time:.2f} seconds")
        lines.append("")
        
        # Options Used
        lines.append("OPTIONS USED")
        lines.append("-" * 40)
        if options_used:
            for key, value in options_used.items():
                # Mask sensitive values
                display_value = "***REDACTED***" if any(s in key.lower() for s in ['secret', 'password', 'key', 'token']) else value
                lines.append(f"{key:<20}: {display_value}")
        else:
            lines.append("No options specified")
        lines.append("")
        
        # Execution Status
        lines.append("EXECUTION STATUS")
        lines.append("-" * 40)
        status = results.get("status", "unknown")
        status_symbol = "✓ SUCCESS" if status == "success" else "✗ FAILED"
        lines.append(f"Status: {status_symbol}")
        lines.append("")
        
        # Results Summary
        lines.append("RESULTS SUMMARY")
        lines.append("-" * 40)
        
        # Handle different result structures
        if "summary" in results:
            summary = results["summary"]
            for key, value in summary.items():
                formatted_key = key.replace("_", " ").title()
                lines.append(f"{formatted_key:<25}: {value}")
        elif "findings" in results:
            findings = results.get("findings", [])
            lines.append(f"Total Findings: {len(findings)}")
            
            # Count by severity if available
            severity_counts = {}
            for finding in findings:
                if isinstance(finding, dict):
                    for issue in finding.get("issues", []):
                        severity = issue.get("severity", "Unknown")
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            if severity_counts:
                lines.append("")
                lines.append("Findings by Severity:")
                for severity, count in sorted(severity_counts.items()):
                    lines.append(f"  {severity}: {count}")
        
        lines.append("")
        
        # Detailed Findings
        if "findings" in results and results["findings"]:
            lines.append("DETAILED FINDINGS")
            lines.append("-" * 40)
            
            for idx, finding in enumerate(results["findings"], 1):
                if isinstance(finding, dict):
                    lines.append(f"\n[Finding #{idx}]")
                    
                    # Display name or ID
                    if "display_name" in finding:
                        lines.append(f"Name: {finding['display_name']}")
                    elif "object_id" in finding:
                        lines.append(f"Object ID: {finding['object_id']}")
                    elif "policy_name" in finding:
                        lines.append(f"Policy: {finding['policy_name']}")
                    
                    # Risk level
                    if "risk_level" in finding:
                        lines.append(f"Risk Level: {finding['risk_level']}")
                    
                    # Issues
                    issues = finding.get("issues", [])
                    if issues:
                        lines.append("\nIssues:")
                        for issue_idx, issue in enumerate(issues, 1):
                            if isinstance(issue, dict):
                                severity = issue.get("severity", "Unknown")
                                category = issue.get("category", "General")
                                description = issue.get("issue", "No description")
                                
                                lines.append(f"  [{issue_idx}] Severity: {severity}")
                                lines.append(f"      Category: {category}")
                                lines.append(f"      Issue: {description}")
                                
                                if "details" in issue:
                                    lines.append(f"      Details: {issue['details']}")
                                if "recommendation" in issue:
                                    lines.append(f"      Recommendation: {issue['recommendation']}")
                                lines.append("")
                    
                    # Test results
                    test_results = finding.get("test_results", [])
                    if test_results:
                        lines.append("Test Results:")
                        for tr in test_results:
                            if isinstance(tr, dict):
                                result_status = tr.get("result", "Unknown")
                                details = tr.get("details", "")
                                lines.append(f"  - Result: {result_status} | {details}")
                        lines.append("")
        
        # Recommendations
        if "recommendations" in results and results["recommendations"]:
            lines.append("\nRECOMMENDATIONS")
            lines.append("-" * 40)
            for idx, rec in enumerate(results["recommendations"], 1):
                lines.append(f"{idx}. {rec}")
            lines.append("")
        
        # Additional Data Sections
        for key, value in results.items():
            if key not in ["status", "module", "summary", "findings", "recommendations"]:
                lines.append(f"\n{key.upper().replace('_', ' ')}")
                lines.append("-" * 40)
                
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(json.dumps(item, indent=2, default=str))
                        else:
                            lines.append(f"  - {item}")
                elif isinstance(value, dict):
                    lines.append(json.dumps(value, indent=2, default=str))
                else:
                    lines.append(str(value))
                lines.append("")
        
        # Notes
        if notes:
            lines.append("\nOPERATOR NOTES")
            lines.append("-" * 40)
            lines.append(notes)
            lines.append("")
        
        # Footer
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Generated by Escanor Framework - https://github.com/escanor-framework")
        lines.append("This report is confidential and intended for authorized personnel only.")
        
        return "\n".join(lines)
    
    def consolidate_reports(self, report_paths: list, output_filename: str = "consolidated_report.txt") -> str:
        """Consolidate multiple reports into a single document"""
        output_path = self.output_dir / output_filename
        
        lines = []
        lines.append("=" * 80)
        lines.append("ESCANOR FRAMEWORK - CONSOLIDATED ASSESSMENT REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Number of Reports: {len(report_paths)}")
        lines.append("")
        
        for idx, report_path in enumerate(report_paths, 1):
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines.append(f"\n{'='*80}")
                    lines.append(f"REPORT #{idx}: {os.path.basename(report_path)}")
                    lines.append(f"{'='*80}\n")
                    lines.append(content)
            except Exception as e:
                lines.append(f"\n[!] Error reading report {report_path}: {e}\n")
        
        lines.append("\n" + "=" * 80)
        lines.append("END OF CONSOLIDATED REPORT")
        lines.append("=" * 80)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        return str(output_path)
    
    def list_reports(self) -> list:
        """List all available reports in the output directory"""
        reports = []
        for f in self.output_dir.glob("*.txt"):
            reports.append({
                "filename": f.name,
                "path": str(f),
                "created": datetime.fromtimestamp(f.stat().st_ctime).isoformat(),
                "size": f.stat().st_size
            })
        return sorted(reports, key=lambda x: x["created"], reverse=True)


# Singleton instance for easy access
_reporter_instance = None

def get_reporter(output_dir: str = "./results") -> ResultReporter:
    """Get or create the singleton reporter instance"""
    global _reporter_instance
    if _reporter_instance is None:
        _reporter_instance = ResultReporter(output_dir)
    return _reporter_instance
