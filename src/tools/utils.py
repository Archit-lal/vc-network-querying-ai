import json
from typing import Dict, Any, Optional, List
import requests
from datetime import datetime, timedelta


def format_api_response(response: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
    """
    Format API response with consistent structure
    
    Args:
        response: Raw API response
        include_metadata: Whether to include metadata about the response
    
    Returns:
        Formatted response dictionary
    """
    formatted = {
        "data": response,
        "timestamp": datetime.now().isoformat(),
        "success": True
    }
    
    if include_metadata:
        # Add common metadata fields
        if isinstance(response, dict):
            formatted["metadata"] = {
                "record_count": len(response) if isinstance(response, list) else 1,
                "has_pagination": "page_token" in response or "cursor" in response or "next" in response,
                "response_size": len(str(response))
            }
    
    return formatted


def handle_api_error(error: Exception, endpoint: str, api_name: str) -> Dict[str, Any]:
    """
    Standardized error handling for API calls
    
    Args:
        error: The exception that occurred
        endpoint: The API endpoint that failed
        api_name: Name of the API (Affinity/Harmonic)
    
    Returns:
        Formatted error response
    """
    error_response = {
        "success": False,
        "error": {
            "message": str(error),
            "endpoint": endpoint,
            "api": api_name,
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__
        }
    }
    
    # Add specific error details for common HTTP errors
    if isinstance(error, requests.exceptions.HTTPError):
        if hasattr(error, 'response') and error.response is not None:
            error_response["error"]["status_code"] = error.response.status_code
            error_response["error"]["reason"] = error.response.reason
            try:
                error_response["error"]["details"] = error.response.json()
            except:
                error_response["error"]["details"] = error.response.text
    
    return error_response


def validate_pagination_params(page_size: Optional[int] = None, 
                             limit: Optional[int] = None) -> Dict[str, int]:
    """
    Validate and normalize pagination parameters
    
    Args:
        page_size: Page size for Affinity API
        limit: Limit for Harmonic API
    
    Returns:
        Validated pagination parameters
    """
    params = {}
    
    if page_size is not None:
        if page_size < 1 or page_size > 500:
            raise ValueError("page_size must be between 1 and 500")
        params["page_size"] = page_size
    
    if limit is not None:
        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")
        params["limit"] = limit
    
    return params


def build_date_filters(start_date: Optional[str] = None, 
                      end_date: Optional[str] = None) -> Dict[str, str]:
    """
    Build date filter parameters for API calls
    
    Args:
        start_date: Start date in ISO format or relative (e.g., '7d', '1m', '1y')
        end_date: End date in ISO format
    
    Returns:
        Date filter parameters
    """
    filters = {}
    
    if start_date:
        # Handle relative dates
        if start_date.endswith('d'):
            days = int(start_date[:-1])
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
        elif start_date.endswith('m'):
            months = int(start_date[:-1])
            start_date = (datetime.now() - timedelta(days=months*30)).isoformat()
        elif start_date.endswith('y'):
            years = int(start_date[:-1])
            start_date = (datetime.now() - timedelta(days=years*365)).isoformat()
        
        filters["min_interaction_date"] = start_date
    
    if end_date:
        filters["max_interaction_date"] = end_date
    
    return filters


def merge_api_responses(*responses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple API responses into a single response
    
    Args:
        responses: Multiple API response dictionaries
    
    Returns:
        Merged response with combined data
    """
    if not responses:
        return {"data": [], "merged": True}
    
    merged_data = []
    for response in responses:
        if isinstance(response, dict) and "data" in response:
            data = response["data"]
        else:
            data = response
        
        if isinstance(data, list):
            merged_data.extend(data)
        else:
            merged_data.append(data)
    
    return {
        "data": merged_data,
        "merged": True,
        "source_count": len(responses),
        "total_records": len(merged_data),
        "timestamp": datetime.now().isoformat()
    }


def search_filter_builder(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build search filters for API queries
    
    Args:
        filters: Dictionary of filter criteria
    
    Returns:
        Properly formatted filter parameters
    """
    formatted_filters = {}
    
    # Common filter mappings
    filter_mappings = {
        "company_stage": "stage",
        "funding_stage": "funding_stage",
        "employee_count_min": "employee_count_min",
        "employee_count_max": "employee_count_max",
        "founded_year_min": "founded_year_min",
        "founded_year_max": "founded_year_max",
        "industry": "industry",
        "location": "location",
        "technology": "technology"
    }
    
    for key, value in filters.items():
        if value is not None:
            mapped_key = filter_mappings.get(key, key)
            formatted_filters[mapped_key] = value
    
    return formatted_filters


def extract_entity_ids(response: Dict[str, Any], entity_type: str = "id") -> List[str]:
    """
    Extract entity IDs from API response
    
    Args:
        response: API response containing entities
        entity_type: Type of ID to extract (id, person_id, company_id, etc.)
    
    Returns:
        List of extracted IDs
    """
    ids = []
    
    # Handle different response structures
    data = response.get("data", response)
    if isinstance(data, list):
        entities = data
    elif isinstance(data, dict) and "results" in data:
        entities = data["results"]
    elif isinstance(data, dict) and "items" in data:
        entities = data["items"]
    else:
        entities = [data] if isinstance(data, dict) else []
    
    for entity in entities:
        if isinstance(entity, dict) and entity_type in entity:
            ids.append(str(entity[entity_type]))
    
    return ids


def create_batch_processor(api_client, method_name: str, batch_size: int = 50):
    """
    Create a batch processor for API calls
    
    Args:
        api_client: API client instance (Affinity or Harmonic)
        method_name: Name of the method to call
        batch_size: Number of items to process in each batch
    
    Returns:
        Batch processor function
    """
    def process_batch(ids: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Process a batch of IDs"""
        results = []
        method = getattr(api_client, method_name)
        
        for i in range(0, len(ids), batch_size):
            batch = ids[i:i + batch_size]
            for item_id in batch:
                try:
                    result = method(item_id, **kwargs)
                    results.append(result)
                except Exception as e:
                    results.append(handle_api_error(e, f"{method_name}/{item_id}", api_client.__class__.__name__))
        
        return results
    
    return process_batch
