#!/usr/bin/env python3
"""
Find QA Assignments

This script searches for tickets where the current user is assigned as QA Assignee
using different search strategies.
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def find_qa_assignments():
    """Find tickets where current user is QA Assignee using different strategies."""
    
    jira_server = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Finding tickets where you are QA Assignee...")
    print("=" * 60)
    
    # Strategy 1: Search for recent tickets in AP project
    print("1️⃣ Searching for recent tickets in AP project...")
    search_url = f"{jira_server}/rest/api/2/search"
    search_data = {
        "jql": "project = AP AND updated >= -30d ORDER BY updated DESC",
        "startAt": 0,
        "maxResults": 20,
        "fields": ["summary", "status", "issuetype", "assignee", "reporter"]
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
        return False
    
    search_results = response.json()
    tickets = search_results.get('issues', [])
    
    print(f"✅ Found {len(tickets)} recent tickets in AP project")
    print()
    
    # Check each ticket for QA Assignee
    qa_tickets = []
    for ticket in tickets:
        ticket_key = ticket.get('key')
        
        # Get full ticket data
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
                qa_email = qa_assignee.get('emailAddress', 'Unknown')
                
                # Check if this is the current user
                if qa_email == jira_email:
                    qa_tickets.append({
                        'key': ticket_key,
                        'summary': ticket['fields'].get('summary'),
                        'status': ticket['fields'].get('status', {}).get('name'),
                        'type': ticket['fields'].get('issuetype', {}).get('name'),
                        'assignee': ticket['fields'].get('assignee', {}).get('displayName'),
                        'qa_field_name': qa_field_name,
                        'qa_name': qa_name
                    })
    
    if qa_tickets:
        print(f"✅ Found {len(qa_tickets)} tickets where you are QA Assignee:")
        print()
        for i, ticket in enumerate(qa_tickets, 1):
            print(f"{i}. 🎫 {ticket['key']}")
            print(f"   📝 {ticket['summary']}")
            print(f"   📊 Status: {ticket['status']}")
            print(f"   📋 Type: {ticket['type']}")
            print(f"   👤 Assignee: {ticket['assignee']}")
            print(f"   🧪 QA Assignee ({ticket['qa_field_name']}): {ticket['qa_name']}")
            print()
    else:
        print("📝 No tickets found where you are QA Assignee in recent AP tickets")
        print()
        
        # Strategy 2: Check if there are any tickets with QA Assignee set at all
        print("2️⃣ Checking if any tickets have QA Assignee set...")
        qa_tickets_with_anyone = []
        
        for ticket in tickets[:10]:  # Check first 10 tickets
            ticket_key = ticket.get('key')
            
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
                    qa_tickets_with_anyone.append({
                        'key': ticket_key,
                        'summary': ticket['fields'].get('summary'),
                        'qa_field_name': qa_field_name,
                        'qa_name': qa_name
                    })
        
        if qa_tickets_with_anyone:
            print(f"✅ Found {len(qa_tickets_with_anyone)} tickets with QA Assignee set:")
            for ticket in qa_tickets_with_anyone:
                print(f"   • {ticket['key']}: {ticket['qa_name']} ({ticket['qa_field_name']})")
        else:
            print("📝 No tickets found with QA Assignee field set")
    
    print("=" * 60)
    print("🎉 QA assignment search complete!")
    return True

if __name__ == "__main__":
    success = find_qa_assignments()
    sys.exit(0 if success else 1)
