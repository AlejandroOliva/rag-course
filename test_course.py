#!/usr/bin/env python3
"""
Test script for RAG Course
=========================

This script tests the basic structure and functionality of the RAG course
without requiring external dependencies.

Author: RAG Course
Date: January 2025
"""

import os
import sys
import json
from pathlib import Path

def test_course_structure():
    """Test that the course structure is correct."""
    print("🔍 Testing RAG Course Structure...")
    
    # Define expected structure
    expected_files = [
        "README.md",
        "COURSE-INFO.md", 
        "START-HERE.md",
        "QUICK-GUIDE.md",
        "ADDITIONAL-RESOURCES.md",
        "VERIFICATION-REPORT.md",
        "requirements.txt"
    ]
    
    expected_dirs = [
        "module-01-introduction",
        "module-02-fundamentals", 
        "module-03-advanced-concepts",
        "module-04-vector-databases",
        "module-05-embeddings",
        "module-06-retrieval-strategies",
        "module-07-practical-projects",
        "examples",
        "containers"
    ]
    
    # Test files
    missing_files = []
    for file in expected_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    # Test directories
    missing_dirs = []
    for dir_name in expected_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    # Report results
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
    else:
        print("✅ All required files present")
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
    else:
        print("✅ All required directories present")
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def test_examples():
    """Test that examples are properly structured."""
    print("\n🔍 Testing Examples...")
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found")
        return False
    
    # Check for example subdirectories
    example_dirs = [d for d in examples_dir.iterdir() if d.is_dir()]
    
    if len(example_dirs) == 0:
        print("❌ No example directories found")
        return False
    
    print(f"✅ Found {len(example_dirs)} example directories:")
    for example_dir in example_dirs:
        print(f"  - {example_dir.name}")
        
        # Check for required files in each example
        required_files = ["README.md", "requirements.txt"]
        for file in required_files:
            if (example_dir / file).exists():
                print(f"    ✅ {file}")
            else:
                print(f"    ❌ Missing {file}")
    
    return True

def test_module_content():
    """Test that modules have proper content."""
    print("\n🔍 Testing Module Content...")
    
    # Test Module 1 (should be complete)
    module1_dir = Path("module-01-introduction")
    if not module1_dir.exists():
        print("❌ Module 1 directory not found")
        return False
    
    module1_readme = module1_dir / "README.md"
    if not module1_readme.exists():
        print("❌ Module 1 README not found")
        return False
    
    # Check content length
    with open(module1_readme, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if len(content) < 1000:  # Should be substantial
        print("❌ Module 1 content seems too short")
        return False
    
    print("✅ Module 1 content looks good")
    
    # Check other modules exist (even if empty)
    other_modules = [
        "module-02-fundamentals",
        "module-03-advanced-concepts", 
        "module-04-vector-databases",
        "module-05-embeddings",
        "module-06-retrieval-strategies",
        "module-07-practical-projects"
    ]
    
    for module in other_modules:
        if Path(module).exists():
            print(f"✅ {module} directory exists")
        else:
            print(f"❌ {module} directory missing")
    
    return True

def test_containers():
    """Test container configuration."""
    print("\n🔍 Testing Container Configuration...")
    
    containers_dir = Path("containers")
    if not containers_dir.exists():
        print("❌ Containers directory not found")
        return False
    
    # Check for Dockerfiles
    dockerfiles = list(containers_dir.glob("Dockerfile*"))
    if len(dockerfiles) == 0:
        print("❌ No Dockerfiles found")
        return False
    
    print(f"✅ Found {len(dockerfiles)} Dockerfiles:")
    for dockerfile in dockerfiles:
        print(f"  - {dockerfile.name}")
    
    # Check for docker-compose
    compose_file = containers_dir / "docker-compose.yml"
    if compose_file.exists():
        print("✅ docker-compose.yml found")
    else:
        print("❌ docker-compose.yml not found")
    
    return True

def test_documentation():
    """Test documentation quality."""
    print("\n🔍 Testing Documentation Quality...")
    
    # Check main README
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("❌ Main README not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for key sections
    key_sections = [
        "Course Index",
        "Learning Objectives", 
        "Prerequisites",
        "Technology Stack"
    ]
    
    missing_sections = []
    for section in key_sections:
        if section not in readme_content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing sections in README: {missing_sections}")
    else:
        print("✅ README contains all key sections")
    
    # Check file sizes
    doc_files = [
        "COURSE-INFO.md",
        "START-HERE.md", 
        "QUICK-GUIDE.md",
        "ADDITIONAL-RESOURCES.md"
    ]
    
    for doc_file in doc_files:
        if Path(doc_file).exists():
            size = Path(doc_file).stat().st_size
            if size > 1000:  # Should be substantial
                print(f"✅ {doc_file} has good content ({size} bytes)")
            else:
                print(f"⚠️ {doc_file} seems short ({size} bytes)")
    
    return len(missing_sections) == 0

def generate_test_report():
    """Generate a comprehensive test report."""
    print("\n" + "="*60)
    print("📊 RAG COURSE TEST REPORT")
    print("="*60)
    
    tests = [
        ("Course Structure", test_course_structure),
        ("Examples", test_examples),
        ("Module Content", test_module_content),
        ("Container Configuration", test_containers),
        ("Documentation Quality", test_documentation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Course is ready for use.")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the issues above.")
        return False

def main():
    """Main test function."""
    print("🚀 Starting RAG Course Tests")
    print("="*60)
    
    # Change to course directory
    course_dir = Path(__file__).parent
    os.chdir(course_dir)
    
    # Run tests
    success = generate_test_report()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
