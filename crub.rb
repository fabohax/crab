require 'okex-api'
require 'dotenv'
require 'rufus-scheduler'

Dotenv.load

# Initialize API client with environment variables
client = Okex::Client.new(api_key: ENV['API_KEY'], api_secret: ENV['API_SECRET'], api_passphrase: ENV['API_PASSPHRASE'], instrument_id: ENV['INSTRUMENT_ID'])

# Define a scheduler that runs every 15 seconds
scheduler = Rufus::Scheduler.new
scheduler.every '15s' do
  # Get ticker data
  ticker = client.ticker

  # Print ticker data to console
  puts "Ticker data: #{ticker}"
end

# Keep the script running
loop do
  sleep 1
end
