#!/usr/bin/env python3
"""
System Status Check
Quick verification that all components are working
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        "backend/analysis/gmail_analyzer.py",
        "backend/analysis/providers/deepseek_adapter.py", 
        "backend/app/main.py",
        "backend/app/routes/analyze.py",
        ".env"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    print("✅ All required files present")
    return True

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking environment...")
    
    # Try to load .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment file loaded")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    # Check API key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key and api_key != "your_deepseek_api_key_here":
        print(f"✅ DeepSeek API key configured: {api_key[:15]}...")
        return True
    else:
        print("❌ DeepSeek API key not found or invalid")
        return False

def check_imports():
    """Check if all required modules can be imported"""
    print("\n📦 Checking imports...")
    
    # Add backend to path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    try:
        import requests
        print("✅ requests")
        
        from fastapi import FastAPI
        print("✅ fastapi")
        
        from analysis.gmail_analyzer import GmailAnalyzer
        print("✅ gmail_analyzer")
        
        from analysis.providers.deepseek_adapter import DeepSeekAdapter
        print("✅ deepseek_adapter")
        
        from app.main import app
        print("✅ FastAPI app")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def quick_functionality_test():
    """Quick test of core functionality"""
    print("\n🧪 Quick functionality test...")
    
    try:
        # Set environment
        os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY", "")
        
        from analysis.providers.deepseek_adapter import DeepSeekAdapter
        
        adapter = DeepSeekAdapter(os.environ["DEEPSEEK_API_KEY"])
        
        # Test with mock-friendly input
        result = adapter.analyze_text("Extract people from: John Smith and Sarah met.")
        
        if result and len(result) > 10:  # Should return some meaningful content
            print("✅ DeepSeek adapter responding")
            print(f"   Sample response: {result[:100]}...")
            return True
        else:
            print("❌ DeepSeek adapter not responding properly")
            return False
            
    except Exception as e:
        print(f"❌ Functionality test failed: {str(e)}")
        return False

def main():
    """Run all status checks"""
    print("🔍 GenAI Go System Status Check")
    print("=" * 40)
    
    checks = [
        ("File Structure", check_files),
        ("Environment", check_environment), 
        ("Module Imports", check_imports),
        ("Core Functionality", quick_functionality_test)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔎 {check_name}")
        print("-" * 20)
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"❌ Check failed: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 STATUS SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for check_name, success in results:
        status = "✅ OK" if success else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    health_percentage = (passed / total) * 100
    print(f"\nSystem Health: {health_percentage:.1f}% ({passed}/{total})")
    
    if passed == total:
        print("\n🎉 System is fully operational!")
        print("Ready to test mail analysis with LLM.")
    elif passed >= total * 0.75:
        print("\n⚠️ System mostly operational with minor issues.")
    else:
        print("\n❌ System has significant issues that need attention.")
    
    print("\n💡 Next steps:")
    if passed == total:
        print("   Run: python test_complete_analysis.py")
    else:
        print("   Fix the failed checks above first")

if __name__ == "__main__":
    main()
