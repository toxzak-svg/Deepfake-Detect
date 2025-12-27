import httpx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

class WebhookService:
    """Service for sending webhook notifications to customers."""
    
    @staticmethod
    async def send_webhook(
        webhook_url: str,
        event_type: str,
        data: Dict[Any, Any],
        retry_count: int = 3
    ) -> bool:
        """
        Send webhook notification to customer endpoint.
        
        Args:
            webhook_url: Customer's webhook endpoint URL
            event_type: Type of event (e.g., 'scan.completed', 'scan.flagged', 'review.completed')
            data: Event data to send
            retry_count: Number of retry attempts
            
        Returns:
            True if webhook was successfully delivered, False otherwise
        """
        payload = {
            'event': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'DeepfakeGuard-Webhook/1.0',
        }
        
        for attempt in range(retry_count):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        webhook_url,
                        json=payload,
                        headers=headers
                    )
                    
                    if response.status_code in [200, 201, 202, 204]:
                        print(f"✅ Webhook delivered successfully: {event_type} to {webhook_url}")
                        return True
                    else:
                        print(f"⚠️ Webhook failed with status {response.status_code}: {webhook_url}")
                        
            except httpx.TimeoutException:
                print(f"⏱️ Webhook timeout (attempt {attempt + 1}/{retry_count}): {webhook_url}")
            except httpx.RequestError as e:
                print(f"❌ Webhook request error (attempt {attempt + 1}/{retry_count}): {e}")
            except Exception as e:
                print(f"❌ Unexpected webhook error: {e}")
            
            # Exponential backoff
            if attempt < retry_count - 1:
                await asyncio.sleep(2 ** attempt)
        
        print(f"❌ Webhook failed after {retry_count} attempts: {webhook_url}")
        return False
    
    @staticmethod
    async def notify_scan_completed(webhook_url: str, scan_id: str, result: Dict[Any, Any]) -> bool:
        """Send notification when scan is completed."""
        return await WebhookService.send_webhook(
            webhook_url=webhook_url,
            event_type='scan.completed',
            data={
                'scan_id': scan_id,
                'url': result.get('url'),
                'score': result.get('score'),
                'flags': result.get('flags', []),
                'is_flagged': result.get('score', 0) > 0.6,
            }
        )
    
    @staticmethod
    async def notify_scan_flagged(webhook_url: str, scan_id: str, result: Dict[Any, Any]) -> bool:
        """Send notification when deepfake is detected (high score)."""
        return await WebhookService.send_webhook(
            webhook_url=webhook_url,
            event_type='scan.flagged',
            data={
                'scan_id': scan_id,
                'url': result.get('url'),
                'score': result.get('score'),
                'flags': result.get('flags', []),
                'severity': 'high' if result.get('score', 0) > 0.8 else 'medium',
                'manual_review_pending': True,
            }
        )
    
    @staticmethod
    async def notify_review_completed(
        webhook_url: str,
        scan_id: str,
        original_score: float,
        reviewed_verdict: str,
        reviewer_notes: Optional[str] = None
    ) -> bool:
        """Send notification when manual review is completed."""
        return await WebhookService.send_webhook(
            webhook_url=webhook_url,
            event_type='review.completed',
            data={
                'scan_id': scan_id,
                'original_score': original_score,
                'reviewed_verdict': reviewed_verdict,  # 'confirmed', 'false_positive', 'uncertain'
                'reviewer_notes': reviewer_notes,
            }
        )
