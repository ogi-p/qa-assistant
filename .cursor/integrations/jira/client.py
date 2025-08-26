"""
Jira Client Implementation

This module provides a robust Jira API client wrapper with:
- Connection management with retry logic
- Authentication handling
- Rate limiting compliance
- Error handling and logging
- Configuration management
"""

import os
import yaml
import logging
import time
from typing import Optional, Dict, Any, List
from jira import JIRA
from jira.exceptions import JIRAError
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class JiraClient:
    """
    Jira API client wrapper with enhanced error handling and rate limiting.
    """
    
    def __init__(self, config_path: str = ".cursor/config/jira_config.yaml"):
        """
        Initialize the Jira client with configuration.
        
        Args:
            config_path: Path to the Jira configuration file
        """
        self.config = self._load_config(config_path)
        self.client = None
        self.logger = self._setup_logging()
        self.rate_limit_tracker = {
            'requests': 0,
            'last_reset': time.time(),
            'limit': int(self.config.get('rate_limiting', {}).get('requests_per_minute', 60))
        }
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file and environment variables.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Override with environment variables
            config['jira_server']['url'] = os.getenv('JIRA_SERVER', config['jira_server']['url'])
            config['auth']['email'] = os.getenv('JIRA_EMAIL', config['auth']['email'])
            config['auth']['api_token'] = os.getenv('JIRA_API_TOKEN', config['auth']['api_token'])
            
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def _setup_logging(self) -> logging.Logger:
        """
        Set up logging configuration.
        
        Returns:
            Configured logger
        """
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        logger = logging.getLogger('jira_client')
        logger.setLevel(log_level)
        
        # Create handlers
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            
            # File handler
            log_file = log_config.get('file', 'logs/jira_integration.log')
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
        
        return logger
    
    def _check_rate_limit(self) -> None:
        """
        Check and enforce rate limiting.
        """
        current_time = time.time()
        time_window = 60  # 1 minute window
        
        # Reset counter if time window has passed
        if current_time - self.rate_limit_tracker['last_reset'] >= time_window:
            self.rate_limit_tracker['requests'] = 0
            self.rate_limit_tracker['last_reset'] = current_time
        
        # Check if we're at the limit
        if self.rate_limit_tracker['requests'] >= self.rate_limit_tracker['limit']:
            sleep_time = time_window - (current_time - self.rate_limit_tracker['last_reset'])
            if sleep_time > 0:
                self.logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                self.rate_limit_tracker['requests'] = 0
                self.rate_limit_tracker['last_reset'] = time.time()
        
        self.rate_limit_tracker['requests'] += 1
    
    def _handle_jira_error(self, error: JIRAError, operation: str) -> None:
        """
        Handle Jira API errors with appropriate logging and retry logic.
        
        Args:
            error: JIRAError exception
            operation: Description of the operation that failed
        """
        error_config = self.config.get('error_handling', {})
        
        if error.status_code == 401:
            self.logger.error(f"Authentication failed for {operation}: {error.text}")
            raise AuthenticationError(f"Invalid credentials for {operation}")
        elif error.status_code == 403:
            self.logger.error(f"Permission denied for {operation}: {error.text}")
            raise PermissionError(f"Insufficient permissions for {operation}")
        elif error.status_code == 404:
            self.logger.error(f"Resource not found for {operation}: {error.text}")
            raise ResourceNotFoundError(f"Resource not found for {operation}")
        elif error.status_code == 429:
            self.logger.warning(f"Rate limit exceeded for {operation}. Retrying...")
            time.sleep(error_config.get('retry_delay', 2))
            return  # Allow retry
        else:
            self.logger.error(f"Jira API error for {operation}: {error.status_code} - {error.text}")
            raise JiraAPIError(f"API error {error.status_code} for {operation}: {error.text}")
    
    def connect(self) -> bool:
        """
        Establish connection to Jira with authentication.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.logger.info("Attempting to connect to Jira...")
            
            server_config = self.config['jira_server']
            auth_config = self.config['auth']
            
            # Create Jira client
            self.client = JIRA(
                server=server_config['url'],
                basic_auth=(auth_config['email'], auth_config['api_token']),
                timeout=server_config['timeout'],
                validate=server_config.get('validate_ssl', True)
            )
            
            # Test connection by getting server info
            server_info = self.client.server_info()
            self.logger.info(f"Successfully connected to Jira server: {server_info['serverTitle']}")
            
            return True
            
        except JIRAError as e:
            self._handle_jira_error(e, "connection")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during connection: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test the Jira connection and authentication.
        
        Returns:
            True if connection and authentication successful
        """
        try:
            if not self.client:
                return self.connect()
            
            # Test by getting current user
            current_user = self.client.current_user()
            self.logger.info(f"Connection test successful. Current user: {current_user['displayName']}")
            return True
            
        except JIRAError as e:
            self._handle_jira_error(e, "connection test")
            return False
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def read_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a Jira ticket by ID.
        
        Args:
            ticket_id: Jira ticket ID (e.g., 'AP-20575')
            
        Returns:
            Ticket data dictionary or None if not found
        """
        try:
            self._check_rate_limit()
            
            if not self.client:
                if not self.connect():
                    return None
            
            self.logger.info(f"Reading ticket: {ticket_id}")
            issue = self.client.issue(ticket_id)
            
            # Extract relevant ticket data
            ticket_data = {
                'id': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description,
                'status': issue.fields.status.name,
                'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
                'reporter': issue.fields.reporter.displayName if issue.fields.reporter else None,
                'created': issue.fields.created,
                'updated': issue.fields.updated,
                'priority': issue.fields.priority.name if issue.fields.priority else None,
                'labels': issue.fields.labels,
                'components': [c.name for c in issue.fields.components],
                'issue_type': issue.fields.issuetype.name,
                'project': issue.fields.project.key
            }
            
            self.logger.info(f"Successfully read ticket {ticket_id}")
            return ticket_data
            
        except JIRAError as e:
            self._handle_jira_error(e, f"reading ticket {ticket_id}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error reading ticket {ticket_id}: {e}")
            return None
    
    def get_comments(self, ticket_id: str) -> List[Dict[str, Any]]:
        """
        Get all comments for a Jira ticket.
        
        Args:
            ticket_id: Jira ticket ID
            
        Returns:
            List of comment dictionaries
        """
        try:
            self._check_rate_limit()
            
            if not self.client:
                if not self.connect():
                    return []
            
            self.logger.info(f"Getting comments for ticket: {ticket_id}")
            issue = self.client.issue(ticket_id)
            comments = issue.fields.comment.comments
            
            comment_data = []
            for comment in comments:
                comment_data.append({
                    'id': comment.id,
                    'author': comment.author.displayName,
                    'body': comment.body,
                    'created': comment.created,
                    'updated': comment.updated
                })
            
            self.logger.info(f"Retrieved {len(comment_data)} comments for ticket {ticket_id}")
            return comment_data
            
        except JIRAError as e:
            self._handle_jira_error(e, f"getting comments for ticket {ticket_id}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error getting comments for ticket {ticket_id}: {e}")
            return []
    
    def get_project_info(self, project_key: str) -> Optional[Dict[str, Any]]:
        """
        Get project information.
        
        Args:
            project_key: Project key (e.g., 'AP')
            
        Returns:
            Project data dictionary or None if not found
        """
        try:
            self._check_rate_limit()
            
            if not self.client:
                if not self.connect():
                    return None
            
            self.logger.info(f"Getting project info for: {project_key}")
            project = self.client.project(project_key)
            
            project_data = {
                'key': project.key,
                'name': project.name,
                'description': project.description,
                'lead': project.lead.displayName if project.lead else None,
                'url': project.url,
                'avatar_url': project.avatarUrls['48x48'] if project.avatarUrls else None
            }
            
            self.logger.info(f"Successfully retrieved project info for {project_key}")
            return project_data
            
        except JIRAError as e:
            self._handle_jira_error(e, f"getting project info for {project_key}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error getting project info for {project_key}: {e}")
            return None
    
    def disconnect(self) -> None:
        """
        Disconnect from Jira and clean up resources.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.logger.info("Disconnected from Jira")


class AuthenticationError(Exception):
    """Raised when Jira authentication fails."""
    pass


class PermissionError(Exception):
    """Raised when user lacks required permissions."""
    pass


class ResourceNotFoundError(Exception):
    """Raised when a requested resource is not found."""
    pass


class JiraAPIError(Exception):
    """Raised when Jira API returns an error."""
    pass
