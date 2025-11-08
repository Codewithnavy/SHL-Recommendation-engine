"""
Setup script to help configure the Google Gemini API key
"""

import os
import sys

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("Creating .env file from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env:
                env.write(content)
            print("✓ Created .env file")
        else:
            with open('.env', 'w') as env:
                env.write("GOOGLE_API_KEY=\n")
            print("✓ Created .env file")
    else:
        print("✓ .env file exists")

def check_api_key():
    """Check if API key is set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or not api_key.strip():
        return False
    return True

def main():
    print("="*80)
    print("Google Gemini API Setup")
    print("="*80)
    
    # Check .env file
    check_env_file()
    
    # Check API key
    if check_api_key():
        print("\n✓ GOOGLE_API_KEY is configured!")
        print("\nYou can now run the application:")
        print("  python app/main.py")
        return 0
    else:
        print("\n⚠ GOOGLE_API_KEY is not set or empty")
        print("\nTo get your FREE Google Gemini API key:")
        print("="*80)
        print("\n1. Visit: https://ai.google.dev/gemini-api/docs/api-key")
        print("\n2. Click 'Get an API key' button")
        print("\n3. Sign in with your Google account")
        print("\n4. Click 'Create API key in new project' or use existing project")
        print("\n5. Copy the generated API key")
        print("\n6. Edit the .env file in this directory:")
        print(f"   {os.path.abspath('.env')}")
        print("\n7. Add your key:")
        print("   GOOGLE_API_KEY=AIza...")
        print("\n8. Save the file and run this script again")
        print("\n" + "="*80)
        print("\nFree Tier Limits:")
        print("  - 60 requests per minute")
        print("  - 1,500 requests per day")
        print("  - More than enough for this project!")
        print("\n" + "="*80)
        print("\nNote: Without API key, the system will use keyword-based recommendations")
        print("      which work but are less accurate than semantic search.")
        print("\n" + "="*80)
        
        # Open .env file for editing
        env_path = os.path.abspath('.env')
        print(f"\nOpening .env file for you to edit...")
        print(f"File location: {env_path}")
        
        if sys.platform == 'win32':
            os.system(f'notepad "{env_path}"')
        elif sys.platform == 'darwin':
            os.system(f'open -e "{env_path}"')
        else:
            os.system(f'nano "{env_path}"')
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
