<img src="https://bafybeib2q3dv22gkf5jc5vamy653jsvqkvek4ulmqu6ynrmjzlv64zbpde.ipfs.w3s.link/crub.svg" alt="crub" height="180" style="margin:0;"/>

# crab

<b>crab</b> is a bot written in Ruby that utilizes the [SIDESHIFT API](https://documenter.getpostman.com/view/6895769/TWDZGvjd) to access and analyze financial data related to cryptocurrency trading.

It includes functions such as obtaining market data, managing user accounts, and placing trades based on [Dollar-Cost Averaging](https://www.investopedia.com/terms/d/dollarcostaveraging.asp) (DCA) strategy. The script is designed to run automatically at specified intervals using a scheduler, with the aim of optimizing trading strategies and generating profits.

## Installation

1. Clone the repository:

  ```
  git clone https://github.com/fabohax/crab.git
  ```0 * * * * cd /path/to/project && ruby crab.rb

2. Install the required gems:

  ```
  bundle install
  ```
  
3. Modify the crub.rb file to suit your trading strategy. Now is intended to buy 100 USDT of Bitcoin every sunday at 0:00 h.

4. Set up the cron job to run the script at your desired intervals. For example, to run the script every 5 minutes:

  ```
  0 * * * * cd /path/to/project && ruby crab.rb
  ```

5. Start the cron job:

  ```
  sudo service cron start
  ```
 
7. Verify that the cron job is running:

  ```
  sudo service cron status
  ```
  
  That's it! Crub should now be up and running, executing your trading strategy on [SIDESHIFT.AI](https://sideshift.ai)
  

# **[!] Warning: Use at Your Own Risk**

<em>This script is designed to automate trading activities in the cryptocurrency market. However, the use of bots for trading carries inherent risks and uncertainties, and there is no guarantee that the bot will perform as intended or generate profits. 

Before using this script, it is important to understand the risks involved with trading cryptocurrencies, including market volatility, liquidity risks, and potential regulatory and legal issues. 

Furthermore, it is recommended that you thoroughly test the bot in a simulated trading environment before using it with real funds. It is also important to monitor the bot's performance regularly and adjust its parameters as needed.

The creators of this script are not responsible for any losses or damages that may occur as a result of using the bot, and by using it, you acknowledge and accept all risks associated with cryptocurrency trading.</em>

