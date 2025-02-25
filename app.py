from flask import Flask, request, jsonify
import json, os, logging
from dotenv import load_dotenv
from coinbase_strategy import CoinbaseStrategy
from trading_context import TradingContext

application = Flask(__name__)

load_dotenv()
# Load Coinbase API credentials from environment variables
MIN_BALANCE = os.getenv('MIN_BALANCE')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

@application.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_data(as_text=True)
        payload = json.loads(data)
        
        secret = payload.get('secret')
        action = payload.get('action')
        symbol = payload.get('symbol')
        exchange = payload.get('exchange', 'coinbase')  # Default to Coinbase if not specified

        buy_symbol = symbol.split('-')[0]
        sell_symbol = symbol.split('-')[1]

        logging.info(f"Received webhook for action: {action}, symbol: {symbol}, exchange: {exchange}")

        # Initialize the appropriate exchange strategy
        if exchange == 'coinbase':
            strategy = CoinbaseStrategy()
        else:
            return jsonify({"error": "Unsupported exchange"}), 400

        context = TradingContext(strategy)

        # Fetch wallet information
        wallets = context.get_wallets()
        product_wallet = None
        base_wallet = None
        for wallet in wallets:
            if wallet['currency'] == sell_symbol:
                base_wallet = wallet
            if wallet['currency'] == buy_symbol:
                product_wallet = wallet

        logging.info(f"Base wallet: {base_wallet}")
        logging.info(f"Product wallet: {product_wallet}")

        if secret != WEBHOOK_SECRET:
            return jsonify({"error": "Invalid secret"}), 401

        if base_wallet is None:
            return jsonify({"error": "Base wallet not found"}), 400

        total_balance = float(base_wallet['available_balance']['value'])
        if total_balance < MIN_BALANCE and action == 'buy':
            return jsonify({"error": f"Insufficient balance to trade. Current balance: {total_balance}"}), 400

        if action == 'buy':
            amount = round(total_balance * .98, 2)
            order = context.buy(symbol, amount)
            logging.info(f"Buy Order: {order}")            

            return jsonify({"success": order['success']}), 200
        elif action == 'sell':
            if product_wallet is None:
                return jsonify({"error": "Product wallet not found"}), 400
            quantity_of_asset = float(product_wallet['available_balance']['value'])
            order = context.sell(symbol, quantity_of_asset)
            logging.info(f"Sell Order: {order}")           

            return jsonify({"success": order['success']}), 200
        else:
            return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        logging.error(f"Error in webhook call: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    application.run(port=5000)