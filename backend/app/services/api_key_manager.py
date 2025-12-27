from datetime import datetime
from typing import Optional
import hashlib
import secrets

# In production, use Azure Cosmos DB
# For now, in-memory storage
_api_keys_db = {}  # api_key -> user_data
_scan_history_db = []  # list of scan records

class APIKeyManager:
    """Manages API keys, usage tracking, and tier limits."""
    
    TIERS = {
        'free': {'scans_per_month': 10, 'price': 0, 'manual_review': False},
        'pro': {'scans_per_month': 500, 'price': 49, 'manual_review': True},
        'enterprise': {'scans_per_month': -1, 'price': None, 'manual_review': True},  # -1 = unlimited
    }
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return 'dfg_' + secrets.token_urlsafe(32)
    
    @staticmethod
    def create_user(email: str, tier: str = 'free', webhook_url: Optional[str] = None) -> dict:
        """Create a new user account with API key."""
        if tier not in APIKeyManager.TIERS:
            raise ValueError(f"Invalid tier: {tier}")
        
        api_key = APIKeyManager.generate_api_key()
        
        user_data = {
            'email': email,
            'api_key': api_key,
            'tier': tier,
            'webhook_url': webhook_url,
            'scans_used_this_month': 0,
            'total_scans': 0,
            'created_at': datetime.utcnow().isoformat(),
            'current_period_start': datetime.utcnow().isoformat(),
            'active': True,
        }
        
        _api_keys_db[api_key] = user_data
        return user_data
    
    @staticmethod
    def validate_api_key(api_key: str) -> tuple[bool, Optional[dict], Optional[str]]:
        """
        Validate API key and check usage limits.
        Returns: (is_valid, user_data, error_message)
        """
        if not api_key or not api_key.startswith('dfg_'):
            return False, None, "Invalid API key format"
        
        user_data = _api_keys_db.get(api_key)
        if not user_data:
            return False, None, "API key not found"
        
        if not user_data['active']:
            return False, None, "API key has been deactivated"
        
        # Check usage limits
        tier = user_data['tier']
        tier_config = APIKeyManager.TIERS[tier]
        scans_limit = tier_config['scans_per_month']
        
        if scans_limit != -1 and user_data['scans_used_this_month'] >= scans_limit:
            return False, user_data, f"Monthly scan limit reached ({scans_limit} scans). Please upgrade your plan."
        
        return True, user_data, None
    
    @staticmethod
    def increment_usage(api_key: str, scan_data: dict):
        """Increment usage counter and record scan."""
        user_data = _api_keys_db.get(api_key)
        if not user_data:
            return
        
        user_data['scans_used_this_month'] += 1
        user_data['total_scans'] += 1
        
        # Record scan in history
        scan_record = {
            'api_key': api_key,
            'email': user_data['email'],
            'timestamp': datetime.utcnow().isoformat(),
            'url': scan_data.get('url'),
            'score': scan_data.get('score'),
            'flagged': scan_data.get('score', 0) > 0.6,
            'manual_review_pending': user_data['tier'] in ['pro', 'enterprise'] and scan_data.get('score', 0) > 0.6,
        }
        _scan_history_db.append(scan_record)
        
        return scan_record
    
    @staticmethod
    def get_user_stats(api_key: str) -> Optional[dict]:
        """Get usage statistics for a user."""
        user_data = _api_keys_db.get(api_key)
        if not user_data:
            return None
        
        tier_config = APIKeyManager.TIERS[user_data['tier']]
        scans_limit = tier_config['scans_per_month']
        
        return {
            'email': user_data['email'],
            'tier': user_data['tier'],
            'scans_used': user_data['scans_used_this_month'],
            'scans_limit': scans_limit if scans_limit != -1 else 'unlimited',
            'scans_remaining': scans_limit - user_data['scans_used_this_month'] if scans_limit != -1 else 'unlimited',
            'total_scans': user_data['total_scans'],
            'created_at': user_data['created_at'],
        }
    
    @staticmethod
    def get_pending_reviews() -> list:
        """Get all scans pending manual review."""
        return [scan for scan in _scan_history_db if scan.get('manual_review_pending')]
    
    @staticmethod
    def update_webhook_url(api_key: str, webhook_url: str) -> bool:
        """Update webhook URL for a user."""
        user_data = _api_keys_db.get(api_key)
        if not user_data:
            return False
        
        user_data['webhook_url'] = webhook_url
        return True
    
    @staticmethod
    def get_webhook_url(api_key: str) -> Optional[str]:
        """Get webhook URL for a user."""
        user_data = _api_keys_db.get(api_key)
        return user_data.get('webhook_url') if user_data else None
