# Google Maps Scraper API

A FastAPI-based web service for scraping business information from Google Maps.

## Features

- Scrape business information from Google Maps
- Extract contact details including emails and phone numbers
- Visit business websites for additional contact information
- RESTful API with JSON responses
- CORS enabled for web applications

## API Endpoints

### GET /
Returns basic API information and status.

### GET /health
Health check endpoint for monitoring.

### POST /scrape
Main scraping endpoint.

**Request Body:**
```json
{
  "query": "restaurants in New York",
  "max_results": 100,
  "visit_websites": true
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Business Name",
      "address": "Business Address",
      "rating": 4.5,
      "review_count": 123,
      "category": "Restaurant",
      "website": "https://example.com",
      "mobile": "(555) 123-4567",
      "email": "contact@example.com",
      "secondary_email": "info@example.com",
      "google_maps_url": "https://maps.google.com/...",
      "search_query": "restaurants in New York",
      "website_visited": true,
      "additional_contacts": "{...}"
    }
  ],
  "total_results": 1,
  "message": "Successfully scraped 1 businesses"
}
```

## Deployment

This service is designed to be deployed on Railway.com with the following files:
- `Procfile`: Defines the web process
- `requirements.txt`: Python dependencies
- `railway.json`: Railway-specific configuration
- `runtime.txt`: Python version specification

## Usage

1. Deploy to Railway.com
2. Send POST requests to `/scrape` endpoint with your search query
3. Receive structured business data in JSON format

## Environment Variables

- `PORT`: Port number (automatically set by Railway)

## Rate Limiting

The scraper includes built-in rate limiting to avoid being blocked by Google Maps.
