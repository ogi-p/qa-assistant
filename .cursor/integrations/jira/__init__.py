"""
Jira Integration Package

This package provides integration with Jira for:
- Reading ticket details and comments
- Adding comments to tickets
- Changing ticket status
- Managing test execution updates
- Handling bug reports and traceability

Modules:
- client: Jira API client wrapper
- reader: Ticket reading functionality
- writer: Comment writing functionality
- status: Status change functionality
"""

from .client import JiraClient
from .reader import JiraReader
from .writer import JiraWriter
from .status import JiraStatus

__version__ = "1.0.0"
__author__ = "Ognjen"

__all__ = [
    "JiraClient",
    "JiraReader", 
    "JiraWriter",
    "JiraStatus"
]
