import requests
from typing import Optional, Dict, Any, List, Union
import json


class AffinityAPI:
    """
    Affinity CRM API client for GET endpoints.
    Base URL: https://api.affinity.co
    Authentication: HTTP Basic Auth with API key as password
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.affinity.co"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.auth = ("", api_key)  # HTTP Basic Auth with empty username
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Affinity API"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # Lists endpoints
    def get_lists(self) -> List[Dict[str, Any]]:
        """Get all lists that you have access to"""
        return self._make_request("/lists")
    
    def get_list(self, list_id: int) -> Dict[str, Any]:
        """Get details for a specific list"""
        return self._make_request(f"/lists/{list_id}")
    
    # List Entries endpoints
    def get_list_entries(self, list_id: int, page_size: Optional[int] = None, 
                        page_token: Optional[str] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Get all list entries in a list"""
        params = {}
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        return self._make_request(f"/lists/{list_id}/list-entries", params)
    
    def get_list_entry(self, list_id: int, list_entry_id: int) -> Dict[str, Any]:
        """Get a specific list entry"""
        return self._make_request(f"/lists/{list_id}/list-entries/{list_entry_id}")
    
    # Fields endpoints
    def get_fields(self, list_id: Optional[int] = None, value_type: Optional[int] = None,
                  entity_type: Optional[int] = None, with_modified_names: Optional[bool] = None,
                  exclude_dropdown_options: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get fields based on parameters"""
        params = {}
        if list_id is not None:
            params["list_id"] = list_id
        if value_type is not None:
            params["value_type"] = value_type
        if entity_type is not None:
            params["entity_type"] = entity_type
        if with_modified_names is not None:
            params["with_modified_names"] = with_modified_names
        if exclude_dropdown_options is not None:
            params["exclude_dropdown_options"] = exclude_dropdown_options
        return self._make_request("/fields", params)
    
    # Field Values endpoints
    def get_field_values(self, person_id: Optional[int] = None, organization_id: Optional[int] = None,
                        opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get field values for a person, organization, opportunity, or list entry"""
        params = {}
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        if list_entry_id is not None:
            params["list_entry_id"] = list_entry_id
        return self._make_request("/field-values", params)
    
    # Field Value Changes endpoints
    def get_field_value_changes(self, field_id: int, action_type: Optional[int] = None,
                               person_id: Optional[int] = None, organization_id: Optional[int] = None,
                               opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get field value changes for a specific field"""
        params = {"field_id": field_id}
        if action_type is not None:
            params["action_type"] = action_type
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        if list_entry_id is not None:
            params["list_entry_id"] = list_entry_id
        return self._make_request("/field-value-changes", params)
    
    # Persons endpoints
    def search_persons(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None,
                      with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None,
                      with_current_organizations: Optional[bool] = None, page_size: Optional[int] = None,
                      page_token: Optional[str] = None, **interaction_filters) -> Dict[str, Any]:
        """Search for persons with various filters"""
        params = {}
        if term:
            params["term"] = term
        if with_interaction_dates is not None:
            params["with_interaction_dates"] = with_interaction_dates
        if with_interaction_persons is not None:
            params["with_interaction_persons"] = with_interaction_persons
        if with_opportunities is not None:
            params["with_opportunities"] = with_opportunities
        if with_current_organizations is not None:
            params["with_current_organizations"] = with_current_organizations
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        
        # Add interaction date filters
        for key, value in interaction_filters.items():
            if key.startswith(("min_", "max_")) and key.endswith("_date"):
                params[key] = value
        
        return self._make_request("/persons", params)
    
    def get_person(self, person_id: int, with_interaction_dates: Optional[bool] = None,
                  with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None,
                  with_current_organizations: Optional[bool] = None) -> Dict[str, Any]:
        """Get a specific person by ID"""
        params = {}
        if with_interaction_dates is not None:
            params["with_interaction_dates"] = with_interaction_dates
        if with_interaction_persons is not None:
            params["with_interaction_persons"] = with_interaction_persons
        if with_opportunities is not None:
            params["with_opportunities"] = with_opportunities
        if with_current_organizations is not None:
            params["with_current_organizations"] = with_current_organizations
        return self._make_request(f"/persons/{person_id}", params)
    
    def get_person_fields(self) -> List[Dict[str, Any]]:
        """Get global person fields"""
        return self._make_request("/persons/fields")
    
    # Organizations endpoints
    def search_organizations(self, term: Optional[str] = None, with_interaction_dates: Optional[bool] = None,
                           with_interaction_persons: Optional[bool] = None, page_size: Optional[int] = None,
                           page_token: Optional[str] = None, **interaction_filters) -> Dict[str, Any]:
        """Search for organizations with various filters"""
        params = {}
        if term:
            params["term"] = term
        if with_interaction_dates is not None:
            params["with_interaction_dates"] = with_interaction_dates
        if with_interaction_persons is not None:
            params["with_interaction_persons"] = with_interaction_persons
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        
        # Add interaction date filters
        for key, value in interaction_filters.items():
            if key.startswith(("min_", "max_")) and key.endswith("_date"):
                params[key] = value
        
        return self._make_request("/organizations", params)
    
    def get_organization(self, organization_id: int, with_interaction_dates: Optional[bool] = None,
                        with_interaction_persons: Optional[bool] = None) -> Dict[str, Any]:
        """Get a specific organization by ID"""
        params = {}
        if with_interaction_dates is not None:
            params["with_interaction_dates"] = with_interaction_dates
        if with_interaction_persons is not None:
            params["with_interaction_persons"] = with_interaction_persons
        return self._make_request(f"/organizations/{organization_id}", params)
    
    def get_organization_fields(self) -> List[Dict[str, Any]]:
        """Get global organization fields"""
        return self._make_request("/organizations/fields")
    
    # Opportunities endpoints
    def search_opportunities(self, term: Optional[str] = None, page_size: Optional[int] = None,
                           page_token: Optional[str] = None) -> Dict[str, Any]:
        """Search for opportunities"""
        params = {}
        if term:
            params["term"] = term
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        return self._make_request("/opportunities", params)
    
    def get_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Get a specific opportunity by ID"""
        return self._make_request(f"/opportunities/{opportunity_id}")
    
    # Interactions endpoints
    def get_interactions(self, person_id: Optional[int] = None, organization_id: Optional[int] = None,
                        opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
                        page_token: Optional[str] = None) -> Dict[str, Any]:
        """Get interactions"""
        params = {}
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        return self._make_request("/interactions", params)
    
    def get_interaction(self, interaction_id: int) -> Dict[str, Any]:
        """Get a specific interaction by ID"""
        return self._make_request(f"/interactions/{interaction_id}")
    
    # Relationship Strengths endpoints
    def get_relationship_strengths(self, internal_id: Optional[int] = None, external_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get relationship strength between internal and external persons"""
        params = {}
        if internal_id is not None:
            params["internal_id"] = internal_id
        if external_id is not None:
            params["external_id"] = external_id
        return self._make_request("/relationship-strengths", params)
    
    # Notes endpoints
    def get_notes(self, person_id: Optional[int] = None, organization_id: Optional[int] = None,
                 opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
                 page_token: Optional[str] = None) -> Dict[str, Any]:
        """Get notes"""
        params = {}
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        return self._make_request("/notes", params)
    
    def get_note(self, note_id: int) -> Dict[str, Any]:
        """Get a specific note by ID"""
        return self._make_request(f"/notes/{note_id}")
    
    # Entity Files endpoints
    def get_files(self, person_id: Optional[int] = None, organization_id: Optional[int] = None,
                 opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
                 page_token: Optional[str] = None) -> Dict[str, Any]:
        """Get files attached to entities"""
        params = {}
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        if page_size:
            params["page_size"] = page_size
        if page_token:
            params["page_token"] = page_token
        return self._make_request("/entity-files", params)
    
    def get_file(self, file_id: int) -> Dict[str, Any]:
        """Get a specific file by ID"""
        return self._make_request(f"/entity-files/{file_id}")
    
    def download_file(self, file_id: int) -> bytes:
        """Download a file by ID"""
        url = f"{self.base_url}/entity-files/{file_id}/download"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.content
    
    # Reminders endpoints
    def get_reminders(self, person_id: Optional[int] = None, organization_id: Optional[int] = None,
                     opportunity_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get reminders"""
        params = {}
        if person_id is not None:
            params["person_id"] = person_id
        if organization_id is not None:
            params["organization_id"] = organization_id
        if opportunity_id is not None:
            params["opportunity_id"] = opportunity_id
        return self._make_request("/reminders", params)
    
    def get_reminder(self, reminder_id: int) -> Dict[str, Any]:
        """Get a specific reminder by ID"""
        return self._make_request(f"/reminders/{reminder_id}")
    
    # Webhooks endpoints
    def get_webhook_subscriptions(self) -> List[Dict[str, Any]]:
        """Get all webhook subscriptions"""
        return self._make_request("/webhook-subscriptions")
    
    def get_webhook_subscription(self, webhook_id: int) -> Dict[str, Any]:
        """Get a specific webhook subscription by ID"""
        return self._make_request(f"/webhook-subscriptions/{webhook_id}")
    
    # Whoami endpoint
    def get_whoami(self) -> Dict[str, Any]:
        """Get current user information"""
        return self._make_request("/whoami")
    
    # Rate Limit endpoint
    def get_rate_limit(self) -> Dict[str, Any]:
        """Get rate limit information"""
        return self._make_request("/rate-limit")


class AffinityAPIV2:
    """
    Affinity CRM API v2 client for GET endpoints.
    Base URL: https://api.affinity.co/v2
    Authentication: Bearer token
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.affinity.co/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Affinity API v2"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # Auth endpoints
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        return self._make_request("/auth/whoami")
    
    # Companies endpoints
    def get_companies(self, cursor: Optional[str] = None, limit: Optional[int] = None,
                     ids: Optional[List[int]] = None, field_ids: Optional[List[str]] = None,
                     field_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get all companies with pagination and field filtering"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        if ids:
            params.update({f"ids": id_val for id_val in ids})
        if field_ids:
            params.update({f"fieldIds": field_id for field_id in field_ids})
        if field_types:
            params.update({f"fieldTypes": field_type for field_type in field_types})
        return self._make_request("/companies", params)
    
    def get_company(self, company_id: int, field_ids: Optional[List[str]] = None,
                   field_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a single company by ID"""
        params = {}
        if field_ids:
            params.update({f"fieldIds": field_id for field_id in field_ids})
        if field_types:
            params.update({f"fieldTypes": field_type for field_type in field_types})
        return self._make_request(f"/companies/{company_id}", params)
    
    def get_company_fields(self, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on company fields"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request("/companies/fields", params)
    
    def get_company_lists(self, company_id: int, cursor: Optional[str] = None,
                         limit: Optional[int] = None) -> Dict[str, Any]:
        """Get a company's lists"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/companies/{company_id}/lists", params)
    
    def get_company_list_entries(self, company_id: int, cursor: Optional[str] = None,
                                limit: Optional[int] = None) -> Dict[str, Any]:
        """Get a company's list entries"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/companies/{company_id}/list-entries", params)
    
    # Emails endpoints (coming soon)
    def get_emails(self, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on all emails (coming soon)"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request("/emails", params)
    
    # Lists endpoints
    def get_lists(self, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on all lists"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request("/lists", params)
    
    def get_list(self, list_id: int) -> Dict[str, Any]:
        """Get metadata on a single list"""
        return self._make_request(f"/lists/{list_id}")
    
    def get_list_entries(self, list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None,
                        field_ids: Optional[List[str]] = None, field_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get all list entries on a list"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        if field_ids:
            params.update({f"fieldIds": field_id for field_id in field_ids})
        if field_types:
            params.update({f"fieldTypes": field_type for field_type in field_types})
        return self._make_request(f"/lists/{list_id}/list-entries", params)
    
    def get_list_entry(self, list_id: int, list_entry_id: int) -> Dict[str, Any]:
        """Get a single list entry on a list (BETA)"""
        return self._make_request(f"/lists/{list_id}/list-entries/{list_entry_id}")
    
    def get_list_entry_fields(self, list_id: int, list_entry_id: int) -> Dict[str, Any]:
        """Get field values on a single list entry (BETA)"""
        return self._make_request(f"/lists/{list_id}/list-entries/{list_entry_id}/fields")
    
    def get_list_entry_field(self, list_id: int, list_entry_id: int, field_id: str) -> Dict[str, Any]:
        """Get a single field value (BETA)"""
        return self._make_request(f"/lists/{list_id}/list-entries/{list_entry_id}/fields/{field_id}")
    
    def get_list_fields(self, list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on a single list's fields"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/lists/{list_id}/fields", params)
    
    def get_saved_views(self, list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on saved views"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/lists/{list_id}/saved-views", params)
    
    def get_saved_view(self, list_id: int, view_id: int) -> Dict[str, Any]:
        """Get metadata on a single saved view"""
        return self._make_request(f"/lists/{list_id}/saved-views/{view_id}")
    
    def get_saved_view_list_entries(self, list_id: int, view_id: int, cursor: Optional[str] = None,
                                   limit: Optional[int] = None) -> Dict[str, Any]:
        """Get all list entries on a saved view"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/lists/{list_id}/saved-views/{view_id}/list-entries", params)
    
    # Opportunities endpoints
    def get_opportunities(self, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get all opportunities"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request("/opportunities", params)
    
    def get_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Get a single opportunity"""
        return self._make_request(f"/opportunities/{opportunity_id}")
    
    # Persons endpoints
    def get_persons(self, cursor: Optional[str] = None, limit: Optional[int] = None,
                   ids: Optional[List[int]] = None, field_ids: Optional[List[str]] = None,
                   field_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get all persons with pagination and field filtering"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        if ids:
            params.update({f"ids": id_val for id_val in ids})
        if field_ids:
            params.update({f"fieldIds": field_id for field_id in field_ids})
        if field_types:
            params.update({f"fieldTypes": field_type for field_type in field_types})
        return self._make_request("/persons", params)
    
    def get_person(self, person_id: int, field_ids: Optional[List[str]] = None,
                  field_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a single person by ID"""
        params = {}
        if field_ids:
            params.update({f"fieldIds": field_id for field_id in field_ids})
        if field_types:
            params.update({f"fieldTypes": field_type for field_type in field_types})
        return self._make_request(f"/persons/{person_id}", params)
    
    def get_person_fields(self, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get metadata on person fields"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request("/persons/fields", params)
    
    def get_person_lists(self, person_id: int, cursor: Optional[str] = None,
                        limit: Optional[int] = None) -> Dict[str, Any]:
        """Get a person's lists"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/persons/{person_id}/lists", params)
    
    def get_person_list_entries(self, person_id: int, cursor: Optional[str] = None,
                               limit: Optional[int] = None) -> Dict[str, Any]:
        """Get a person's list entries"""
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        return self._make_request(f"/persons/{person_id}/list-entries", params)


class HarmonicAPI:
    """
    Harmonic API client for GET endpoints.
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
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # Companies endpoints
    def get_companies(self, limit: Optional[int] = None, offset: Optional[int] = None,
                     search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get companies from the Harmonic database"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if search:
            params["search"] = search
        if filters:
            params.update(filters)
        return self._make_request("/companies", params)
    
    def get_company(self, company_id: str) -> Dict[str, Any]:
        """Get a specific company by ID"""
        return self._make_request(f"/companies/{company_id}")
    
    def get_company_by_domain(self, domain: str) -> Dict[str, Any]:
        """Get a company by domain"""
        return self._make_request(f"/companies/domain/{domain}")
    
    def get_company_funding(self, company_id: str) -> Dict[str, Any]:
        """Get funding information for a company"""
        return self._make_request(f"/companies/{company_id}/funding")
    
    def get_company_people(self, company_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get people associated with a company"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/companies/{company_id}/people", params)
    
    def get_company_news(self, company_id: str, limit: Optional[int] = None,
                        offset: Optional[int] = None) -> Dict[str, Any]:
        """Get news for a company"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/companies/{company_id}/news", params)
    
    def get_company_metrics(self, company_id: str) -> Dict[str, Any]:
        """Get metrics for a company"""
        return self._make_request(f"/companies/{company_id}/metrics")
    
    def get_company_technologies(self, company_id: str) -> Dict[str, Any]:
        """Get technologies used by a company"""
        return self._make_request(f"/companies/{company_id}/technologies")
    
    def get_company_competitors(self, company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get competitors for a company"""
        params = {}
        if limit:
            params["limit"] = limit
        return self._make_request(f"/companies/{company_id}/competitors", params)
    
    def get_company_similar(self, company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get similar companies"""
        params = {}
        if limit:
            params["limit"] = limit
        return self._make_request(f"/companies/{company_id}/similar", params)
    
    # People endpoints
    def get_people(self, limit: Optional[int] = None, offset: Optional[int] = None,
                  search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get people from the Harmonic database"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if search:
            params["search"] = search
        if filters:
            params.update(filters)
        return self._make_request("/people", params)
    
    def get_person(self, person_id: str) -> Dict[str, Any]:
        """Get a specific person by ID"""
        return self._make_request(f"/people/{person_id}")
    
    def get_person_by_email(self, email: str) -> Dict[str, Any]:
        """Get a person by email"""
        return self._make_request(f"/people/email/{email}")
    
    def get_person_companies(self, person_id: str, limit: Optional[int] = None,
                            offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies associated with a person"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/companies", params)
    
    def get_person_investments(self, person_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get investments made by a person"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/investments", params)
    
    def get_person_network(self, person_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get a person's network connections"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/people/{person_id}/network", params)
    
    # Industries endpoints
    def get_industries(self) -> Dict[str, Any]:
        """Get all industries"""
        return self._make_request("/industries")
    
    def get_industry(self, industry_id: str) -> Dict[str, Any]:
        """Get a specific industry by ID"""
        return self._make_request(f"/industries/{industry_id}")
    
    def get_industry_companies(self, industry_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies in an industry"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/industries/{industry_id}/companies", params)
    
    # Funding endpoints
    def get_funding_rounds(self, limit: Optional[int] = None, offset: Optional[int] = None,
                          filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get funding rounds"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/funding/rounds", params)
    
    def get_funding_round(self, round_id: str) -> Dict[str, Any]:
        """Get a specific funding round by ID"""
        return self._make_request(f"/funding/rounds/{round_id}")
    
    def get_investors(self, limit: Optional[int] = None, offset: Optional[int] = None,
                     filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get investors"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/investors", params)
    
    def get_investor(self, investor_id: str) -> Dict[str, Any]:
        """Get a specific investor by ID"""
        return self._make_request(f"/investors/{investor_id}")
    
    def get_investor_portfolio(self, investor_id: str, limit: Optional[int] = None,
                              offset: Optional[int] = None) -> Dict[str, Any]:
        """Get an investor's portfolio"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/investors/{investor_id}/portfolio", params)
    
    def get_investor_investments(self, investor_id: str, limit: Optional[int] = None,
                                offset: Optional[int] = None) -> Dict[str, Any]:
        """Get investments made by an investor"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/investors/{investor_id}/investments", params)
    
    # Search endpoints
    def search_companies(self, query: str, limit: Optional[int] = None,
                        offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for companies"""
        params = {"q": query}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/companies", params)
    
    def search_people(self, query: str, limit: Optional[int] = None,
                     offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for people"""
        params = {"q": query}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/people", params)
    
    def search_investors(self, query: str, limit: Optional[int] = None,
                        offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for investors"""
        params = {"q": query}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if filters:
            params.update(filters)
        return self._make_request("/search/investors", params)
    
    # Saved Searches endpoints
    def get_saved_searches(self) -> Dict[str, Any]:
        """Get all saved searches"""
        return self._make_request("/saved-searches")
    
    def get_saved_search(self, search_id: str) -> Dict[str, Any]:
        """Get a specific saved search by ID"""
        return self._make_request(f"/saved-searches/{search_id}")
    
    def get_saved_search_results(self, search_id: str, limit: Optional[int] = None,
                                offset: Optional[int] = None) -> Dict[str, Any]:
        """Get results for a saved search"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/saved-searches/{search_id}/results", params)
    
    # Analytics endpoints
    def get_market_analytics(self, market: str, time_period: Optional[str] = None) -> Dict[str, Any]:
        """Get market analytics"""
        params = {}
        if time_period:
            params["time_period"] = time_period
        return self._make_request(f"/analytics/markets/{market}", params)
    
    def get_industry_analytics(self, industry: str, time_period: Optional[str] = None) -> Dict[str, Any]:
        """Get industry analytics"""
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
        """Get all lists"""
        return self._make_request("/lists")
    
    def get_list(self, list_id: str) -> Dict[str, Any]:
        """Get a specific list by ID"""
        return self._make_request(f"/lists/{list_id}")
    
    def get_list_companies(self, list_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
        """Get companies in a list"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/lists/{list_id}/companies", params)
    
    # Alerts endpoints
    def get_alerts(self) -> Dict[str, Any]:
        """Get all alerts"""
        return self._make_request("/alerts")
    
    def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """Get a specific alert by ID"""
        return self._make_request(f"/alerts/{alert_id}")
    
    def get_alert_results(self, alert_id: str, limit: Optional[int] = None,
                         offset: Optional[int] = None) -> Dict[str, Any]:
        """Get results for an alert"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._make_request(f"/alerts/{alert_id}/results", params)


# Usage examples and helper functions
def create_affinity_client(api_key: str) -> AffinityAPI:
    """Create an Affinity API client"""
    return AffinityAPI(api_key)


def create_affinity_v2_client(api_key: str) -> AffinityAPIV2:
    """Create an Affinity API v2 client"""
    return AffinityAPIV2(api_key)


def create_harmonic_client(api_key: str) -> HarmonicAPI:
    """Create a Harmonic API client"""
    return HarmonicAPI(api_key)
