#!/usr/bin/env python3
"""
QA Workload Reader

This script finds all Jira tickets where the current user is assigned as the QA Assignee.
Very useful for tracking QA workload and managing assignments.
"""

import sys
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Load environment variables
load_dotenv()

class QAWorkloadReader:
    """Finds all tickets assigned to the current user as QA Assignee."""
    
    def __init__(self):
        """Initialize the workload reader with credentials."""
        self.jira_server = os.getenv('JIRA_SERVER')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_server, self.jira_email, self.jira_token]):
            raise ValueError("Missing Jira credentials in environment variables")
        
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_qa_assignee_field_id(self) -> Optional[str]:
        """Get the QA Assignee field ID by checking a known ticket."""
        try:
            # Use AP-20641 which we know has QA Assignee field
            test_url = f"{self.jira_server}/rest/api/2/issue/AP-20641?expand=names,schema"
            response = requests.get(
                test_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                ticket_data = response.json()
                names = ticket_data.get('names', {})
                
                # Find QA Assignee field
                for field_id, field_name in names.items():
                    if 'qa' in field_name.lower() and 'assignee' in field_name.lower():
                        return field_id
                
                print("⚠️  Could not find QA Assignee field ID")
                return None
            else:
                print(f"❌ Failed to get field ID (Status: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"❌ Error getting field ID: {e}")
            return None
    
    def get_current_user_account_id(self) -> Optional[str]:
        """Get the current user's account ID."""
        try:
            user_url = f"{self.jira_server}/rest/api/2/myself"
            response = requests.get(
                user_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('accountId')
            else:
                print(f"❌ Failed to get user info (Status: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"❌ Error getting user info: {e}")
            return None
    
    def find_qa_tickets(self, status_filter: str = None, project_filter: str = None) -> List[Dict[str, Any]]:
        """
        Find all tickets where current user is QA Assignee.
        
        Args:
            status_filter: Optional status filter (e.g., 'To Do', 'In Progress', 'Done')
            project_filter: Optional project filter (e.g., 'AP', 'DEV')
            
        Returns:
            List of ticket information dictionaries
        """
        try:
            print("🔍 Finding tickets where you are QA Assignee...")
            print("=" * 60)
            
            # Get QA Assignee field ID
            qa_field_id = self.get_qa_assignee_field_id()
            if not qa_field_id:
                print("❌ Could not determine QA Assignee field ID")
                return []
            
            # Get current user's account ID
            user_account_id = self.get_current_user_account_id()
            if not user_account_id:
                print("❌ Could not determine your account ID")
                return []
            
            print(f"✅ Found QA Assignee field: {qa_field_id}")
            print(f"✅ Your account ID: {user_account_id}")
            
            # Since custom field search doesn't work via JQL, let's search for recent tickets
            # and then filter for QA Assignee
            print("🔍 Searching for recent tickets in AP project...")
            
            # Build JQL query for recent tickets search
            jql_parts = ["project = AP", "updated >= -30d"]
            
            if status_filter:
                jql_parts.append(f'status = "{status_filter}"')
            
            if project_filter:
                jql_parts.append(f'project = "{project_filter}"')
            
            jql_query = " AND ".join(jql_parts)
            
            print(f"🔍 JQL Query: {jql_query}")
            print()
            
            # Search for tickets where user is assignee
            search_url = f"{self.jira_server}/rest/api/2/search"
            search_data = {
                "jql": jql_query,
                "startAt": 0,
                "maxResults": 100,
                "fields": [
                    "summary", "status", "issuetype", "priority", "assignee", 
                    "reporter", "created", "updated", "labels", "components"
                ]
            }
            
            response = requests.post(
                search_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                json=search_data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Search failed (Status: {response.status_code})")
                print(f"📄 Response: {response.text}")
                return []
            
            search_results = response.json()
            all_tickets = search_results.get('issues', [])
            total_assigned = search_results.get('total', 0)
            
            print(f"✅ Found {total_assigned} recent tickets in AP project")
            print("🔍 Now filtering for QA Assignee...")
            
            # Now filter for tickets where user is QA Assignee
            qa_tickets = []
            for ticket in all_tickets:
                # Get full ticket data to check QA Assignee field
                ticket_key = ticket.get('key')
                full_ticket = self._get_full_ticket(ticket_key, qa_field_id)
                
                if full_ticket and full_ticket.get('qa_assignee_account_id') == user_account_id:
                    qa_tickets.append(full_ticket)
            
            print(f"✅ Found {len(qa_tickets)} tickets where you are QA Assignee")
            print()
            
            if not qa_tickets:
                print("📝 No tickets found where you are QA Assignee")
                return []
            
            # Display tickets
            for i, ticket_info in enumerate(qa_tickets, 1):
                ticket_info['index'] = i
                self._display_ticket_summary(ticket_info)
            
            return qa_tickets
            
        except Exception as e:
            print(f"❌ Error finding QA tickets: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_full_ticket(self, ticket_key: str, qa_field_id: str) -> Optional[Dict[str, Any]]:
        """Get full ticket data including custom fields."""
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
                
                # Get QA Assignee info
                qa_assignee = fields.get(qa_field_id)
                qa_account_id = qa_assignee.get('accountId') if qa_assignee else None
                
                return {
                    'key': ticket_data.get('key'),
                    'summary': fields.get('summary'),
                    'status': fields.get('status', {}).get('name'),
                    'issue_type': fields.get('issuetype', {}).get('name'),
                    'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
                    'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
                    'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
                    'created': fields.get('created'),
                    'updated': fields.get('updated'),
                    'labels': fields.get('labels', []),
                    'components': [c['name'] for c in fields.get('components', [])],
                    'qa_assignee_account_id': qa_account_id
                }
            else:
                print(f"⚠️  Failed to get full ticket {ticket_key} (Status: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"⚠️  Error getting full ticket {ticket_key}: {e}")
            return None
    
    def _process_ticket(self, ticket: Dict, index: int, qa_field_id: str) -> Dict[str, Any]:
        """Process a single ticket and extract relevant information."""
        fields = ticket.get('fields', {})
        
        # Get QA Assignee info
        qa_assignee = fields.get(qa_field_id)
        qa_name = qa_assignee.get('displayName') if qa_assignee else "Unknown"
        
        return {
            'index': index,
            'key': ticket.get('key'),
            'summary': fields.get('summary'),
            'status': fields.get('status', {}).get('name'),
            'issue_type': fields.get('issuetype', {}).get('name'),
            'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
            'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
            'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
            'created': fields.get('created'),
            'updated': fields.get('updated'),
            'labels': fields.get('labels', []),
            'components': [c['name'] for c in fields.get('components', [])],
            'qa_assignee': qa_name
        }
    
    def _display_ticket_summary(self, ticket_info: Dict[str, Any]):
        """Display a summary of a single ticket."""
        print(f"{ticket_info['index']:2d}. 🎫 {ticket_info['key']}")
        print(f"    📝 {ticket_info['summary']}")
        print(f"    📊 Status: {ticket_info['status']}")
        print(f"    📋 Type: {ticket_info['issue_type']}")
        if ticket_info['priority']:
            print(f"    ⚡ Priority: {ticket_info['priority']}")
        print(f"    👤 Assignee: {ticket_info['assignee']}")
        print(f"    🔄 Updated: {ticket_info['updated'][:10]}")  # Just the date
        if ticket_info['labels']:
            print(f"    🏷️  Labels: {ticket_info['labels']}")
        print()
    
    def get_workload_summary(self, tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of the QA workload."""
        if not tickets:
            return {}
        
        summary = {
            'total_tickets': len(tickets),
            'by_status': {},
            'by_type': {},
            'by_priority': {},
            'recent_updates': []
        }
        
        for ticket in tickets:
            # Count by status
            status = ticket['status']
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1
            
            # Count by type
            issue_type = ticket['issue_type']
            summary['by_type'][issue_type] = summary['by_type'].get(issue_type, 0) + 1
            
            # Count by priority
            priority = ticket['priority'] or 'None'
            summary['by_priority'][priority] = summary['by_priority'].get(priority, 0) + 1
            
            # Track recent updates (last 7 days)
            updated_date = ticket['updated'][:10]  # YYYY-MM-DD
            summary['recent_updates'].append({
                'key': ticket['key'],
                'summary': ticket['summary'],
                'updated': updated_date
            })
        
        return summary
    
    def display_workload_summary(self, summary: Dict[str, Any]):
        """Display the workload summary."""
        if not summary:
            return
        
        print("📊 QA Workload Summary")
        print("=" * 40)
        print(f"📈 Total Tickets: {summary['total_tickets']}")
        print()
        
        print("📊 By Status:")
        for status, count in sorted(summary['by_status'].items()):
            print(f"   • {status}: {count}")
        print()
        
        print("📋 By Issue Type:")
        for issue_type, count in sorted(summary['by_type'].items()):
            print(f"   • {issue_type}: {count}")
        print()
        
        print("⚡ By Priority:")
        for priority, count in sorted(summary['by_priority'].items()):
            print(f"   • {priority}: {count}")
        print()
        
        print("🔄 Recently Updated (Last 7 days):")
        recent_tickets = [t for t in summary['recent_updates'] if t['updated'] >= '2025-01-18']  # Adjust date as needed
        if recent_tickets:
            for ticket in recent_tickets[:5]:  # Show top 5
                print(f"   • {ticket['key']}: {ticket['summary'][:50]}...")
        else:
            print("   • No recent updates")
        print()

def main():
    """Main function to run the QA workload reader."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Find tickets where you are QA Assignee')
    parser.add_argument('--status', help='Filter by status (e.g., "To Do", "In Progress")')
    parser.add_argument('--project', help='Filter by project (e.g., "AP", "DEV")')
    parser.add_argument('--summary-only', action='store_true', help='Show only summary, not individual tickets')
    
    args = parser.parse_args()
    
    try:
        reader = QAWorkloadReader()
        tickets = reader.find_qa_tickets(
            status_filter=args.status,
            project_filter=args.project
        )
        
        # Filter out Done tickets (only show active tickets)
        active_tickets = [ticket for ticket in tickets if ticket.get('status') != 'Done']
        
        if active_tickets:
            summary = reader.get_workload_summary(active_tickets)
            reader.display_workload_summary(summary)
            
            # Show count of Done tickets if any
            done_tickets = [ticket for ticket in tickets if ticket.get('status') == 'Done']
            if done_tickets:
                print(f"📋 Note: {len(done_tickets)} completed tickets (Done status) excluded from active workload")
        else:
            print("✅ No active QA assignments found!")
            return True
            
            if not args.summary_only:
                print("=" * 60)
                print("🎉 QA workload analysis complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
