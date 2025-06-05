import os
from src.prompts import prompt
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_openai_tools_agent
from src.tools.affinity_tools import *
from src.tools.harmonic_tools import *
from src.tools.utils import *
from typing import Optional, Dict, Any, List, Union
from langchain.tools import tool

# Initialize API clients
affinity_client = AffinityAPI(os.getenv("AFFINITY_API_KEY"))
affinity_v2_client = AffinityAPIV2(os.getenv("AFFINITY_API_KEY"))
harmonic_client = HarmonicAPI(os.getenv("HARMONIC_API_KEY"))

# Affinity API v1 Tools
@tool
def get_lists() -> List[Dict[str, Any]]:
    """Get all lists that you have access to"""
    return affinity_client.get_lists()

@tool
def get_list(list_id: int) -> Dict[str, Any]:
    """Get details for a specific list"""
    return affinity_client.get_list(list_id)

@tool
def get_list_entries(list_id: int, page_size: Optional[int] = None, 
                    page_token: Optional[str] = None) -> Dict[str, Any]:
    """Get all list entries in a list"""
    return affinity_client.get_list_entries(list_id, page_size, page_token)

@tool
def get_list_entry(list_id: int, list_entry_id: int) -> Dict[str, Any]:
    """Get a specific list entry"""
    return affinity_client.get_list_entry(list_id, list_entry_id)

@tool
def get_fields(list_id: Optional[int] = None, value_type: Optional[int] = None,
              entity_type: Optional[int] = None, with_modified_names: Optional[bool] = None,
              exclude_dropdown_options: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Get fields based on parameters"""
    return affinity_client.get_fields(list_id, value_type, entity_type, 
                                    with_modified_names, exclude_dropdown_options)

@tool
def get_field_values(person_id: Optional[int] = None, organization_id: Optional[int] = None,
                    opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get field values for a person, organization, opportunity, or list entry"""
    return affinity_client.get_field_values(person_id, organization_id, 
                                          opportunity_id, list_entry_id)

@tool
def get_field_value_changes(field_id: int, action_type: Optional[int] = None,
                           person_id: Optional[int] = None, organization_id: Optional[int] = None,
                           opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get field value changes for a specific field"""
    return affinity_client.get_field_value_changes(field_id, action_type, person_id,
                                                 organization_id, opportunity_id, list_entry_id)

@tool
def search_persons(term: Optional[str] = None, with_interaction_dates: Optional[bool] = None,
                  with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None,
                  with_current_organizations: Optional[bool] = None, page_size: Optional[int] = None,
                  page_token: Optional[str] = None, **interaction_filters) -> Dict[str, Any]:
    """Search for persons with various filters"""
    return affinity_client.search_persons(term, with_interaction_dates, with_interaction_persons,
                                        with_opportunities, with_current_organizations,
                                        page_size, page_token, **interaction_filters)

@tool
def get_person(person_id: int, with_interaction_dates: Optional[bool] = None,
              with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None,
              with_current_organizations: Optional[bool] = None) -> Dict[str, Any]:
    """Get a specific person by ID"""
    return affinity_client.get_person(person_id, with_interaction_dates, with_interaction_persons,
                                    with_opportunities, with_current_organizations)

@tool
def get_person_fields() -> List[Dict[str, Any]]:
    """Get global person fields"""
    return affinity_client.get_person_fields()

@tool
def search_organizations(term: Optional[str] = None, with_interaction_dates: Optional[bool] = None,
                        with_interaction_persons: Optional[bool] = None, page_size: Optional[int] = None,
                        page_token: Optional[str] = None, **interaction_filters) -> Dict[str, Any]:
    """Search for organizations with various filters"""
    return affinity_client.search_organizations(term, with_interaction_dates, with_interaction_persons,
                                              page_size, page_token, **interaction_filters)

@tool
def get_organization(organization_id: int, with_interaction_dates: Optional[bool] = None,
                    with_interaction_persons: Optional[bool] = None) -> Dict[str, Any]:
    """Get a specific organization by ID"""
    return affinity_client.get_organization(organization_id, with_interaction_dates, with_interaction_persons)

@tool
def get_organization_fields() -> List[Dict[str, Any]]:
    """Get global organization fields"""
    return affinity_client.get_organization_fields()

@tool
def search_opportunities(term: Optional[str] = None, page_size: Optional[int] = None,
                        page_token: Optional[str] = None) -> Dict[str, Any]:
    """Search for opportunities"""
    return affinity_client.search_opportunities(term, page_size, page_token)

@tool
def get_opportunity(opportunity_id: int) -> Dict[str, Any]:
    """Get a specific opportunity by ID"""
    return affinity_client.get_opportunity(opportunity_id)

@tool
def get_interactions(person_id: Optional[int] = None, organization_id: Optional[int] = None,
                    opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
                    page_token: Optional[str] = None) -> Dict[str, Any]:
    """Get interactions"""
    return affinity_client.get_interactions(person_id, organization_id, opportunity_id,
                                          page_size, page_token)

@tool
def get_interaction(interaction_id: int) -> Dict[str, Any]:
    """Get a specific interaction by ID"""
    return affinity_client.get_interaction(interaction_id)

@tool
def get_relationship_strengths(internal_id: Optional[int] = None, external_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get relationship strength between internal and external persons"""
    return affinity_client.get_relationship_strengths(internal_id, external_id)

@tool
def get_notes(person_id: Optional[int] = None, organization_id: Optional[int] = None,
             opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
             page_token: Optional[str] = None) -> Dict[str, Any]:
    """Get notes"""
    return affinity_client.get_notes(person_id, organization_id, opportunity_id,
                                   page_size, page_token)

@tool
def get_note(note_id: int) -> Dict[str, Any]:
    """Get a specific note by ID"""
    return affinity_client.get_note(note_id)

@tool
def get_files(person_id: Optional[int] = None, organization_id: Optional[int] = None,
             opportunity_id: Optional[int] = None, page_size: Optional[int] = None,
             page_token: Optional[str] = None) -> Dict[str, Any]:
    """Get files attached to entities"""
    return affinity_client.get_files(person_id, organization_id, opportunity_id,
                                   page_size, page_token)

@tool
def get_file(file_id: int) -> Dict[str, Any]:
    """Get a specific file by ID"""
    return affinity_client.get_file(file_id)

@tool
def download_file(file_id: int) -> bytes:
    """Download a file by ID"""
    return affinity_client.download_file(file_id)

@tool
def get_reminders(person_id: Optional[int] = None, organization_id: Optional[int] = None,
                 opportunity_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get reminders"""
    return affinity_client.get_reminders(person_id, organization_id, opportunity_id)

@tool
def get_reminder(reminder_id: int) -> Dict[str, Any]:
    """Get a specific reminder by ID"""
    return affinity_client.get_reminder(reminder_id)

@tool
def get_webhook_subscriptions() -> List[Dict[str, Any]]:
    """Get all webhook subscriptions"""
    return affinity_client.get_webhook_subscriptions()

@tool
def get_webhook_subscription(webhook_id: int) -> Dict[str, Any]:
    """Get a specific webhook subscription by ID"""
    return affinity_client.get_webhook_subscription(webhook_id)

@tool
def get_whoami() -> Dict[str, Any]:
    """Get current user information"""
    return affinity_client.get_whoami()

@tool
def get_rate_limit() -> Dict[str, Any]:
    """Get rate limit information"""
    return affinity_client.get_rate_limit()

# Affinity API v2 Tools
@tool
def get_current_user() -> Dict[str, Any]:
    """Get current user information"""
    return affinity_v2_client.get_current_user()

@tool
def get_companies_v2(cursor: Optional[str] = None, limit: Optional[int] = None,
                    ids: Optional[List[int]] = None, field_ids: Optional[List[str]] = None,
                    field_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get all companies with pagination and field filtering"""
    return affinity_v2_client.get_companies(cursor, limit, ids, field_ids, field_types)

@tool
def get_company_v2(company_id: int, field_ids: Optional[List[str]] = None,
                  field_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get a single company by ID"""
    return affinity_v2_client.get_company(company_id, field_ids, field_types)

@tool
def get_company_fields_v2(cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on company fields"""
    return affinity_v2_client.get_company_fields(cursor, limit)

@tool
def get_company_lists_v2(company_id: int, cursor: Optional[str] = None,
                        limit: Optional[int] = None) -> Dict[str, Any]:
    """Get a company's lists"""
    return affinity_v2_client.get_company_lists(company_id, cursor, limit)

@tool
def get_company_list_entries_v2(company_id: int, cursor: Optional[str] = None,
                               limit: Optional[int] = None) -> Dict[str, Any]:
    """Get a company's list entries"""
    return affinity_v2_client.get_company_list_entries(company_id, cursor, limit)

@tool
def get_emails(cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on all emails"""
    return affinity_v2_client.get_emails(cursor, limit)

@tool
def get_lists_v2(cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on all lists"""
    return affinity_v2_client.get_lists(cursor, limit)

@tool
def get_list_v2(list_id: int) -> Dict[str, Any]:
    """Get metadata on a single list"""
    return affinity_v2_client.get_list(list_id)

@tool
def get_list_entries_v2(list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None,
                       field_ids: Optional[List[str]] = None, field_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get all list entries on a list"""
    return affinity_v2_client.get_list_entries(list_id, cursor, limit, field_ids, field_types)

@tool
def get_list_entry_v2(list_id: int, list_entry_id: int) -> Dict[str, Any]:
    """Get a single list entry on a list"""
    return affinity_v2_client.get_list_entry(list_id, list_entry_id)

@tool
def get_list_entry_fields(list_id: int, list_entry_id: int) -> Dict[str, Any]:
    """Get field values on a single list entry"""
    return affinity_v2_client.get_list_entry_fields(list_id, list_entry_id)

@tool
def get_list_entry_field(list_id: int, list_entry_id: int, field_id: str) -> Dict[str, Any]:
    """Get a single field value"""
    return affinity_v2_client.get_list_entry_field(list_id, list_entry_id, field_id)

@tool
def get_list_fields(list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on a single list's fields"""
    return affinity_v2_client.get_list_fields(list_id, cursor, limit)

@tool
def get_saved_views(list_id: int, cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on saved views"""
    return affinity_v2_client.get_saved_views(list_id, cursor, limit)

@tool
def get_saved_view(list_id: int, view_id: int) -> Dict[str, Any]:
    """Get metadata on a single saved view"""
    return affinity_v2_client.get_saved_view(list_id, view_id)

@tool
def get_saved_view_list_entries(list_id: int, view_id: int, cursor: Optional[str] = None,
                               limit: Optional[int] = None) -> Dict[str, Any]:
    """Get all list entries on a saved view"""
    return affinity_v2_client.get_saved_view_list_entries(list_id, view_id, cursor, limit)

@tool
def get_opportunities_v2(cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get all opportunities"""
    return affinity_v2_client.get_opportunities(cursor, limit)

@tool
def get_opportunity_v2(opportunity_id: int) -> Dict[str, Any]:
    """Get a single opportunity"""
    return affinity_v2_client.get_opportunity(opportunity_id)

@tool
def get_persons_v2(cursor: Optional[str] = None, limit: Optional[int] = None,
                  ids: Optional[List[int]] = None, field_ids: Optional[List[str]] = None,
                  field_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get all persons with pagination and field filtering"""
    return affinity_v2_client.get_persons(cursor, limit, ids, field_ids, field_types)

@tool
def get_person_v2(person_id: int, field_ids: Optional[List[str]] = None,
                 field_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get a single person by ID"""
    return affinity_v2_client.get_person(person_id, field_ids, field_types)

@tool
def get_person_fields_v2(cursor: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get metadata on person fields"""
    return affinity_v2_client.get_person_fields(cursor, limit)

@tool
def get_person_lists(person_id: int, cursor: Optional[str] = None,
                    limit: Optional[int] = None) -> Dict[str, Any]:
    """Get a person's lists"""
    return affinity_v2_client.get_person_lists(person_id, cursor, limit)

@tool
def get_person_list_entries(person_id: int, cursor: Optional[str] = None,
                           limit: Optional[int] = None) -> Dict[str, Any]:
    """Get a person's list entries"""
    return affinity_v2_client.get_person_list_entries(person_id, cursor, limit)

# Harmonic API Tools
@tool
def get_companies(limit: Optional[int] = None, offset: Optional[int] = None,
                 search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get companies from the Harmonic database"""
    return harmonic_client.get_companies(limit, offset, search, filters)

@tool
def get_company(company_id: str) -> Dict[str, Any]:
    """Get a specific company by ID"""
    return harmonic_client.get_company(company_id)

@tool
def get_company_by_domain(domain: str) -> Dict[str, Any]:
    """Get a company by domain"""
    return harmonic_client.get_company_by_domain(domain)

@tool
def get_company_funding(company_id: str) -> Dict[str, Any]:
    """Get funding information for a company"""
    return harmonic_client.get_company_funding(company_id)

@tool
def get_company_people(company_id: str, limit: Optional[int] = None,
                      offset: Optional[int] = None) -> Dict[str, Any]:
    """Get people associated with a company"""
    return harmonic_client.get_company_people(company_id, limit, offset)

@tool
def get_company_news(company_id: str, limit: Optional[int] = None,
                    offset: Optional[int] = None) -> Dict[str, Any]:
    """Get news for a company"""
    return harmonic_client.get_company_news(company_id, limit, offset)

@tool
def get_company_metrics(company_id: str) -> Dict[str, Any]:
    """Get metrics for a company"""
    return harmonic_client.get_company_metrics(company_id)

@tool
def get_company_technologies(company_id: str) -> Dict[str, Any]:
    """Get technologies used by a company"""
    return harmonic_client.get_company_technologies(company_id)

@tool
def get_company_competitors(company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get competitors for a company"""
    return harmonic_client.get_company_competitors(company_id, limit)

@tool
def get_company_similar(company_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get similar companies"""
    return harmonic_client.get_company_similar(company_id, limit)

@tool
def get_people(limit: Optional[int] = None, offset: Optional[int] = None,
              search: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get people from the Harmonic database"""
    return harmonic_client.get_people(limit, offset, search, filters)

@tool
def get_person_harmonic(person_id: str) -> Dict[str, Any]:
    """Get a specific person by ID"""
    return harmonic_client.get_person(person_id)

@tool
def get_person_by_email(email: str) -> Dict[str, Any]:
    """Get a person by email"""
    return harmonic_client.get_person_by_email(email)

@tool
def get_person_companies(person_id: str, limit: Optional[int] = None,
                        offset: Optional[int] = None) -> Dict[str, Any]:
    """Get companies associated with a person"""
    return harmonic_client.get_person_companies(person_id, limit, offset)

@tool
def get_person_investments(person_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
    """Get investments made by a person"""
    return harmonic_client.get_person_investments(person_id, limit, offset)

@tool
def get_person_network(person_id: str, limit: Optional[int] = None,
                      offset: Optional[int] = None) -> Dict[str, Any]:
    """Get a person's network connections"""
    return harmonic_client.get_person_network(person_id, limit, offset)

@tool
def get_industries() -> Dict[str, Any]:
    """Get all industries"""
    return harmonic_client.get_industries()

@tool
def get_industry(industry_id: str) -> Dict[str, Any]:
    """Get a specific industry by ID"""
    return harmonic_client.get_industry(industry_id)

@tool
def get_industry_companies(industry_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
    """Get companies in an industry"""
    return harmonic_client.get_industry_companies(industry_id, limit, offset)

@tool
def get_funding_rounds(limit: Optional[int] = None, offset: Optional[int] = None,
                      filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get funding rounds"""
    return harmonic_client.get_funding_rounds(limit, offset, filters)

@tool
def get_funding_round(round_id: str) -> Dict[str, Any]:
    """Get a specific funding round by ID"""
    return harmonic_client.get_funding_round(round_id)

@tool
def get_investors(limit: Optional[int] = None, offset: Optional[int] = None,
                 filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get investors"""
    return harmonic_client.get_investors(limit, offset, filters)

@tool
def get_investor(investor_id: str) -> Dict[str, Any]:
    """Get a specific investor by ID"""
    return harmonic_client.get_investor(investor_id)

@tool
def get_investor_portfolio(investor_id: str, limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Dict[str, Any]:
    """Get an investor's portfolio"""
    return harmonic_client.get_investor_portfolio(investor_id, limit, offset)

@tool
def get_investor_investments(investor_id: str, limit: Optional[int] = None,
                            offset: Optional[int] = None) -> Dict[str, Any]:
    """Get investments made by an investor"""
    return harmonic_client.get_investor_investments(investor_id, limit, offset)

@tool
def search_companies(query: str, limit: Optional[int] = None,
                    offset: Optional[int] = None, filters: Optional[Union[Dict[str, Any], str]] = None) -> Dict[str, Any]:
    """Search for companies
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        offset: Number of results to skip
        filters: Either a dictionary of filters or a string in format 'key=value'
    """
    if isinstance(filters, str):
        # Convert string filter to dictionary
        filter_dict = {}
        for filter_item in filters.split(','):
            if '=' in filter_item:
                key, value = filter_item.split('=', 1)
                filter_dict[key.strip()] = value.strip()
        filters = filter_dict
    return harmonic_client.search_companies(query, limit, offset, filters)

@tool
def search_people(query: str, limit: Optional[int] = None,
                 offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Search for people"""
    return harmonic_client.search_people(query, limit, offset, filters)

@tool
def search_investors(query: str, limit: Optional[int] = None,
                    offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Search for investors"""
    return harmonic_client.search_investors(query, limit, offset, filters)

@tool
def get_saved_searches() -> Dict[str, Any]:
    """Get all saved searches"""
    return harmonic_client.get_saved_searches()

@tool
def get_saved_search(search_id: str) -> Dict[str, Any]:
    """Get a specific saved search by ID"""
    return harmonic_client.get_saved_search(search_id)

@tool
def get_saved_search_results(search_id: str, limit: Optional[int] = None,
                            offset: Optional[int] = None) -> Dict[str, Any]:
    """Get results for a saved search"""
    return harmonic_client.get_saved_search_results(search_id, limit, offset)

@tool
def get_market_analytics(market: str, time_period: Optional[str] = None) -> Dict[str, Any]:
    """Get market analytics"""
    return harmonic_client.get_market_analytics(market, time_period)

@tool
def get_industry_analytics(industry: str, time_period: Optional[str] = None) -> Dict[str, Any]:
    """Get industry analytics"""
    return harmonic_client.get_industry_analytics(industry, time_period)

@tool
def get_funding_analytics(time_period: Optional[str] = None,
                         filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get funding analytics"""
    return harmonic_client.get_funding_analytics(time_period, filters)

@tool
def get_lists_harmonic() -> Dict[str, Any]:
    """Get all lists"""
    return harmonic_client.get_lists()

@tool
def get_list_harmonic(list_id: str) -> Dict[str, Any]:
    """Get a specific list by ID"""
    return harmonic_client.get_list(list_id)

@tool
def get_list_companies(list_id: str, limit: Optional[int] = None,
                      offset: Optional[int] = None) -> Dict[str, Any]:
    """Get companies in a list"""
    return harmonic_client.get_list_companies(list_id, limit, offset)

@tool
def get_alerts() -> Dict[str, Any]:
    """Get all alerts"""
    return harmonic_client.get_alerts()

@tool
def get_alert(alert_id: str) -> Dict[str, Any]:
    """Get a specific alert by ID"""
    return harmonic_client.get_alert(alert_id)

@tool
def get_alert_results(alert_id: str, limit: Optional[int] = None,
                     offset: Optional[int] = None) -> Dict[str, Any]:
    """Get results for an alert"""
    return harmonic_client.get_alert_results(alert_id, limit, offset)

# Utility Tools
@tool
def format_api_response_tool(response: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
    """Format API response with consistent structure"""
    return format_api_response(response, include_metadata)

@tool
def validate_pagination_params_tool(page_size: Optional[int] = None, 
                                  limit: Optional[int] = None) -> Dict[str, int]:
    """Validate and normalize pagination parameters"""
    return validate_pagination_params(page_size, limit)

@tool
def build_date_filters_tool(start_date: Optional[str] = None, 
                          end_date: Optional[str] = None) -> Dict[str, str]:
    """Build date filter parameters for API calls"""
    return build_date_filters(start_date, end_date)

@tool
def search_filter_builder_tool(filters: Dict[str, Any]) -> Dict[str, Any]:
    """Build search filters for API queries"""
    return search_filter_builder(filters)

@tool
def extract_entity_ids_tool(response: Dict[str, Any], entity_type: str = "id") -> List[str]:
    """Extract entity IDs from API response"""
    return extract_entity_ids(response, entity_type)

@tool
def create_batch_processor_tool(api_client: Any, method_name: str, batch_size: int = 50) -> Any:
    """Create a batch processor for API calls"""
    return create_batch_processor(api_client, method_name, batch_size)

def get_agent():
    llm = init_chat_model(
        model="gemini-2.0-flash",
        model_provider="google_genai",
        temperature=1.0,
        api_key=os.getenv("GEMINI_API_KEY")
    )

    tools = [
        get_lists, get_list, get_list_entries, get_list_entry, get_fields,
        get_field_values, get_field_value_changes, search_persons, get_person,
        get_person_fields, search_organizations, get_organization, get_organization_fields,
        search_opportunities, get_opportunity, get_interactions, get_interaction,
        get_relationship_strengths, get_notes, get_note, get_files, get_file,
        download_file, get_reminders, get_reminder, get_webhook_subscriptions,
        get_webhook_subscription, get_whoami, get_rate_limit,
        get_current_user, get_companies_v2, get_company_v2, get_company_fields_v2,
        get_company_lists_v2, get_company_list_entries_v2, get_emails, get_lists_v2,
        get_list_v2, get_list_entries_v2, get_list_entry_v2, get_list_entry_fields,
        get_list_entry_field, get_list_fields, get_saved_views, get_saved_view,
        get_saved_view_list_entries, get_opportunities_v2, get_opportunity_v2,
        get_persons_v2, get_person_v2, get_person_fields_v2, get_person_lists,
        get_person_list_entries,
        get_companies, get_company, get_company_by_domain, get_company_funding,
        get_company_people, get_company_news, get_company_metrics, get_company_technologies,
        get_company_competitors, get_company_similar, get_people, get_person_harmonic,
        get_person_by_email, get_person_companies, get_person_investments,
        get_person_network, get_industries, get_industry, get_industry_companies,
        get_funding_rounds, get_funding_round, get_investors, get_investor,
        get_investor_portfolio, get_investor_investments, search_companies,
        search_people, search_investors, get_saved_searches, get_saved_search,
        get_saved_search_results, get_market_analytics, get_industry_analytics,
        get_funding_analytics, get_lists_harmonic, get_list_harmonic, get_list_companies,
        get_alerts, get_alert, get_alert_results,
        format_api_response_tool, validate_pagination_params_tool, build_date_filters_tool,
        search_filter_builder_tool, extract_entity_ids_tool]
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
