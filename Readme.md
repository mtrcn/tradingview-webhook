# TradingView Webhook API

This flask-based web application that integrates with cryptocurrency exchanges (e.g., Coinbase) to execute buy/sell orders via TradkingView webhooks, so alerts can be easily converted into orders.

## Features

- **Webhook Integration**: Accepts trading signals from external sources (e.g., TradingView) via webhooks.
- **Exchange Support**: Uses the Strategy Pattern to support multiple cryptocurrency exchanges (e.g., Coinbase, Binance).
- **Dockerized**: Easily deployable using Docker.
- **Environment Variables**: Securely manages API keys and secrets using .env files.
- **Logging**: Detailed logging for debugging and monitoring.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.9+**: [Install Python](https://www.python.org/downloads/)
- **Coinbase API Keys**: Obtain API keys and secrets from your Coinbase account.
- **TradingView Webhook**: Set up a webhook in TradingView to send trading signals. This requies minimum Essential package on TradingView website.

### 2. Create a .env File

Currently, this only support Coinbase, thus `.env` file has only configuration for Coinbase account.

Create a `.env` file in the project root directory and add the following environment variables:

```env
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
MIN_BALANCE=10
WEBHOOK_SECRET=your_webhook_secret
```

Replace the placeholders with your actual values.

### 3. Build the Docker Image

Build the Docker image for the application:

```bash
docker build -t tradingview-webhook-api .
```

### 4. Run the Docker Container

Run the container and map port 5000:

```bash
docker run -p 8000:8000 --env-file .env tradingview-webhook-api
```

The application will be available at http://localhost:8000.

## Usage

### Webhook Endpoint

The application exposes a `/webhook` endpoint to accept trading signals. Send a POST request to this endpoint with the following JSON payload:

```json
{
  "secret": "your_webhook_secret",
  "action": "buy",
  "symbol": "BTC-USDC",
  "exchange": "coinbase"
}
```

**Fields**:
- `secret`: The webhook secret (must match WEBHOOK_SECRET in .env).
- `action`: The trading action (buy or sell).
- `symbol`: The trading pair (e.g., BTC-USDC).
- `exchange`: The exchange to use (e.g., coinbase).

**Example cURL Request**:
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
        "secret": "your_webhook_secret",
        "action": "buy",
        "symbol": "BTC-USDC",
        "exchange": "coinbase"
      }'
```

Enjoy trading! 🚀