#!/usr/bin/env python3
"""
Test script for session-based code generation.
Demonstrates the new feature where each generation gets its own timestamped folder.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.file_tools import FileTools
from config import Config

def test_session_generation():
    """Test the new session-based code generation feature."""
    
    print("=" * 80)
    print("🧪 Testing Session-Based Code Generation")
    print("=" * 80)
    
    # Test 1: Start first generation session
    print("\n[Test 1] Starting first generation session...")
    session1 = FileTools.start_generation_session("QuickSort_Algorithm")
    print(f"✓ Session 1 created: {session1}")
    
    # Verify session 1 directory exists
    session1_path = Path(session1)
    assert session1_path.exists(), "Session 1 directory not created!"
    print(f"✓ Session 1 directory verified: {session1_path}")
    
    # Test 2: Save code to session 1
    print("\n[Test 2] Saving code to session 1...")
    quick_sort_code = '''"""
Quick Sort Algorithm Implementation
"""

def quick_sort(arr):
    """
    Sort array using Quick Sort algorithm.
    
    Args:
        arr: List of elements to sort
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    test_array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"Original array: {test_array}")
    sorted_array = quick_sort(test_array)
    print(f"Sorted array: {sorted_array}")
'''
    
    saved_path1 = FileTools.save_code("quick_sort.py", quick_sort_code)
    print(f"✓ Code saved: {saved_path1}")
    
    # Verify file exists and has content
    assert Path(saved_path1).exists(), "File not created!"
    with open(saved_path1, 'r') as f:
        content = f.read()
        assert len(content) > 0, "File is empty!"
    print(f"✓ File verified: {len(content)} bytes")
    
    # Test 3: Start second generation session
    print("\n[Test 3] Starting second generation session...")
    session2 = FileTools.start_generation_session("BinarySearch_Implementation")
    print(f"✓ Session 2 created: {session2}")
    
    # Verify session 2 directory exists and is different from session 1
    session2_path = Path(session2)
    assert session2_path.exists(), "Session 2 directory not created!"
    assert session1_path != session2_path, "Sessions have same directory!"
    print(f"✓ Session 2 directory verified: {session2_path}")
    print(f"✓ Sessions are isolated: {session1_path.name} != {session2_path.name}")
    
    # Test 4: Save code to session 2
    print("\n[Test 4] Saving code to session 2...")
    binary_search_code = '''"""
Binary Search Algorithm Implementation
"""

def binary_search(arr, target):
    """
    Search for target in sorted array using Binary Search.
    
    Args:
        arr: Sorted list to search
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


if __name__ == "__main__":
    sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    targets = [5, 11]
    for target in targets:
        result = binary_search(sorted_array, target)
        if result != -1:
            print(f"Found {target} at index {result}")
        else:
            print(f"Target {target} not found")
'''
    
    saved_path2 = FileTools.save_code("binary_search.py", binary_search_code)
    print(f"✓ Code saved: {saved_path2}")
    
    # Verify file exists in session 2
    assert Path(saved_path2).exists(), "File not created in session 2!"
    with open(saved_path2, 'r') as f:
        content = f.read()
        assert len(content) > 0, "File in session 2 is empty!"
    print(f"✓ File verified in session 2: {len(content)} bytes")
    
    # Test 5: Verify session isolation
    print("\n[Test 5] Verifying session isolation...")
    
    # List files in session 1
    session1_files = list(Path(session1).glob("**/*.py"))
    print(f"Files in session 1: {[f.name for f in session1_files]}")
    
    # List files in session 2
    session2_files = list(Path(session2).glob("**/*.py"))
    print(f"Files in session 2: {[f.name for f in session2_files]}")
    
    # Verify isolation
    assert len(session1_files) >= 1, "Session 1 should have at least 1 file"
    assert len(session2_files) >= 1, "Session 2 should have at least 1 file"
    assert session1_files != session2_files, "Sessions should have different files"
    print("✓ Sessions are properly isolated!")
    
    # Test 6: Directory structure summary
    print("\n[Test 6] Directory structure summary:")
    print(f"\nWorkspace root: {FileTools.WORKSPACE_DIR}")
    
    # Show directory tree
    print("\n📁 Generated folder structure:")
    for session_dir in sorted(FileTools.WORKSPACE_DIR.iterdir()):
        if session_dir.is_dir() and (session_dir.name.startswith("session_") or session_dir.name[0].isdigit()):
            print(f"\n  {session_dir.name}/")
            for file in sorted(session_dir.glob("**/*")):
                if file.is_file():
                    relative = file.relative_to(session_dir)
                    size = file.stat().st_size
                    print(f"    ├── {relative} ({size} bytes)")
    
    print("\n" + "=" * 80)
    print("✅ All tests passed! Session-based generation is working correctly.")
    print("=" * 80)
    
    print("\n📝 Summary:")
    print(f"  • Session 1 folder: {session1_path.name}")
    print(f"    └── Contains: quick_sort.py")
    print(f"  • Session 2 folder: {session2_path.name}")
    print(f"    └── Contains: binary_search.py")
    print(f"\n💡 Each time you generate code, a new timestamped folder is created!")
    print(f"   This keeps your code organized and prevents overwriting previous generations.")


if __name__ == "__main__":
    try:
        test_session_generation()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
