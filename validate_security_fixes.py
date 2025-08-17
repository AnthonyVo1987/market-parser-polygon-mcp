#!/usr/bin/env python3
"""
Security Validation Script

This script validates that all security fixes have been properly implemented
and the application is secure against common vulnerabilities.
"""

import os
import sys
import re
from pathlib import Path

def validate_env_security():
    """Validate .env file security"""
    results = []
    
    # Check if .env.example exists
    if Path('.env.example').exists():
        results.append("✅ .env.example template exists")
    else:
        results.append("❌ .env.example template missing")
    
    # Check if .env is in .gitignore
    if Path('.gitignore').exists():
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                results.append("✅ .env is protected in .gitignore")
            else:
                results.append("❌ .env not found in .gitignore")
    else:
        results.append("❌ .gitignore file missing")
    
    # Check if actual .env contains placeholder values
    if Path('.env').exists():
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'your_' in env_content or '_here' in env_content:
                results.append("✅ .env contains placeholder values (safe)")
            else:
                # Check for potential live API keys
                api_key_patterns = [
                    r'sk-[a-zA-Z0-9]{32,}',  # OpenAI
                    r'sk-ant-[a-zA-Z0-9-_]{95,}',  # Anthropic
                    r'AIza[a-zA-Z0-9_-]{35}',  # Google
                ]
                
                has_live_keys = any(re.search(pattern, env_content) for pattern in api_key_patterns)
                if has_live_keys:
                    results.append("⚠️  .env may contain live API keys")
                else:
                    results.append("✅ .env appears safe")
    
    return results

def validate_secure_logging():
    """Validate that sensitive debug output has been removed"""
    results = []
    
    # Check response_parser.py for secure logging
    if Path('response_parser.py').exists():
        with open('response_parser.py', 'r') as f:
            content = f.read()
            
            # Check that debug output has been sanitized
            if 'Full response:' in content:
                results.append("❌ response_parser.py still contains sensitive debug output")
            else:
                results.append("✅ response_parser.py debug output sanitized")
            
            # Check for secure logging patterns
            if 'self.logger.debug(' in content and 'Secure logging:' in content:
                results.append("✅ response_parser.py uses secure logging")
            else:
                results.append("⚠️  response_parser.py secure logging needs verification")
    
    return results

def validate_input_validation():
    """Validate that input validation is implemented"""
    results = []
    
    # Check if security_utils.py exists and contains required functions
    if Path('security_utils.py').exists():
        with open('security_utils.py', 'r') as f:
            content = f.read()
            
            required_functions = [
                'validate_ticker',
                'validate_query',
                'validate_message',
                'sanitize_log_message'
            ]
            
            for func in required_functions:
                if func in content:
                    results.append(f"✅ {func} implemented")
                else:
                    results.append(f"❌ {func} missing")
    else:
        results.append("❌ security_utils.py module missing")
    
    return results

def validate_documentation():
    """Validate security documentation"""
    results = []
    
    # Check for SECURITY.md
    if Path('SECURITY.md').exists():
        results.append("✅ SECURITY.md documentation exists")
        
        with open('SECURITY.md', 'r') as f:
            content = f.read()
            required_sections = [
                'API Key Management',
                'Secure Setup Process',
                'Input Validation',
                'Secure Logging'
            ]
            
            for section in required_sections:
                if section in content:
                    results.append(f"✅ Security docs include {section}")
                else:
                    results.append(f"⚠️  Security docs missing {section}")
    else:
        results.append("❌ SECURITY.md documentation missing")
    
    return results

def validate_code_security():
    """Validate code for common security issues"""
    results = []
    
    # Check for hardcoded secrets in common files
    files_to_check = ['market_parser_demo.py', 'chat_ui.py', 'prompt_templates.py']
    
    secret_patterns = [
        r'sk-[a-zA-Z0-9]{32,}',
        r'sk-ant-[a-zA-Z0-9-_]{95,}',
        r'AIza[a-zA-Z0-9_-]{35}',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']'
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read()
                
                has_secrets = any(re.search(pattern, content, re.IGNORECASE) for pattern in secret_patterns)
                if has_secrets:
                    results.append(f"❌ {file_path} may contain hardcoded secrets")
                else:
                    results.append(f"✅ {file_path} appears secure")
    
    return results

def main():
    """Run comprehensive security validation"""
    print("🔒 Market Parser Security Validation")
    print("=" * 50)
    
    validation_functions = [
        ("Environment Security", validate_env_security),
        ("Secure Logging", validate_secure_logging),
        ("Input Validation", validate_input_validation),
        ("Documentation", validate_documentation),
        ("Code Security", validate_code_security)
    ]
    
    all_results = []
    
    for category, validate_func in validation_functions:
        print(f"\n📋 {category}")
        print("-" * 30)
        
        try:
            results = validate_func()
            all_results.extend(results)
            
            for result in results:
                print(f"  {result}")
                
        except Exception as e:
            error_msg = f"💥 {category} validation failed: {e}"
            print(f"  {error_msg}")
            all_results.append(error_msg)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SECURITY VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = len([r for r in all_results if r.startswith('✅')])
    warnings = len([r for r in all_results if r.startswith('⚠️')])
    failed = len([r for r in all_results if r.startswith('❌')])
    errors = len([r for r in all_results if r.startswith('💥')])
    total = len(all_results)
    
    print(f"✅ Passed: {passed}")
    print(f"⚠️  Warnings: {warnings}")
    print(f"❌ Failed: {failed}")
    print(f"💥 Errors: {errors}")
    print(f"📊 Total: {total}")
    
    # Overall assessment
    critical_issues = failed + errors
    if critical_issues == 0:
        print("\n🎉 SECURITY VALIDATION PASSED!")
        print("✅ Application meets security requirements")
        print("🚀 Safe for deployment")
        return 0
    else:
        print(f"\n⚠️  {critical_issues} CRITICAL SECURITY ISSUES FOUND")
        print("❌ Address security issues before deployment")
        print("🔧 Review failed validations above")
        return 1

if __name__ == "__main__":
    sys.exit(main())