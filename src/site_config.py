"""
Site-specific configuration for handling different authentication methods
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum

class AuthType(Enum):
    """Types of authentication methods"""
    NONE = "none"
    BASIC_COOKIE = "basic_cookie"  # Traditional cookie-based auth
    OAUTH_GOOGLE = "oauth_google"   # Google OAuth
    OAUTH_GITHUB = "oauth_github"   # GitHub OAuth
    API_KEY = "api_key"             # API key in header/query
    CUSTOM = "custom"               # Custom authentication

@dataclass
class SiteConfig:
    """Configuration for a specific site"""
    domain: str
    auth_type: AuthType
    auth_indicators: List[str]  # URL patterns that indicate auth pages
    success_indicators: List[str]  # URL patterns that indicate successful auth
    session_duration_days: int = 7  # How long to keep stored sessions
    special_handling: Optional[Dict] = None  # Any special handling needed
    
class SiteRegistry:
    """Registry of site-specific configurations"""
    
    def __init__(self):
        self.sites = {
            "sensortower.com": SiteConfig(
                domain="sensortower.com",
                auth_type=AuthType.OAUTH_GOOGLE,
                auth_indicators=["sign_in", "login", "auth/google"],
                success_indicators=["/api/docs", "/dashboard"],
                session_duration_days=7,
                special_handling={
                    "needs_subdomain_check": True,  # Check app.sensortower.com too
                    "capture_local_storage": True,   # Capture localStorage for tokens
                }
            ),
            "stripe.com": SiteConfig(
                domain="stripe.com",
                auth_type=AuthType.BASIC_COOKIE,
                auth_indicators=["login", "signin"],
                success_indicators=["/docs", "/dashboard"],
                session_duration_days=30,
            ),
            "github.com": SiteConfig(
                domain="github.com",
                auth_type=AuthType.OAUTH_GITHUB,
                auth_indicators=["login", "signin"],
                success_indicators=["/settings", "/dashboard"],
                session_duration_days=90,
                special_handling={
                    "check_api_subdomain": True,  # Also check api.github.com
                }
            ),
            "openai.com": SiteConfig(
                domain="openai.com",
                auth_type=AuthType.OAUTH_GOOGLE,
                auth_indicators=["auth/login", "login"],
                success_indicators=["/api", "/playground"],
                session_duration_days=30,
                special_handling={
                    "check_platform_subdomain": True,  # Check platform.openai.com
                }
            ),
        }
    
    def get_config(self, url: str) -> Optional[SiteConfig]:
        """Get configuration for a URL"""
        from urllib.parse import urlparse
        
        domain = urlparse(url).netloc
        
        # Direct match
        for site_domain, config in self.sites.items():
            if site_domain in domain:
                return config
        
        # Check parent domains (e.g., app.sensortower.com -> sensortower.com)
        domain_parts = domain.split('.')
        if len(domain_parts) > 2:
            parent_domain = '.'.join(domain_parts[-2:])
            if parent_domain in self.sites:
                return self.sites[parent_domain]
        
        return None
    
    def add_site(self, config: SiteConfig):
        """Add or update a site configuration"""
        self.sites[config.domain] = config
    
    def is_auth_page(self, url: str, config: SiteConfig) -> bool:
        """Check if URL is an authentication page"""
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in config.auth_indicators)
    
    def is_authenticated(self, url: str, config: SiteConfig) -> bool:
        """Check if URL indicates successful authentication"""
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in config.success_indicators)