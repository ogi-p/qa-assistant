#!/usr/bin/env python3
"""
Test JQL Search Capabilities

This script tests different JQL search approaches to find the right way
to search for tickets where the current user is QA Assignee.
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_jql_search():
    """Test different JQL search approaches."""
    
    jira_server = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Testing JQL Search Capabilities...")
    print("=" * 50)
    
    # Test 1: Simple search to see if basic JQL works
    print("1️⃣ Testing basic JQL search...")
    search_data = {
        "jql": "project = AP",
        "startAt": 0,
        "maxResults": 5,
        "fields": ["summary", "status"]
    }
    
    response = requests.post(
        f"{jira_server}/rest/api/2/search",
        auth=(jira_email, jira_token),
        headers=headers,
        json=search_data,
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Basic search works! Found {results.get('total', 0)} tickets")
    else:
        print(f"❌ Basic search failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test 2: Search for tickets where current user is assignee
    print("\n2️⃣ Testing assignee search...")
    search_data = {
        "jql": "assignee = currentUser()",
        "startAt": 0,
        "maxResults": 5,
        "fields": ["summary", "status", "assignee"]
    }
    
    response = requests.post(
        f"{jira_server}/rest/api/2/search",
        auth=(jira_email, jira_token),
        headers=headers,
        json=search_data,
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Assignee search works! Found {results.get('total', 0)} tickets")
    else:
        print(f"❌ Assignee search failed: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 3: Search for tickets where current user is reporter
    print("\n3️⃣ Testing reporter search...")
    search_data = {
        "jql": "reporter = currentUser()",
        "startAt": 0,
        "maxResults": 5,
        "fields": ["summary", "status", "reporter"]
    }
    
    response = requests.post(
        f"{jira_server}/rest/api/2/search",
        auth=(jira_email, jira_token),
        headers=headers,
        json=search_data,
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Reporter search works! Found {results.get('total', 0)} tickets")
    else:
        print(f"❌ Reporter search failed: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 4: Try to get field metadata
    print("\n4️⃣ Testing field metadata...")
    response = requests.get(
        f"{jira_server}/rest/api/2/field",
        auth=(jira_email, jira_token),
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        fields = response.json()
        print(f"✅ Field metadata works! Found {len(fields)} fields")
        
        # Look for QA Assignee field
        qa_fields = [f for f in fields if 'qa' in f.get('name', '').lower() and 'assignee' in f.get('name', '').lower()]
        if qa_fields:
            print(f"✅ Found QA Assignee fields: {[f['id'] for f in qa_fields]}")
        else:
            print("❌ No QA Assignee fields found in field metadata")
    else:
        print(f"❌ Field metadata failed: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 5: Try searching with custom field ID
    print("\n5️⃣ Testing custom field search...")
    search_data = {
        "jql": "customfield_11207 IS NOT EMPTY",
        "startAt": 0,
        "maxResults": 5,
        "fields": ["summary", "status"]
    }
    
    response = requests.post(
        f"{jira_server}/rest/api/2/search",
        auth=(jira_email, jira_token),
        headers=headers,
        json=search_data,
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Custom field search works! Found {results.get('total', 0)} tickets with customfield_11207")
    else:
        print(f"❌ Custom field search failed: {response.status_code}")
        print(f"Response: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 JQL search testing complete!")
    return True

if __name__ == "__main__":
    success = test_jql_search()
    sys.exit(0 if success else 1)
