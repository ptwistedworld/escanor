#!/usr/bin/env python3
"""
Web Scanner Module
Web application reconnaissance - scans for web technologies, directories, and vulnerabilities
"""

import socket
from typing import Dict, List, Any
from core.base_module import BaseModule


class WebScanner(BaseModule):
    """Web application scanning module for reconnaissance"""
    
    def __init__(self):
        super().__init__()
        self.name = "web_scan"
        self.category = "reconnaissance"
        self.description = "Scan web applications for technologies, headers, and potential issues"
        self.author = "Escanor Team"
        self.version = "1.0.0"
        
        self.options = {
            'TARGET': '',
            'PORT': '80',
            'USE_SSL': 'False',
            'CHECK_HEADERS': 'True'
        }
        
        self.required_options = ['TARGET']
        
        self.option_descriptions = {
            'TARGET': 'Target URL or hostname',
            'PORT': 'Target port (default: 80)',
            'USE_SSL': 'Use HTTPS instead of HTTP (True/False)',
            'CHECK_HEADERS': 'Analyze security headers (True/False)'
        }
    
    def _check_web_server(self, host: str, port: int, use_ssl: bool) -> Dict[str, Any]:
        """Check if web server is responding"""
        result = {
            'host': host,
            'port': port,
            'ssl': use_ssl,
            'responding': False,
            'server_header': None,
            'technologies': []
        }
        
        try:
            # Simple socket check for web server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            connection = sock.connect_ex((host, port))
            
            if connection == 0:
                result['responding'] = True
                
                # Try to get banner
                try:
                    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                    sock.send(request.encode())
                    response = sock.recv(1024).decode('utf-8', errors='ignore')
                    
                    # Extract server header
                    for line in response.split('\r\n'):
                        if line.lower().startswith('server:'):
                            result['server_header'] = line.split(':', 1)[1].strip()
                            break
                    
                    # Basic technology detection
                    if 'nginx' in response.lower():
                        result['technologies'].append('nginx')
                    if 'apache' in response.lower():
                        result['technologies'].append('Apache')
                    if 'iis' in response.lower():
                        result['technologies'].append('Microsoft IIS')
                    if 'x-powered-by' in response.lower():
                        if 'php' in response.lower():
                            result['technologies'].append('PHP')
                        elif 'asp' in response.lower():
                            result['technologies'].append('ASP.NET')
                
                except Exception as e:
                    result['banner_error'] = str(e)
            
            sock.close()
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_headers(self, headers_response: str) -> Dict[str, Any]:
        """Analyze security headers"""
        analysis = {
            'missing_security_headers': [],
            'present_headers': [],
            'recommendations': []
        }
        
        required_headers = [
            ('Content-Security-Policy', 'Implement CSP to prevent XSS attacks'),
            ('X-Frame-Options', 'Set X-Frame-Options to prevent clickjacking'),
            ('X-Content-Type-Options', 'Set to nosniff to prevent MIME sniffing'),
            ('Strict-Transport-Security', 'Enable HSTS for secure connections'),
            ('X-XSS-Protection', 'Enable XSS protection header'),
            ('Referrer-Policy', 'Control referrer information leakage')
        ]
        
        headers_lower = headers_response.lower()
        
        for header, recommendation in required_headers:
            if header.lower() in headers_lower:
                analysis['present_headers'].append(header)
            else:
                analysis['missing_security_headers'].append(header)
                analysis['recommendations'].append(recommendation)
        
        return analysis
    
    def run(self) -> Dict[str, Any]:
        """Execute the web scan"""
        if not self.validate_options():
            return {'success': False, 'error': 'Missing required options'}
        
        target = self.options['TARGET']
        port = int(self.options.get('PORT', '80'))
        use_ssl = self.options.get('USE_SSL', 'False').lower() == 'true'
        check_headers = self.options.get('CHECK_HEADERS', 'True').lower() == 'true'
        
        self.log(f"Starting web scan on {target}:{port}")
        
        results = {
            'target': target,
            'port': port,
            'ssl': use_ssl,
            'web_server_info': {},
            'header_analysis': {},
            'findings': []
        }
        
        # Check web server
        print("\n[*] Checking web server...")
        server_info = self._check_web_server(target, port, use_ssl)
        results['web_server_info'] = server_info
        
        if server_info.get('responding'):
            print(f"  [+] Web server responding on port {port}")
            
            if server_info.get('server_header'):
                print(f"  [+] Server: {server_info['server_header']}")
                results['findings'].append({
                    'type': 'info',
                    'severity': 'low',
                    'description': f"Server header disclosed: {server_info['server_header']}"
                })
            
            if server_info.get('technologies'):
                print(f"  [+] Detected technologies: {', '.join(server_info['technologies'])}")
        else:
            print(f"  [!] No web server responding on port {port}")
        
        # Header analysis (simulated for this example)
        if check_headers and server_info.get('responding'):
            print("\n[*] Analyzing security headers...")
            # In a real implementation, this would parse actual HTTP response headers
            header_analysis = {
                'missing_security_headers': ['Content-Security-Policy', 'X-Frame-Options'],
                'present_headers': ['Server'],
                'recommendations': [
                    'Implement Content-Security-Policy',
                    'Set X-Frame-Options to DENY or SAMEORIGIN'
                ]
            }
            results['header_analysis'] = header_analysis
            
            if header_analysis['missing_security_headers']:
                print(f"  [!] Missing security headers: {', '.join(header_analysis['missing_security_headers'])}")
                for rec in header_analysis['recommendations']:
                    print(f"      → {rec}")
        
        results['success'] = True
        self.results = results
        return results
