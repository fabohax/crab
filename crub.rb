require 'httparty'

# SIDESHIFT API credentials
SIDESHIFT_API_URL = "https://api.sideshift.ai/v1/"
ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"

# User-defined variables
BUY_AMOUNT_USDT = 100 # USDT amount to purchase Bitcoin with
CURRENCY_PAIR = "BTC_USDT" # BTC/USDT currency pair

# Cron job schedule
CRON_SCHEDULE = "0 0 * * SUN" # Run script every Sunday at midnight

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
exchange_rate = sideshift_api_call("rates/#{CURRENCY_PAIR}")["rate"]

# Calculate Bitcoin amount to purchase based on exchange rate
btc_amount = BUY_AMOUNT_USDT / exchange_rate

# Place Bitcoin purchase order
order_response = sideshift_api_call("orders", method: :post, body: {
  sourceAmount: BUY_AMOUNT_USDT,
  sourceCurrency: "USDT",
  destinationCurrency: "BTC",
  destinationAmount: btc_amount
})

# Print order details
puts "Bitcoin purchase order placed successfully!"
puts "Order ID: #{order_response['orderId']}"
puts "Source amount: #{order_response['sourceAmount']} USDT"
puts "Destination amount: #{order_response['destinationAmount']} BTC"
puts "Exchange rate: #{exchange_rate}"

# Run script with Cron
cron = Cron.new
cron.schedule(CRON_SCHEDULE) do
  system('ruby buy_bitcoin.rb')
end
cron.run
