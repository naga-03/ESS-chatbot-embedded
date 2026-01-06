#!/usr/bin/env python
"""
Test script to verify ESS Chatbot components are working correctly.
Run this before launching the Streamlit app.
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    try:
        from src.auth import AuthManager
        print("  ✅ AuthManager imported")
        
        from src.intent_detector import IntentDetector
        print("  ✅ IntentDetector imported")
        
        from src.entity_extractor import EntityExtractor
        print("  ✅ EntityExtractor imported")
        
        from src.business_logic import BusinessLogicHandler
        print("  ✅ BusinessLogicHandler imported")
        
        from src.chatbot import ESSChatbot
        print("  ✅ ESSChatbot imported")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_data_files():
    """Test that required data files exist."""
    print("\n📁 Checking data files...")
    
    files = [
        "config/intents.json",
        "data/employees.json"
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file} found")
        else:
            print(f"  ❌ {file} not found")
            all_exist = False
    
    return all_exist

def test_authentication():
    """Test authentication system."""
    print("\n🔐 Testing authentication...")
    try:
        from src.auth import AuthManager
        
        auth = AuthManager()
        
        # Test successful login
        success, msg = auth.login("E001", "pass123")
        if success:
            print(f"  ✅ Login successful: {msg}")
        else:
            print(f"  ❌ Login failed: {msg}")
            return False
        
        # Test get current user
        user = auth.get_current_user()
        if user:
            print(f"  ✅ Current user: {user['name']}")
        else:
            print("  ❌ Failed to get current user")
            return False
        
        # Test logout
        success, msg = auth.logout()
        if success:
            print(f"  ✅ Logout successful: {msg}")
        else:
            print(f"  ❌ Logout failed: {msg}")
            return False
        
        # Test invalid login
        success, msg = auth.login("INVALID", "wrong")
        if not success:
            print(f"  ✅ Invalid login correctly rejected")
        else:
            print("  ❌ Invalid login should have failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Authentication test failed: {e}")
        return False

def test_intent_detection():
    """Test intent detection system."""
    print("\n🧠 Testing intent detection...")
    try:
        from src.intent_detector import IntentDetector
        
        detector = IntentDetector()
        
        # Test general query
        intent, confidence = detector.get_intent("What is the leave policy?")
        if intent and confidence > 0.5:
            print(f"  ✅ Detected intent: {intent['intent_id']} (confidence: {confidence:.3f})")
        else:
            print(f"  ⚠️  Low confidence on leave_policy query: {confidence:.3f}")
        
        # Test employee-specific query
        intent, confidence = detector.get_intent("How many leaves do I have?")
        if intent and confidence > 0.5:
            print(f"  ✅ Detected intent: {intent['intent_id']} (confidence: {confidence:.3f})")
        else:
            print(f"  ⚠️  Low confidence on leave_balance query: {confidence:.3f}")
        
        # Test new intents
        intent, confidence = detector.get_intent("Hello")
        if intent and intent['intent_id'] == 'greeting':
            print(f"  ✅ Detected new intent: greeting (confidence: {confidence:.3f})")
        else:
            print(f"  ⚠️  Failed to detect greeting intent")

        intent, confidence = detector.get_intent("What is my profile?")
        if intent and intent['intent_id'] == 'my_profile':
            print(f"  ✅ Detected new intent: my_profile (confidence: {confidence:.3f})")
        else:
            print(f"  ⚠️  Failed to detect my_profile intent")

        intent, confidence = detector.get_intent("What can you do?")
        if intent and intent['intent_id'] == 'general_inquiry':
            print(f"  ✅ Detected new intent: general_inquiry (confidence: {confidence:.3f})")
        else:
            print(f"  ⚠️  Failed to detect general_inquiry intent")

        # Test private intent detection
        is_private = detector.is_private_intent("leave_balance")
        if is_private:
            print(f"  ✅ Correctly identified private intent")
        else:
            print(f"  ❌ Failed to identify private intent")
            return False

        return True
    except Exception as e:
        print(f"  ❌ Intent detection test failed: {e}")
        return False

def test_entity_extraction():
    """Test entity extraction system."""
    print("\n📝 Testing entity extraction...")
    try:
        from src.entity_extractor import EntityExtractor
        
        extractor = EntityExtractor()
        
        # Test date extraction
        entities = extractor.extract_entities("I want leave on Jan 15 for 3 days")
        
        if entities['dates']:
            print(f"  ✅ Extracted dates: {entities['dates']}")
        else:
            print(f"  ⚠️  No dates extracted")
        
        if entities['leave_duration']['days']:
            print(f"  ✅ Extracted leave duration: {entities['leave_duration']['days']} days")
        else:
            print(f"  ⚠️  No leave duration extracted")
        
        return True
    except Exception as e:
        print(f"  ❌ Entity extraction test failed: {e}")
        return False

def test_business_logic():
    """Test business logic handlers."""
    print("\n⚙️  Testing business logic...")
    try:
        from src.auth import AuthManager
        from src.business_logic import BusinessLogicHandler
        
        auth = AuthManager()
        business_logic = BusinessLogicHandler()
        
        # Test general query
        response = business_logic.handle_intent("leave_policy", auth)
        if response['success']:
            print(f"  ✅ General query handled: leave_policy")
        else:
            print(f"  ❌ Failed to handle general query")
            return False
        
        # Test employee-specific query (without login)
        response = business_logic.handle_intent("leave_balance", auth)
        if not response['success']:
            print(f"  ✅ Correctly rejected unauthorized query")
        else:
            print(f"  ❌ Should reject unauthorized query")
            return False
        
        # Test after login
        auth.login("E001", "pass123")
        response = business_logic.handle_intent("leave_balance", auth)
        if response['success']:
            print(f"  ✅ Employee query handled after login: {response['data']['leave_balance']} leaves")
        else:
            print(f"  ❌ Failed to handle employee query after login")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Business logic test failed: {e}")
        return False

def test_chatbot():
    """Test main chatbot."""
    print("\n🤖 Testing chatbot...")
    try:
        from src.chatbot import ESSChatbot
        
        chatbot = ESSChatbot()
        
        # Test general query
        response = chatbot.process_message("What is the leave policy?")
        if response['success']:
            print(f"  ✅ General query processed: {response['intent']}")
        else:
            print(f"  ⚠️  Could not process query")
        
        # Test login
        response = chatbot.process_message("/login E001 pass123")
        if response['success']:
            print(f"  ✅ Login successful")
        else:
            print(f"  ❌ Login failed: {response['message']}")
            return False
        
        # Test employee query
        response = chatbot.process_message("How many leaves do I have?")
        if response['success']:
            print(f"  ✅ Employee query processed: {response['data']['leave_balance']} leaves")
        else:
            print(f"  ❌ Employee query failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Chatbot test failed: {e}")
        return False

def test_phone_update_flow():
    """Test the complete phone number update flow."""
    print("\n📱 Testing phone number update flow...")
    try:
        from src.chatbot import ESSChatbot

        chatbot = ESSChatbot()
        new_phone_number = "9876543210"
        
        # Step 1: Login
        response = chatbot.process_message("/login E001 pass123")
        if not response['success']:
            print("  ❌ Login failed, aborting test.")
            return False
        print("  ✅ Step 1: Login successful.")

        # Step 2: Initiate phone update
        response = chatbot.process_message("I want to update my phone number")
        if response['success'] and response['data'].get('next_action') == 'prompt_for_phone':
            print("  ✅ Step 2: Chatbot correctly asked for the new phone number.")
        else:
            print("  ❌ Step 2: Chatbot failed to ask for the new phone number.")
            return False

        # Step 3: Provide new phone number
        response = chatbot.process_message(f"My new number is {new_phone_number}")
        if response['success'] and "successfully updated" in response['message']:
            print("  ✅ Step 3: Phone number updated successfully.")
        else:
            print("  ❌ Step 3: Phone number update failed.")
            return False
            
        # Step 5: Verify the change in the JSON file
        with open("data/employees.json", 'r') as f:
            employees_data = json.load(f)
        
        updated_user = next((emp for emp in employees_data['employees'] if emp['employee_id'] == 'E001'), None)
        
        if updated_user and updated_user.get('phone') == new_phone_number:
            print("  ✅ Step 5: Phone number correctly updated in employees.json.")
        else:
            print("  ❌ Step 5: Phone number not updated in employees.json.")
            # Revert the change for consistency
            return False

        # Revert the phone number for consistent tests
        updated_user['phone'] = "123-456-7890"
        with open("data/employees.json", 'w') as f:
            json.dump(employees_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"  ❌ Phone update flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("  ESS Chatbot - System Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Authentication", test_authentication()))
    results.append(("Intent Detection", test_intent_detection()))
    results.append(("Entity Extraction", test_entity_extraction()))
    results.append(("Business Logic", test_business_logic()))
    results.append(("Chatbot", test_chatbot()))
    results.append(("Phone Update Flow", test_phone_update_flow()))
    
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n  Result: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✨ All tests passed! You're ready to run: streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above and install missing dependencies.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
