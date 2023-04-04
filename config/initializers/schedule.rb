require 'dotenv'
require 'rufus-scheduler'

Dotenv.load

Time.zone = 'America/Lima'

require_relative 'crub'

scheduler = Rufus::Scheduler.new

scheduler.every '3d', :first_at => Time.now do

  response = HTTParty.post('https://sideshift.ai/api/v1/swap', 
  body: {
    from: 'usdtErc20',
    to: 'BTC',
    address: '0x1234567890123456789012345678901234567890', # replace with your own receiving address
    refundAddress: '1BitcoinAddress', # replace with your own refund address
    apiKey: ENV['SIDESHIFT_API_KEY'], # replace with your own API key
    amount: 0.01 # replace with the amount you want to swap
  }
  )

  puts response.body, response.code, response.message, response.headers.inspect

end

scheduler.join