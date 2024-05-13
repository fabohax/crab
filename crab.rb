require 'httparty'
require 'dotenv/load' # Load environment variables from .env file

# SIDESHIFT API credentials
SIDESHIFT_API_URL = "https://api.sideshift.ai/v1/"
ACCESS_KEY = ENV['SIDESHIFT_ACCESS_KEY']
SECRET_KEY = ENV['SIDESHIFT_SECRET_KEY']

# User-defined variables
BUY_AMOUNT_USDT = 100 # USDT amount to purchase Bitcoin with
CURRENCY_PAIR = "BTC_USDT" # BTC/USDT currency pair

# Helper function to make API calls
def sideshift_api_call(path, method: :get, body: nil)
  headers = {
    "Authorization" => "Bearer #{ACCESS_KEY}:#{SECRET_KEY}",
    "Content-Type" => "application/json"
  }

  response = HTTParty.send(method, "#{SIDESHIFT_API_URL}#{path}", headers: headers, body: body.to_json)
  raise "API Error: #{response.body}" unless response.success?

  response.parsed_response
end

# Fetch Bitcoin exchange rate
def fetch_exchange_rate(currency_pair)
  sideshift_api_call("rates/#{currency_pair}")["rate"]
end

# Place Bitcoin purchase order
def place_order(source_currency, destination_currency, source_amount)
  btc_amount = source_amount / fetch_exchange_rate("#{destination_currency}_#{source_currency}")

  order_response = sideshift_api_call("orders", method: :post, body: {
    sourceAmount: source_amount,
    sourceCurrency: source_currency,
    destinationCurrency: destination_currency,
    destinationAmount: btc_amount
  })

  order_response
end

# Print order details
def print_order_details(order_response, exchange_rate)
  puts "Bitcoin purchase order placed successfully!"
  puts "Order ID: #{order_response['orderId']}"
  puts "Source amount: #{order_response['sourceAmount']} #{order_response['sourceCurrency']}"
  puts "Destination amount: #{order_response['destinationAmount']} #{order_response['destinationCurrency']}"
  puts "Exchange rate: #{exchange_rate}"
end

# Main function to execute trading strategy
def execute_strategy
  exchange_rate = fetch_exchange_rate(CURRENCY_PAIR)
  order_response = place_order("USDT", "BTC", BUY_AMOUNT_USDT)
  print_order_details(order_response, exchange_rate)
end

# Run trading strategy
execute_strategy
