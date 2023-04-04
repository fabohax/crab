require 'httparty'
require 'dotenv'
require 'rufus-scheduler'
require 'logger'

response = HTTParty.get('https://sideshift.ai/api/v1/market-info')
puts response.body, response.code, response.message, response.headers.inspect

Dotenv.load
okex_client = OKEX::Client.new(api_key: ENV['OKEX_API_KEY'], api_secret: ENV['OKEX_API_SECRET'], api_passphrase: ENV['OKEX_API_PASSPHRASE'])
sideshift_client = SideshiftAPI::Client.new(api_key: ENV['SIDESHIFT_API_KEY'], api_secret: ENV['SIDESHIFT_API_SECRET'])

scheduler = Rufus::Scheduler.new
scheduler.every '15s' do
  ticker = okex_client.ticker
  puts "OKEX Ticker data: #{ticker}"
end

def run_sideshift_bot(client)
  logger = Logger.new('sideshift_logfile.log')
  logger.datetime_format = '%Y-%m-%d %H:%M:%S'
  logger.info("#{Time.now.strftime(logger.datetime_format)}: Running crub...")
  
  # SIDESHIFT bot code
end

loop do
  sleep 1
  run_sideshift_bot(sideshift_client)
end
