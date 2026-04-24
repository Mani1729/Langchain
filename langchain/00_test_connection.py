"""
Quick Test - Azure OpenAI Connection
=====================================

This script tests your Azure OpenAI connection and verifies everything is working.
Run this first before going through the tutorials.
"""

print("🔧 Testing Azure OpenAI Connection...\n")

try:
    from langchain_openai import AzureChatOpenAI
    
    # Initialize with your Azure OpenAI credentials
    llm = AzureChatOpenAI(
        azure_endpoint="https://your-resource-name.openai.azure.com",
        api_key="YOUR_AZURE_OPENAI_API_KEY",
        api_version="2025-01-01-preview",
        deployment_name="gpt-4o-mini",
        temperature=0.7
    )
    print("✅ Azure OpenAI client initialized successfully!\n")
    
    # Test a simple call
    print("🤖 Testing LLM call...")
    response = llm.invoke("Say 'Hello! Azure OpenAI is working!' in a friendly way.")
    
    print(f"\n✅ SUCCESS! Response received:\n")
    print(f"📝 {response.content}\n")
    
    print("=" * 60)
    print("🎉 Your Azure OpenAI setup is working perfectly!")
    print("=" * 60)
    print("\n📚 You're ready to start learning LangChain!")
    print("\nNext steps:")
    print("1. Run: python 01_basics_and_setup.py")
    print("2. Follow the tutorials in order (01 through 09)")
    print("3. Complete the practice exercises in README.md")
    print("\nHappy learning! 🚀\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}\n")
    print("Troubleshooting:")
    print("1. Check if langchain-openai is installed: pip install langchain-openai")
    print("2. Verify your Azure OpenAI credentials are correct")
    print("3. Ensure your Azure OpenAI deployment is active")
    print("4. Check your internet connection\n")
