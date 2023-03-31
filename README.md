# crub

The bot script is a program written in Ruby that utilizes the OKEx API to access and analyze financial data related to cryptocurrency trading.

It includes functions such as obtaining market data, managing user accounts, and placing trades based on Dollar-Cost Averaging (DCA) strategy. The script is designed to run automatically at specified intervals using a scheduler, with the aim of optimizing trading strategies and generating profits.

## Installation

1. Clone the repository:

  `git clone https://github.com/your-username/your-repo.git`

2. Install the required gems:

  `bundle install`
  
3. Create a .env file in the root directory of the project and add the following variables with your own credentials:

  ``OKEX_API_KEY=your_api_key
  OKEX_SECRET_KEY=your_secret_key
  OKEX_PASSPHRASE=your_passphrase``
  
4. Modify the bot.rb file to suit your trading strategy.

5. Set up the cron job to run the script at your desired intervals. For example, to run the script every 5 minutes:

  `*/5 * * * * cd /path/to/project && ruby bot.rb`

6. Start the cron job:

  `sudo service cron start`
 
7. Verify that the cron job is running:

  `sudo service cron status`
  
  That's it! Crub should now be up and running, executing your trading strategy on the OKEx platform.
  
  
  

**[!]**

**Warning: Use at Your Own Risk**

<em>This script is designed to automate trading activities in the cryptocurrency market. However, the use of bots for trading carries inherent risks and uncertainties, and there is no guarantee that the bot will perform as intended or generate profits. 

Before using this script, it is important to understand the risks involved with trading cryptocurrencies, including market volatility, liquidity risks, and potential regulatory and legal issues. 

Furthermore, it is recommended that you thoroughly test the bot in a simulated trading environment before using it with real funds. It is also important to monitor the bot's performance regularly and adjust its parameters as needed.

The creators of this script are not responsible for any losses or damages that may occur as a result of using the bot, and by using it, you acknowledge and accept all risks associated with cryptocurrency trading.</em>





