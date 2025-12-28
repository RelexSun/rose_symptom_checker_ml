import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    original = content
    
    # Fix 1: Change 'from rose_symptom_checker.' to 'from rose_symptom_checker.'
    content = re.sub(
        r'from src\.',
        'from rose_symptom_checker.',
        content
    )
    
    # Fix 2: Change 'import rose_symptom_checker.' to 'import rose_symptom_checker.'
    content = re.sub(
        r'import src\.',
        'import rose_symptom_checker.',
        content
    )
    
    # Fix 3: Remove duplicate 'rose_symptom_checker.rose_symptom_checker.'
    content = re.sub(
        r'from rose_symptom_checker\.rose_symptom_checker\.',
        'from rose_symptom_checker.',
        content
    )
    
    # Fix 4: Remove duplicate in import statements
    content = re.sub(
        r'import rose_symptom_checker\.rose_symptom_checker\.',
        'import rose_symptom_checker.',
        content
    )
    
    if content != original:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {file_path.relative_to(Path.cwd())}")
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    return False

def main():
    """Fix all Python files in the project"""
    project_root = Path(__file__).parent.parent
    
    # Directories to process
    directories = [
        project_root / "src" / "rose_symptom_checker",
        project_root / "scripts",
        project_root / "tests",
    ]
    
    updated_files = 0
    total_files = 0
    
    print("=" * 60)
    print("Fixing Imports in Rose Symptom Checker")
    print("=" * 60)
    print()
    
    for directory in directories:
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            continue
        
        print(f"Processing: {directory}")
        print("-" * 60)
        
        for py_file in directory.rglob("*.py"):
            # Skip __pycache__ and other generated files
            if "__pycache__" in str(py_file) or ".egg" in str(py_file):
                continue
            
            total_files += 1
            if fix_imports_in_file(py_file):
                updated_files += 1
        
        print()
    
    print("=" * 60)
    print(f"✅ Processed {total_files} files")
    print(f"✅ Updated {updated_files} files")
    print("=" * 60)
    
    if updated_files == 0:
        print("\n✨ All imports are already correct!")
    else:
        print(f"\n✨ Fixed imports in {updated_files} files!")

if __name__ == "__main__":
    main()