# Google Places Business Finder

A Python script to find local businesses in a specific city using the Google Places API.

## Prerequisites

- Python 3.x
- A Google Cloud Project with the **Places API (New)** or **Places API** enabled.
- An API Key from Google Cloud.

## Installation

1.  **Clone the repository** (if you haven't already).
2.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from the command line:

```bash
python find_businesses.py "YOUR_API_KEY" "City Name" "business_type"
```

### Example

```bash
python find_businesses.py "AIzaSy..." "New York" "pizza"
```

## Testing

### Unit Tests
The project includes unit tests that mock the Google Places API responses, so you don't need a real API key to run them.

To run the tests:

```bash
python -m unittest test_find_businesses.py
```

### Manual Testing
To manually test the script, you will need a valid Google Places API key. Run the script as shown in the **Usage** section and verify the output matches your expectations (e.g., lists pizza places in New York).
