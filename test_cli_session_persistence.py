#!/usr/bin/env python3
"""
Test script for CLI session persistence functionality.
Tests that CLI maintains conversation history across messages.
"""

import subprocess
import sys
import time


def test_cli_session_persistence():
    """Test CLI session persistence with two related prompts."""
    print("🧪 Testing CLI Session Persistence")
    print("=" * 50)
    
    # Test prompts
    prompts = [
        "Current Market Status",
        "What about NVDA?"
    ]
    
    results = []
    
    try:
        # Start CLI process
        print("🚀 Starting CLI process...")
        process = subprocess.Popen(
            [sys.executable, "-m", "uv", "run", "src/backend/main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Wait for CLI to initialize
        time.sleep(3)
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📝 Sending Test Prompt {i}: '{prompt}'")
            start_time = time.time()
            
            # Send prompt
            process.stdin.write(prompt + "\n")
            process.stdin.flush()
            
            # Read response with timeout
            try:
                # Read until we see the prompt again or timeout
                response_lines = []
                timeout_start = time.time()
                
                while time.time() - timeout_start < 120:  # 120s timeout
                    if process.poll() is not None:
                        break
                    
                    try:
                        line = process.stdout.readline()
                        if line:
                            response_lines.append(line.strip())
                            print(f"📄 {line.strip()}")
                            
                            # Check if we're back to prompt
                            if line.strip() == "> ":
                                break
                    except Exception:
                        break
                
                end_time = time.time()
                response_time = end_time - start_time
                
                result = {
                    "prompt": prompt,
                    "response_time": response_time,
                    "response_lines": response_lines,
                    "success": True
                }
                
                print(f"✅ Response time: {response_time:.2f}s")
                results.append(result)
                
            except Exception as e:
                print(f"❌ Error with prompt {i}: {e}")
                results.append({
                    "prompt": prompt,
                    "error": str(e),
                    "success": False
                })
        
        # Send exit command
        print("\n🚪 Sending exit command...")
        process.stdin.write("exit\n")
        process.stdin.flush()
        
        # Wait for process to finish
        process.wait(timeout=10)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    # Analyze results
    print("\n📊 Session Persistence Analysis")
    print("=" * 50)
    
    if len(results) >= 2:
        # Check if second response references first response context
        first_response = " ".join(results[0].get("response_lines", []))
        second_response = " ".join(results[1].get("response_lines", []))
        
        print(f"📝 First response length: {len(first_response)} characters")
        print(f"📝 Second response length: {len(second_response)} characters")
        
        # Look for context references
        context_indicators = [
            "market status", "previous", "earlier", "mentioned", 
            "as discussed", "building on", "following up"
        ]
        
        context_found = any(indicator in second_response.lower() for indicator in context_indicators)
        
        print(f"🔍 Context reference found: {'✅ Yes' if context_found else '❌ No'}")
        
        if context_found:
            print("✅ CLI Session Persistence: PASSED")
            return True
        else:
            print("❌ CLI Session Persistence: FAILED - No context reference found")
            return False
    else:
        print("❌ CLI Session Persistence: FAILED - Insufficient responses")
        return False

if __name__ == "__main__":
    success = test_cli_session_persistence()
    sys.exit(0 if success else 1)
