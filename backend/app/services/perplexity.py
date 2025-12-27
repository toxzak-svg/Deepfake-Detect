"""Perplexity AI service for enhanced NLP analysis and threat intelligence.

This module provides integration with Perplexity.ai for:
- Real-time threat intelligence on crypto scams
- Content analysis and fact-checking
- Research on suspicious URLs, addresses, and accounts
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PerplexityService:
    """Service for interacting with Perplexity AI API."""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: int = 30):
        """Initialize Perplexity service.

        Args:
            api_key: Perplexity API key
            base_url: API base URL (default: https://api.perplexity.ai)
            model: Model to use (e.g., llama-3.1-sonar-small-128k-online)
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise ValueError("Perplexity API key is required")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout
        )
        self.model = model

    async def analyze_scam_indicators(
        self,
        url: str,
        description: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze a URL for crypto scam indicators using real-time web search.

        Args:
            url: URL to analyze
            description: Optional description or text content
            additional_context: Additional context about the content

        Returns:
            Dict containing analysis results with scam indicators and risk score
        """
        prompt = self._build_scam_analysis_prompt(url, description, additional_context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity expert specializing in crypto scam detection. "
                                   "Analyze content for deepfake giveaway scams, fake airdrops, and crypto fraud. "
                                   "Provide concise, factual analysis with risk scores."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            return {
                "analysis": result,
                "url": url,
                "model": self.model,
                "success": True
            }

        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return {
                "analysis": None,
                "url": url,
                "error": str(e),
                "success": False
            }

    async def research_wallet_address(self, address: str) -> Dict[str, Any]:
        """Research a cryptocurrency wallet address for scam history.

        Args:
            address: Wallet address to research

        Returns:
            Dict containing research results about the address
        """
        prompt = f"""Research this cryptocurrency wallet address for scam history and reputation:

Address: {address}

Search for:
1. Known scam reports or warnings
2. Transaction patterns indicating fraud
3. Association with crypto giveaway scams
4. Reports on blockchain explorers or scam databases

Provide a concise summary of findings and risk level (low/medium/high)."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a blockchain forensics expert. Research wallet addresses "
                                   "for scam activity and provide factual, evidence-based assessments."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            return {
                "research": result,
                "address": address,
                "model": self.model,
                "success": True
            }

        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return {
                "research": None,
                "address": address,
                "error": str(e),
                "success": False
            }

    async def verify_celebrity_endorsement(
        self,
        celebrity_name: str,
        crypto_project: str,
        claim: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify if a celebrity endorsement claim is legitimate.

        Args:
            celebrity_name: Name of the celebrity
            crypto_project: Name of the crypto project
            claim: Optional specific claim to verify

        Returns:
            Dict containing verification results
        """
        claim_text = f" Specific claim: {claim}" if claim else ""
        prompt = f"""Verify this celebrity endorsement claim:

Celebrity: {celebrity_name}
Crypto Project: {crypto_project}{claim_text}

Search for:
1. Official announcements or statements from the celebrity
2. Verified social media posts
3. News articles from reputable sources
4. Scam warnings about fake endorsements

Determine if this is likely legitimate, fake, or uncertain. Cite sources."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fact-checker specializing in crypto scam detection. "
                                   "Verify celebrity endorsement claims using reputable sources only."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            return {
                "verification": result,
                "celebrity": celebrity_name,
                "project": crypto_project,
                "model": self.model,
                "success": True
            }

        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return {
                "verification": None,
                "celebrity": celebrity_name,
                "project": crypto_project,
                "error": str(e),
                "success": False
            }

    async def analyze_text_for_scam_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze text content for common scam patterns and urgency tactics.

        Args:
            text: Text content to analyze

        Returns:
            Dict containing analysis of scam patterns found
        """
        prompt = f"""Analyze this text for crypto scam indicators:

Text: {text}

Identify:
1. Urgency tactics (limited time, act now, etc.)
2. Promises of guaranteed returns or free crypto
3. Impersonation language
4. Giveaway/airdrop claims
5. Request for wallet addresses or private keys
6. Suspicious links or instructions

Rate the scam risk as low/medium/high and explain key red flags."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an NLP expert specializing in scam detection. "
                                   "Identify manipulation tactics and fraud patterns in text."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content
            return {
                "analysis": result,
                "text_length": len(text),
                "model": self.model,
                "success": True
            }

        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            return {
                "analysis": None,
                "error": str(e),
                "success": False
            }

    def _build_scam_analysis_prompt(
        self,
        url: str,
        description: Optional[str],
        additional_context: Optional[str]
    ) -> str:
        """Build a comprehensive prompt for scam analysis."""
        prompt_parts = [
            f"Analyze this URL for crypto scam indicators:\n\nURL: {url}"
        ]

        if description:
            prompt_parts.append(f"\nDescription/Content: {description}")

        if additional_context:
            prompt_parts.append(f"\nAdditional Context: {additional_context}")

        prompt_parts.append("""
\nSearch for:
1. Known scam reports or warnings about this URL
2. Domain registration age and history
3. Similar scam patterns or phishing attempts
4. Celebrity impersonation or deepfake usage
5. Fake giveaway or airdrop claims
6. Reports from scam databases or security researchers

Provide:
- Risk level (low/medium/high)
- Key red flags identified
- Evidence from web sources
- Recommended action (safe/caution/block)""")

        return "\n".join(prompt_parts)


def create_perplexity_service(
    api_key: str,
    base_url: str = "https://api.perplexity.ai",
    model: str = "llama-3.1-sonar-small-128k-online",
    timeout: int = 30
) -> PerplexityService:
    """Factory function to create a Perplexity service instance.

    Args:
        api_key: Perplexity API key
        base_url: API base URL
        model: Model to use
        timeout: Request timeout in seconds

    Returns:
        Configured PerplexityService instance
    """
    return PerplexityService(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=timeout
    )
