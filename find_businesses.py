import requests
import sys
import argparse

def find_local_businesses(api_key, city, business_type):
    """
    Finds local businesses in a specific city using the Google Places API.

    Args:
        api_key (str): Your Google Places API key.
        city (str): The city to search in.
        business_type (str): The type of business to find (e.g., 'restaurants', 'gyms').

    Returns:
        list: A list of dictionaries containing business details, or None if an error occurs.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{business_type} in {city}"
    params = {
        "query": query,
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        if data.get("status") != "OK":
            if data.get("status") == "ZERO_RESULTS":
                 return []
            print(f"Error from API: {data.get('status')} - {data.get('error_message', '')}", file=sys.stderr)
            return None

        results = data.get("results", [])
        businesses = []
        for place in results:
            business = {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total")
            }
            businesses.append(business)

        return businesses

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Find local businesses using Google Places API.")
    parser.add_argument("api_key", help="Your Google Places API Key")
    parser.add_argument("city", help="City to search in")
    parser.add_argument("business_type", help="Type of business to find (e.g., 'cafe', 'plumber')")

    args = parser.parse_args()

    print(f"Searching for {args.business_type} in {args.city}...")
    businesses = find_local_businesses(args.api_key, args.city, args.business_type)

    if businesses is None:
        sys.exit(1)

    if not businesses:
        print("No businesses found.")
        return

    print(f"\nFound {len(businesses)} businesses:\n")
    for idx, b in enumerate(businesses, 1):
        print(f"{idx}. {b['name']}")
        print(f"   Address: {b['address']}")
        print(f"   Rating: {b['rating']} ({b['user_ratings_total']} reviews)")
        print("-" * 30)

if __name__ == "__main__":
    main()
