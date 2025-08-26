#!/usr/bin/env python3
"""
Simple QA Workload Reader

This script shows all tickets where the current user is assignee
and displays the QA Assignee field for each ticket.
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_qa_workload():
    """Get all tickets where current user is assignee and show QA Assignee field."""
    
    jira_server = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Finding tickets where you are assignee...")
    print("=" * 60)
    
    # Search for tickets where user is assignee
    search_url = f"{jira_server}/rest/api/2/search"
    search_data = {
        "jql": "assignee = currentUser()",
        "startAt": 0,
        "maxResults": 50,
        "fields": ["summary", "status", "issuetype", "priority", "assignee"]
    }
    
    response = requests.post(
        search_url,
        auth=(jira_email, jira_token),
        headers=headers,
        json=search_data,
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"❌ Search failed (Status: {response.status_code})")
        print(f"📄 Response: {response.text}")
        return False
    
    search_results = response.json()
    tickets = search_results.get('issues', [])
    total = search_results.get('total', 0)
    
    print(f"✅ Found {total} tickets where you are assignee")
    print()
    
    if not tickets:
        print("📝 No tickets found where you are assignee")
        return True
    
    # For each ticket, get the full data including QA Assignee
    for i, ticket in enumerate(tickets, 1):
        ticket_key = ticket.get('key')
        print(f"{i}. 🎫 {ticket_key}")
        print(f"   📝 {ticket['fields'].get('summary')}")
        print(f"   📊 Status: {ticket['fields'].get('status', {}).get('name')}")
        print(f"   📋 Type: {ticket['fields'].get('issuetype', {}).get('name')}")
        
        # Get full ticket data to check QA Assignee
        full_ticket_url = f"{jira_server}/rest/api/2/issue/{ticket_key}?expand=names,schema"
        full_response = requests.get(
            full_ticket_url,
            auth=(jira_email, jira_token),
            headers=headers,
            timeout=10
        )
        
        if full_response.status_code == 200:
            full_ticket_data = full_response.json()
            fields = full_ticket_data.get('fields', {})
            names = full_ticket_data.get('names', {})
            
            # Find QA Assignee field
            qa_assignee = None
            qa_field_name = None
            for field_id, field_name in names.items():
                if 'qa' in field_name.lower() and 'assignee' in field_name.lower():
                    qa_assignee = fields.get(field_id)
                    qa_field_name = field_name
                    break
            
            if qa_assignee:
                qa_name = qa_assignee.get('displayName', 'Unknown')
                print(f"   🧪 QA Assignee ({qa_field_name}): {qa_name}")
            else:
                print(f"   🧪 QA Assignee: Not set")
        else:
            print(f"   ⚠️  Could not get full ticket data")
        
        print()
    
    print("=" * 60)
    print("🎉 QA workload analysis complete!")
    return True

if __name__ == "__main__":
    success = get_qa_workload()
    sys.exit(0 if success else 1)
