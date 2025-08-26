#!/usr/bin/env python3
"""
My Assignments - Complete Workload Overview

This script shows ALL tickets where the current user is assigned,
including both regular assignee and QA assignee roles.
"""

import sys
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

class MyAssignments:
    """Shows all assignments for the current user."""
    
    def __init__(self):
        """Initialize the assignments reader."""
        self.jira_server = os.getenv('JIRA_SERVER')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_server, self.jira_email, self.jira_token]):
            raise ValueError("Missing Jira credentials in environment variables")
        
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_qa_assignee_field_id(self) -> str:
        """Get the QA Assignee field ID."""
        # We know this from our previous testing
        return "customfield_11207"
    
    def get_all_assignments(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all assignments for the current user."""
        print("🔍 Finding ALL your assignments...")
        print("=" * 60)
        
        # Get regular assignee tickets
        print("1️⃣ Finding tickets where you are regular assignee...")
        regular_assignments = self._get_regular_assignments()
        
        # Get QA assignee tickets
        print("2️⃣ Finding tickets where you are QA assignee...")
        qa_assignments = self._get_qa_assignments()
        
        return {
            'regular_assignee': regular_assignments,
            'qa_assignee': qa_assignments
        }
    
    def _get_regular_assignments(self) -> List[Dict[str, Any]]:
        """Get tickets where user is regular assignee."""
        search_url = f"{self.jira_server}/rest/api/2/search"
        search_data = {
            "jql": "assignee = currentUser() ORDER BY updated DESC",
            "startAt": 0,
            "maxResults": 100,
            "fields": ["summary", "status", "issuetype", "priority", "assignee", "reporter", "updated", "labels"]
        }
        
        response = requests.post(
            search_url,
            auth=(self.jira_email, self.jira_token),
            headers=self.headers,
            json=search_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Regular assignments search failed (Status: {response.status_code})")
            return []
        
        search_results = response.json()
        tickets = search_results.get('issues', [])
        total = search_results.get('total', 0)
        
        print(f"✅ Found {total} tickets where you are regular assignee")
        
        processed_tickets = []
        for ticket in tickets:
            fields = ticket.get('fields', {})
            processed_tickets.append({
                'key': ticket.get('key'),
                'summary': fields.get('summary'),
                'status': fields.get('status', {}).get('name'),
                'issue_type': fields.get('issuetype', {}).get('name'),
                'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
                'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
                'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
                'updated': fields.get('updated'),
                'labels': fields.get('labels', []),
                'assignment_type': 'Regular Assignee'
            })
        
        return processed_tickets
    
    def _get_qa_assignments(self) -> List[Dict[str, Any]]:
        """Get tickets where user is QA assignee."""
        qa_field_id = self.get_qa_assignee_field_id()
        
        # Search for recent tickets and filter for QA assignee
        search_url = f"{self.jira_server}/rest/api/2/search"
        search_data = {
            "jql": "project = AP AND updated >= -60d ORDER BY updated DESC",
            "startAt": 0,
            "maxResults": 200,
            "fields": ["summary", "status", "issuetype", "priority", "assignee", "reporter", "updated", "labels"]
        }
        
        response = requests.post(
            search_url,
            auth=(self.jira_email, self.jira_token),
            headers=self.headers,
            json=search_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ QA assignments search failed (Status: {response.status_code})")
            return []
        
        search_results = response.json()
        all_tickets = search_results.get('issues', [])
        
        print(f"✅ Checking {len(all_tickets)} recent tickets for QA assignments...")
        
        qa_tickets = []
        for ticket in all_tickets:
            ticket_key = ticket.get('key')
            
            # Get full ticket data to check QA assignee
            full_ticket = self._get_full_ticket(ticket_key, qa_field_id)
            
            if full_ticket and full_ticket.get('qa_assignee_account_id'):
                qa_tickets.append(full_ticket)
        
        print(f"✅ Found {len(qa_tickets)} tickets where you are QA assignee")
        return qa_tickets
    
    def _get_full_ticket(self, ticket_key: str, qa_field_id: str) -> Dict[str, Any]:
        """Get full ticket data including QA assignee."""
        try:
            ticket_url = f"{self.jira_server}/rest/api/2/issue/{ticket_key}?expand=names,schema"
            response = requests.get(
                ticket_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                ticket_data = response.json()
                fields = ticket_data.get('fields', {})
                
                # Get QA assignee info
                qa_assignee = fields.get(qa_field_id)
                qa_account_id = qa_assignee.get('accountId') if qa_assignee else None
                qa_name = qa_assignee.get('displayName') if qa_assignee else None
                
                # Check if current user is QA assignee
                if qa_account_id:
                    return {
                        'key': ticket_data.get('key'),
                        'summary': fields.get('summary'),
                        'status': fields.get('status', {}).get('name'),
                        'issue_type': fields.get('issuetype', {}).get('name'),
                        'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
                        'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
                        'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
                        'updated': fields.get('updated'),
                        'labels': fields.get('labels', []),
                        'qa_assignee_account_id': qa_account_id,
                        'qa_assignee_name': qa_name,
                        'assignment_type': 'QA Assignee'
                    }
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error getting full ticket {ticket_key}: {e}")
            return None
    
    def display_assignments(self, assignments: Dict[str, List[Dict[str, Any]]]):
        """Display all assignments in a comprehensive format."""
        regular = assignments['regular_assignee']
        qa = assignments['qa_assignee']
        
        total_assignments = len(regular) + len(qa)
        
        print(f"\n📊 COMPLETE ASSIGNMENT OVERVIEW")
        print("=" * 60)
        print(f"📈 Total Assignments: {total_assignments}")
        print(f"   • Regular Assignee: {len(regular)}")
        print(f"   • QA Assignee: {len(qa)}")
        print()
        
        # Show regular assignments
        if regular:
            print("👤 REGULAR ASSIGNEE TICKETS:")
            print("-" * 40)
            for i, ticket in enumerate(regular, 1):
                print(f"{i:2d}. 🎫 {ticket['key']}")
                print(f"    📝 {ticket['summary']}")
                print(f"    📊 Status: {ticket['status']}")
                print(f"    📋 Type: {ticket['issue_type']}")
                if ticket['priority']:
                    print(f"    ⚡ Priority: {ticket['priority']}")
                print(f"    🔄 Updated: {ticket['updated'][:10]}")
                if ticket['labels']:
                    print(f"    🏷️  Labels: {ticket['labels']}")
                print()
        
        # Show QA assignments
        if qa:
            print("🧪 QA ASSIGNEE TICKETS:")
            print("-" * 40)
            for i, ticket in enumerate(qa, 1):
                print(f"{i:2d}. 🎫 {ticket['key']}")
                print(f"    📝 {ticket['summary']}")
                print(f"    📊 Status: {ticket['status']}")
                print(f"    📋 Type: {ticket['issue_type']}")
                if ticket['priority']:
                    print(f"    ⚡ Priority: {ticket['priority']}")
                print(f"    👤 Assignee: {ticket['assignee']}")
                print(f"    🧪 QA Assignee: {ticket['qa_assignee_name']}")
                print(f"    🔄 Updated: {ticket['updated'][:10]}")
                if ticket['labels']:
                    print(f"    🏷️  Labels: {ticket['labels']}")
                print()
        
        # Summary by status
        print("📊 SUMMARY BY STATUS:")
        print("-" * 40)
        all_tickets = regular + qa
        status_counts = {}
        type_counts = {}
        priority_counts = {}
        
        for ticket in all_tickets:
            status = ticket['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
            issue_type = ticket['issue_type']
            type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
            
            priority = ticket.get('priority', 'None')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        print("📊 By Status:")
        for status, count in sorted(status_counts.items()):
            print(f"   • {status}: {count}")
        
        print("\n📋 By Issue Type:")
        for issue_type, count in sorted(type_counts.items()):
            print(f"   • {issue_type}: {count}")
        
        print("\n⚡ By Priority:")
        for priority, count in sorted(priority_counts.items(), key=lambda x: (x[0] is None, x[0])):
            priority_name = priority if priority else "None"
            print(f"   • {priority_name}: {count}")
        
        print("\n" + "=" * 60)
        print("🎉 Complete assignment overview complete!")

def main():
    """Main function."""
    try:
        reader = MyAssignments()
        assignments = reader.get_all_assignments()
        
        # Filter out Done tickets (only show active assignments)
        active_regular = [ticket for ticket in assignments['regular_assignee'] if ticket.get('status') != 'Done']
        active_qa = [ticket for ticket in assignments['qa_assignee'] if ticket.get('status') != 'Done']
        
        active_assignments = {
            'regular_assignee': active_regular,
            'qa_assignee': active_qa
        }
        
        if active_regular or active_qa:
            reader.display_assignments(active_assignments)
            
            # Show count of Done tickets if any
            done_regular = [ticket for ticket in assignments['regular_assignee'] if ticket.get('status') == 'Done']
            done_qa = [ticket for ticket in assignments['qa_assignee'] if ticket.get('status') == 'Done']
            
            if done_regular or done_qa:
                print(f"📋 Note: {len(done_regular)} regular + {len(done_qa)} QA completed tickets (Done status) excluded from active workload")
        else:
            print("✅ No active assignments found!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
