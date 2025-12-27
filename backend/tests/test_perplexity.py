"""Tests for Perplexity AI integration.

Run with: pytest tests/test_perplexity.py -v
"""

import pytest
from app.services.perplexity import PerplexityService, create_perplexity_service


def test_perplexity_service_initialization():
    """Test that PerplexityService initializes correctly."""
    service = create_perplexity_service(
        api_key="test-key",
        base_url="https://api.perplexity.ai",
        model="llama-3.1-sonar-small-128k-online",
        timeout=30
    )
    assert service is not None
    assert service.model == "llama-3.1-sonar-small-128k-online"


def test_perplexity_service_requires_api_key():
    """Test that PerplexityService requires an API key."""
    with pytest.raises(ValueError, match="API key is required"):
        PerplexityService(
            api_key="",
            base_url="https://api.perplexity.ai",
            model="llama-3.1-sonar-small-128k-online",
            timeout=30
        )


@pytest.mark.asyncio
async def test_analyze_scam_indicators_without_real_api():
    """Test scam analysis endpoint structure (mock test)."""
    # This is a mock test - replace with real API key for integration testing
    # We just verify the method exists and returns correct structure on error
    service = create_perplexity_service(
        api_key="fake-test-key",
        base_url="https://api.perplexity.ai",
        model="llama-3.1-sonar-small-128k-online"
    )
    
    result = await service.analyze_scam_indicators(
        url="https://example.com",
        description="Test scam"
    )
    
    # Should return error structure with fake key
    assert "url" in result
    assert "success" in result
    assert result["url"] == "https://example.com"


@pytest.mark.asyncio
async def test_research_wallet_address_without_real_api():
    """Test wallet research endpoint structure (mock test)."""
    service = create_perplexity_service(
        api_key="fake-test-key",
        base_url="https://api.perplexity.ai",
        model="llama-3.1-sonar-small-128k-online"
    )
    
    result = await service.research_wallet_address(
        address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    )
    
    assert "address" in result
    assert "success" in result
    assert result["address"] == "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"


@pytest.mark.asyncio
async def test_verify_celebrity_endorsement_without_real_api():
    """Test endorsement verification endpoint structure (mock test)."""
    service = create_perplexity_service(
        api_key="fake-test-key",
        base_url="https://api.perplexity.ai",
        model="llama-3.1-sonar-small-128k-online"
    )
    
    result = await service.verify_celebrity_endorsement(
        celebrity_name="Elon Musk",
        crypto_project="Bitcoin Giveaway",
        claim="Double your BTC"
    )
    
    assert "celebrity" in result
    assert "project" in result
    assert "success" in result


@pytest.mark.asyncio
async def test_analyze_text_for_scam_patterns_without_real_api():
    """Test text analysis endpoint structure (mock test)."""
    service = create_perplexity_service(
        api_key="fake-test-key",
        base_url="https://api.perplexity.ai",
        model="llama-3.1-sonar-small-128k-online"
    )
    
    result = await service.analyze_text_for_scam_patterns(
        text="URGENT! Send BTC now to receive 10x back!"
    )
    
    assert "success" in result
    if result["success"]:
        assert "analysis" in result
    else:
        assert "error" in result


# Integration tests (require real API key)
# Uncomment and set PERPLEXITY_API_KEY environment variable to run

# @pytest.mark.asyncio
# @pytest.mark.integration
# async def test_real_scam_analysis():
#     """Test real API call to analyze scam."""
#     import os
#     api_key = os.environ.get("PERPLEXITY_API_KEY")
#     if not api_key:
#         pytest.skip("PERPLEXITY_API_KEY not set")
#     
#     service = create_perplexity_service(api_key=api_key)
#     result = await service.analyze_scam_indicators(
#         url="https://example.com",
#         description="Test legitimate site"
#     )
#     
#     assert result["success"] is True
#     assert "analysis" in result
#     assert len(result["analysis"]) > 0
