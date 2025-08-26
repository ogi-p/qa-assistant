#!/usr/bin/env python3
"""
Interactive Jira Ticket Reader

This script provides an interactive interface to read Jira tickets
without needing command line arguments.
"""

import sys
import os
from jira_ticket_reader import JiraTicketReader

def safe_input(prompt):
    """Safe input function that handles various input errors."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return None
    except Exception:
        return None

def interactive_reader():
    """Interactive Jira ticket reader."""
    
    print("🔍 Interactive Jira Ticket Reader")
    print("=" * 50)
    print("This tool can read any Jira ticket and extract all available information.")
    print("Type 'quit' or 'exit' to stop the program.")
    print("=" * 50)
    
    try:
        reader = JiraTicketReader()
        print("✅ Jira connection established successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize Jira reader: {e}")
        return False
    
    while True:
        # Get ticket ID from user
        ticket_id = safe_input("\n🎫 Enter ticket ID (e.g., AP-20641): ")
        
        if ticket_id is None:
            print("\n👋 Goodbye!")
            break
            
        ticket_id = ticket_id.upper()
        
        # Check for exit commands
        if ticket_id.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        # Validate input
        if not ticket_id:
            print("⚠️  Please enter a valid ticket ID.")
            continue
        
        # Read the ticket
        print(f"\n🔍 Reading ticket {ticket_id}...")
        try:
            ticket_info = reader.read_ticket(ticket_id)
            
            if ticket_info:
                print(f"\n✅ Successfully read ticket {ticket_id}")
                
                # Show all information by default
                reader._display_ticket_info(ticket_info)
                
                # Ask if user wants to read another ticket
                choice = safe_input("\n📋 Read another ticket? (y/n): ")
                if choice is None or choice.lower() in ['n', 'no', 'quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                    
            else:
                print(f"❌ Failed to read ticket {ticket_id}")
                
        except Exception as e:
            print(f"❌ Error reading ticket: {e}")
            continue
    
    return True

def main():
    """Main function."""
    try:
        success = interactive_reader()
        return success
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
