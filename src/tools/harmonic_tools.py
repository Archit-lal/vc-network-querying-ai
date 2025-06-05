import requests
from typing import Optional, Dict, Any, List
from .utils import handle_api_error, format_api_response, validate_pagination_params


class HarmonicAPI:
    """
    Harmonic AI API client for GET endpoints.
    Base URL: https://api.harmonic.ai
    Authentication: Bearer token
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.harmonic.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Harmonic API"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return handle_api_error(e, endpoint, "Harmonic")
    
    # Companies endpoints
    def get_companies(self, limit: Optional[int] = None, offset: Optional[int] = None,
                     search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a list of companies with optional filtering"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        if filters:
            params.update(filters)
        return self._make_request("/companies", params)
    
    def get_company(self, company_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific company"""
        return self._make_request(f"/companies/{company_id}")
    
    def get_company_by_domain(self, domain: str) -> Dict[str, Any]:
        """Get company information by domain"""
        return self._make_request(f"/companies/domain/{domain}")
    
    def get_company_funding(self, company_id: str) -> Dict[str, Any]:
        """Get funding information for a company"""
        return self._make_request(f"/companies/{company_id}/funding")
    
    def get_company_people(self, company_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get people associated with a company"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/companies/{company_id}/people", params)
    
    def get_company_news(self, company_id: str, limit: Optional[int] = None,
                        offset: Optional[int] = None) -> Dict[str, Any]:
        """Get news articles about a company"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/companies/{company_id}/news", params)
    
    def get_company_metrics(self, company_id: str) -> Dict[str, Any]:
        """Get key metrics for a company"""
        return self._make_request(f"/companies/{company_id}/metrics")
    
    def get_company_technologies(self, company_id: str) -> Dict[str, Any]:
        """Get technologies used by a company"""
        return self._make_request(f"/companies/{company_id}/technologies")
    
    def get_company_competitors(self, company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get competitors of a company"""
        params = validate_pagination_params(limit=limit)
        return self._make_request(f"/companies/{company_id}/competitors", params)
    
    def get_company_similar(self, company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get similar companies"""
        params = validate_pagination_params(limit=limit)
        return self._make_request(f"/companies/{company_id}/similar", params)
    
    # People endpoints
    def get_people(self, limit: Optional[int] = None, offset: Optional[int] = None,
                  search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a list of people with optional filtering"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        if filters:
            params.update(filters)
        return self._make_request("/people", params)
    
    def get_person(self, person_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific person"""
        return self._make_request(f"/people/{person_id}")
    
    def get_person_by_email(self, email: str) -> Dict[str, Any]:
        """Get person information by email"""
        return self._make_request(f"/people/email/{email}")
    
    def get_person_companies(self, person_id: str, limit: Optional[int] = None,
                            offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies associated with a person"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/companies", params)
    
    def get_person_investments(self, person_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get investments made by a person"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/investments", params)
    
    def get_person_network(self, person_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get the professional network of a person"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/network", params)
    
    # Industries endpoints
    def get_industries(self) -> Dict[str, Any]:
        """Get all available industries"""
        return self._make_request("/industries")
    
    def get_industry(self, industry_id: str) -> Dict[str, Any]:
        """Get details about a specific industry"""
        return self._make_request(f"/industries/{industry_id}")
    
    def get_industry_companies(self, industry_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies in a specific industry"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/industries/{industry_id}/companies", params)
    
    # Funding endpoints
    def get_funding_rounds(self, limit: Optional[int] = None, offset: Optional[int] = None,
                          filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get funding rounds with optional filtering"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/funding/rounds", params)
    
    def get_funding_round(self, round_id: str) -> Dict[str, Any]:
        """Get details about a specific funding round"""
        return self._make_request(f"/funding/rounds/{round_id}")
    
    # Investors endpoints
    def get_investors(self, limit: Optional[int] = None, offset: Optional[int] = None,
                     filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get investors with optional filtering"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/investors", params)
    
    def get_investor(self, investor_id: str) -> Dict[str, Any]:
        """Get details about a specific investor"""
        return self._make_request(f"/investors/{investor_id}")
    
    def get_investor_portfolio(self, investor_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get the portfolio of an investor"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/investors/{investor_id}/portfolio", params)
    
    def get_investor_investments(self, investor_id: str, limit: Optional[int] = None,
                                offset: Optional[int] = None) -> Dict[str, Any]:
        """Get investments made by an investor"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/investors/{investor_id}/investments", params)
    
    # Search endpoints
    def search_companies(self, query: str, limit: Optional[int] = None,
                        offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for companies"""
        params = validate_pagination_params(limit=limit)
        params["q"] = query
        if offset is not None:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/companies", params)
    
    def search_people(self, query: str, limit: Optional[int] = None,
                     offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for people"""
        params = validate_pagination_params(limit=limit)
        params["q"] = query
        if offset is not None:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/people", params)
    
    def search_investors(self, query: str, limit: Optional[int] = None,
                        offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for investors"""
        params = validate_pagination_params(limit=limit)
        params["q"] = query
        if offset is not None:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/investors", params)
    
    # Saved Searches endpoints
    def get_saved_searches(self) -> Dict[str, Any]:
        """Get all saved searches"""
        return self._make_request("/savedSearches")
    
    def get_saved_search(self, search_id: str) -> Dict[str, Any]:
        """Get details about a specific saved search"""
        return self._make_request(f"/savedSearches/{search_id}")
    
    def get_saved_search_results(self, search_id: str, limit: Optional[int] = None,
                                offset: Optional[int] = None) -> Dict[str, Any]:
        """Get results from a saved search (implements the endpoint found in research)"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/savedSearches:results/{search_id}", params)
    
    # Analytics endpoints
    def get_market_analytics(self, market: str, time_period: Optional[str] = None) -> Dict[str, Any]:
        """Get analytics for a specific market"""
        params = {}
        if time_period:
            params["time_period"] = time_period
        return self._make_request(f"/analytics/markets/{market}", params)
    
    def get_industry_analytics(self, industry: str, time_period: Optional[str] = None) -> Dict[str, Any]:
        """Get analytics for a specific industry"""
        params = {}
        if time_period:
            params["time_period"] = time_period
        return self._make_request(f"/analytics/industries/{industry}", params)
    
    def get_funding_analytics(self, time_period: Optional[str] = None,
                             filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get funding analytics"""
        params = {}
        if time_period:
            params["time_period"] = time_period
        if filters:
            params.update(filters)
        return self._make_request("/analytics/funding", params)
    
    # Lists endpoints
    def get_lists(self) -> Dict[str, Any]:
        """Get all user lists"""
        return self._make_request("/lists")
    
    def get_list(self, list_id: str) -> Dict[str, Any]:
        """Get details about a specific list"""
        return self._make_request(f"/lists/{list_id}")
    
    def get_list_companies(self, list_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies in a specific list"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/lists/{list_id}/companies", params)
    
    # Alerts endpoints
    def get_alerts(self) -> Dict[str, Any]:
        """Get all user alerts"""
        return self._make_request("/alerts")
    
    def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """Get details about a specific alert"""
        return self._make_request(f"/alerts/{alert_id}")
    
    def get_alert_results(self, alert_id: str, limit: Optional[int] = None,
                         offset: Optional[int] = None) -> Dict[str, Any]:
        """Get results from a specific alert"""
        params = validate_pagination_params(limit=limit)
        if offset is not None:
            params["offset"] = offset
        return self._make_request(f"/alerts/{alert_id}/results", params)


def create_harmonic_client(api_key: str) -> HarmonicAPI:
    """Factory function to create a Harmonic API client"""
    return HarmonicAPI(api_key)
