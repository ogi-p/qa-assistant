#!/usr/bin/env python3
"""
Comprehensive Jira Ticket Reader

This script can read any Jira ticket and extract all available information
including basic details, custom fields, QA Assignee, comments, and more.
"""

import sys
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Load environment variables
load_dotenv()

class JiraTicketReader:
    """Comprehensive Jira ticket reader with all field extraction capabilities."""
    
    def __init__(self):
        """Initialize the ticket reader with credentials."""
        self.jira_server = os.getenv('JIRA_SERVER')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_server, self.jira_email, self.jira_token]):
            raise ValueError("Missing Jira credentials in environment variables")
        
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def read_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a Jira ticket and extract all available information.
        
        Args:
            ticket_id: Jira ticket ID (e.g., 'AP-20641')
            
        Returns:
            Dictionary containing all ticket information or None if failed
        """
        try:
            print(f"🔍 Reading Ticket {ticket_id}...")
            print("=" * 60)
            
            # Get ticket with expanded field data
            ticket_url = f"{self.jira_server}/rest/api/2/issue/{ticket_id}?expand=names,schema"
            response = requests.get(
                ticket_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to read ticket (Status: {response.status_code})")
                print(f"📄 Response: {response.text}")
                return None
            
            ticket_data = response.json()
            fields = ticket_data.get('fields', {})
            names = ticket_data.get('names', {})
            
            print(f"✅ Successfully read ticket {ticket_id}!")
            
            # Extract all information
            ticket_info = {
                'basic_info': self._extract_basic_info(ticket_data, fields),
                'people_info': self._extract_people_info(fields),
                'qa_info': self._extract_qa_info(fields, names),
                'custom_fields': self._extract_custom_fields(fields, names),
                'comments': self._get_comments(ticket_id),
                'timeline': self._extract_timeline(fields),
                'metadata': self._extract_metadata(fields)
            }
            
            # Display the information
            self._display_ticket_info(ticket_info)
            
            return ticket_info
            
        except Exception as e:
            print(f"❌ Error reading ticket {ticket_id}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_basic_info(self, ticket_data: Dict, fields: Dict) -> Dict[str, Any]:
        """Extract basic ticket information."""
        return {
            'key': ticket_data.get('key'),
            'summary': fields.get('summary'),
            'description': fields.get('description'),
            'status': fields.get('status', {}).get('name'),
            'issue_type': fields.get('issuetype', {}).get('name'),
            'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
            'labels': fields.get('labels', []),
            'components': [c['name'] for c in fields.get('components', [])],
            'project': fields.get('project', {}).get('key')
        }
    
    def _extract_people_info(self, fields: Dict) -> Dict[str, Any]:
        """Extract people-related information."""
        assignee = fields.get('assignee')
        reporter = fields.get('reporter')
        
        return {
            'assignee': {
                'name': assignee.get('displayName') if assignee else None,
                'email': assignee.get('emailAddress') if assignee else None,
                'account_id': assignee.get('accountId') if assignee else None
            },
            'reporter': {
                'name': reporter.get('displayName') if reporter else None,
                'email': reporter.get('emailAddress') if reporter else None,
                'account_id': reporter.get('accountId') if reporter else None
            }
        }
    
    def _extract_qa_info(self, fields: Dict, names: Dict) -> Dict[str, Any]:
        """Extract QA-related information."""
        qa_info = {}
        
        # Look for QA Assignee field
        for field_id, field_name in names.items():
            if 'qa' in field_name.lower() and 'assignee' in field_name.lower():
                field_value = fields.get(field_id)
                if field_value and isinstance(field_value, dict) and 'displayName' in field_value:
                    qa_info['qa_assignee'] = {
                        'name': field_value.get('displayName'),
                        'email': field_value.get('emailAddress'),
                        'account_id': field_value.get('accountId'),
                        'field_id': field_id,
                        'field_name': field_name
                    }
                break
        
        return qa_info
    
    def _extract_custom_fields(self, fields: Dict, names: Dict) -> Dict[str, Any]:
        """Extract all custom fields with their names."""
        custom_fields = {}
        
        for field_id, field_value in fields.items():
            if field_id.startswith('customfield_'):
                field_name = names.get(field_id, field_id)
                custom_fields[field_id] = {
                    'name': field_name,
                    'value': field_value
                }
        
        return custom_fields
    
    def _get_comments(self, ticket_id: str) -> List[Dict[str, Any]]:
        """Get all comments for the ticket."""
        try:
            comments_url = f"{self.jira_server}/rest/api/2/issue/{ticket_id}/comment"
            response = requests.get(
                comments_url,
                auth=(self.jira_email, self.jira_token),
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                comments_data = response.json()
                comments = []
                
                for comment in comments_data.get('comments', []):
                    comments.append({
                        'id': comment.get('id'),
                        'author': comment.get('author', {}).get('displayName'),
                        'body': comment.get('body'),
                        'created': comment.get('created'),
                        'updated': comment.get('updated')
                    })
                
                return comments
            else:
                print(f"⚠️  Failed to get comments (Status: {response.status_code})")
                return []
                
        except Exception as e:
            print(f"⚠️  Error getting comments: {e}")
            return []
    
    def _extract_timeline(self, fields: Dict) -> Dict[str, Any]:
        """Extract timeline information."""
        return {
            'created': fields.get('created'),
            'updated': fields.get('updated'),
            'resolution_date': fields.get('resolutiondate'),
            'due_date': fields.get('duedate')
        }
    
    def _extract_metadata(self, fields: Dict) -> Dict[str, Any]:
        """Extract additional metadata."""
        return {
            'votes': fields.get('votes', {}).get('votes', 0) if fields.get('votes') else 0,
            'watches': fields.get('watches', {}).get('watchCount', 0) if fields.get('watches') else 0,
            'progress': fields.get('progress', {}).get('percent', 0) if fields.get('progress') else 0,
            'time_estimate': fields.get('timeestimate'),
            'time_spent': fields.get('timespent'),
            'work_ratio': fields.get('workratio')
        }
    
    def _display_ticket_info(self, ticket_info: Dict[str, Any]):
        """Display all ticket information in a formatted way."""
        
        # Basic Information
        basic = ticket_info['basic_info']
        print(f"\n📋 Basic Information:")
        print(f"   🆔 Key: {basic['key']}")
        print(f"   📝 Summary: {basic['summary']}")
        print(f"   📊 Status: {basic['status']}")
        print(f"   📋 Issue Type: {basic['issue_type']}")
        print(f"   ⚡ Priority: {basic['priority']}")
        print(f"   🏷️  Labels: {basic['labels']}")
        print(f"   🔧 Components: {basic['components']}")
        print(f"   📁 Project: {basic['project']}")
        
        # People Information
        people = ticket_info['people_info']
        print(f"\n👥 People:")
        print(f"   👤 Assignee: {people['assignee']['name']}")
        print(f"   📧 Reporter: {people['reporter']['name']}")
        
        # QA Information
        qa = ticket_info['qa_info']
        if qa.get('qa_assignee'):
            qa_assignee = qa['qa_assignee']
            print(f"\n🔍 QA Information:")
            print(f"   🧪 QA Assignee: {qa_assignee['name']}")
            print(f"   📧 QA Email: {qa_assignee['email']}")
            print(f"   🆔 Field ID: {qa_assignee['field_id']}")
        else:
            print(f"\n🔍 QA Information:")
            print(f"   ❌ No QA Assignee found")
        
        # Timeline
        timeline = ticket_info['timeline']
        print(f"\n📅 Timeline:")
        print(f"   📅 Created: {timeline['created']}")
        print(f"   🔄 Updated: {timeline['updated']}")
        if timeline['due_date']:
            print(f"   ⏰ Due Date: {timeline['due_date']}")
        if timeline['resolution_date']:
            print(f"   ✅ Resolved: {timeline['resolution_date']}")
        
        # Comments
        comments = ticket_info['comments']
        print(f"\n💬 Comments ({len(comments)} total):")
        if comments:
            for i, comment in enumerate(comments[-3:], 1):  # Show last 3 comments
                print(f"   {i}. {comment['author']} ({comment['created']}):")
                print(f"      {comment['body'][:100]}{'...' if len(comment['body']) > 100 else ''}")
                print()
        else:
            print(f"   📝 No comments")
        
        # Custom Fields (show only non-empty ones)
        custom_fields = ticket_info['custom_fields']
        non_empty_custom_fields = {k: v for k, v in custom_fields.items() if v['value'] is not None}
        
        if non_empty_custom_fields:
            print(f"\n🔧 Custom Fields ({len(non_empty_custom_fields)} non-empty):")
            for field_id, field_data in non_empty_custom_fields.items():
                value = field_data['value']
                if isinstance(value, dict) and 'displayName' in value:
                    print(f"   • {field_data['name']}: {value['displayName']}")
                elif isinstance(value, list) and value:
                    print(f"   • {field_data['name']}: {value}")
                elif value:
                    print(f"   • {field_data['name']}: {value}")
        
        # Metadata
        metadata = ticket_info['metadata']
        print(f"\n📊 Metadata:")
        print(f"   👍 Votes: {metadata['votes']}")
        print(f"   👀 Watches: {metadata['watches']}")
        print(f"   📈 Progress: {metadata['progress']}%")
        if metadata['time_estimate']:
            print(f"   ⏱️  Time Estimate: {metadata['time_estimate']} seconds")
        if metadata['time_spent']:
            print(f"   ⏱️  Time Spent: {metadata['time_spent']} seconds")
        
        print("\n" + "=" * 60)
        print("🎉 Ticket reading complete!")

def main():
    """Main function to run the ticket reader."""
    if len(sys.argv) != 2:
        print("Usage: python3 jira_ticket_reader.py <TICKET_ID>")
        print("Example: python3 jira_ticket_reader.py AP-20641")
        sys.exit(1)
    
    ticket_id = sys.argv[1].upper()
    
    try:
        reader = JiraTicketReader()
        ticket_info = reader.read_ticket(ticket_id)
        
        if ticket_info:
            print(f"\n✅ Successfully read ticket {ticket_id}")
            return True
        else:
            print(f"\n❌ Failed to read ticket {ticket_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
