<img src="https://bafybeib2q3dv22gkf5jc5vamy653jsvqkvek4ulmqu6ynrmjzlv64zbpde.ipfs.w3s.link/crub.svg" alt="crub" height="180" style="margin:0;"/>

# crab

**crab** is a Ruby-based bot that leverages the [SIDESHIFT API](https://docs.sideshift.ai/endpoints/v2/coins) to access and analyze financial data for cryptocurrency trading.

It includes functionalities such as fetching market data, managing user accounts, and executing trades using the [Dollar-Cost Averaging](https://www.investopedia.com/terms/d/dollarcostaveraging.asp) (DCA) strategy. The script is designed to automate these processes at specified intervals using a scheduler, aiming to optimize trading strategies and potentially generate profits.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/fabohax/crab.git
   ```

2. Install required gems:

   ```
   bundle install
   ```

3. Customize the `crub.rb` file to align with your specific trading strategy. For example, to purchase 100 USDT worth of Bitcoin every Sunday at 0:00:

   ```ruby
   0 * * * * cd /path/to/project && ruby crab.rb
   ```

4. Set up a cron job to execute the script at your desired intervals. For instance, to run the script every 5 minutes:

   ```
   */5 * * * * cd /path/to/project && ruby crab.rb
   ```

5. Start the cron service:

   ```
   sudo service cron start
   ```

6. Verify the cron job status:

   ```
   sudo service cron status
   ```

Now, **crub** should be operational, executing your defined trading strategy on [SIDESHIFT.AI](https://sideshift.ai).

# **[!] Warning: Use at Your Own Risk**

*Before deploying this script, it is crucial to understand the risks associated with cryptocurrency trading, including market volatility, liquidity risks, and regulatory challenges.*

*It is strongly recommended to thoroughly test the bot in a simulated environment before using real funds. Regularly monitor its performance and adjust parameters as necessary.*
