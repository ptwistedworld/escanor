#!/usr/bin/env python3
"""
Port Scanner Module
Network reconnaissance - scans for open ports on target systems
"""

import socket
from typing import Dict, List, Any
from core.base_module import BaseModule


class PortScanner(BaseModule):
    """TCP/UDP port scanning module for network reconnaissance"""
    
    def __init__(self):
        super().__init__()
        self.name = "port_scan"
        self.category = "reconnaissance"
        self.description = "Scan target for open TCP/UDP ports"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        
        self.options = {
            'TARGET': '',
            'PORTS': '1-1000',
            'PROTOCOL': 'tcp',
            'TIMEOUT': '1'
        }
        
        self.required_options = ['TARGET']
        
        self.option_descriptions = {
            'TARGET': 'Target IP address or hostname',
            'PORTS': 'Port range (e.g., 1-1000, 80,443,8080)',
            'PROTOCOL': 'Protocol to scan: tcp or udp',
            'TIMEOUT': 'Connection timeout in seconds'
        }
    
    def _parse_ports(self, port_str: str) -> List[int]:
        """Parse port string into list of ports"""
        ports = []
        for part in port_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        return sorted(set(ports))
    
    def _scan_port(self, host: str, port: int, protocol: str, timeout: float) -> Dict[str, Any]:
        """Scan a single port"""
        result = {
            'port': port,
            'protocol': protocol,
            'state': 'closed',
            'service': 'unknown'
        }
        
        try:
            if protocol.lower() == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            sock.settimeout(timeout)
            connection_result = sock.connect_ex((host, port)) if protocol.lower() == 'tcp' else 0
            
            if connection_result == 0:
                result['state'] = 'open'
                # Try to identify service
                try:
                    service = socket.getservbyport(port, protocol.lower())
                    result['service'] = service
                except:
                    pass
            
            sock.close()
        except Exception as e:
            result['state'] = 'filtered'
            result['error'] = str(e)
        
        return result
    
    def run(self) -> Dict[str, Any]:
        """Execute the port scan"""
        if not self.validate_options():
            return {'success': False, 'error': 'Missing required options'}
        
        target = self.options['TARGET']
        ports = self._parse_ports(self.options.get('PORTS', '1-1000'))
        protocol = self.options.get('PROTOCOL', 'tcp')
        timeout = float(self.options.get('TIMEOUT', '1'))
        
        self.log(f"Starting {protocol.upper()} port scan on {target}")
        self.log(f"Scanning {len(ports)} ports")
        
        results = {
            'target': target,
            'protocol': protocol,
            'ports_scanned': len(ports),
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': []
        }
        
        for port in ports:
            scan_result = self._scan_port(target, port, protocol, timeout)
            
            if scan_result['state'] == 'open':
                results['open_ports'].append(scan_result)
                print(f"  [+] {port}/{protocol} - OPEN ({scan_result['service']})")
            elif scan_result['state'] == 'filtered':
                results['filtered_ports'].append(scan_result)
            else:
                results['closed_ports'].append(port)
        
        # Summary
        print(f"\n[+] Scan complete:")
        print(f"    Open: {len(results['open_ports'])}")
        print(f"    Filtered: {len(results['filtered_ports'])}")
        print(f"    Closed: {len(results['closed_ports'])}")
        
        results['success'] = True
        self.results = results
        return results
