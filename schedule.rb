require 'dotenv'
require 'rufus-scheduler'

Dotenv.load

# Configura la zona horaria
Time.zone = 'America/Lima'

# Carga el archivo crub.rb
require_relative 'crub'

# Inicializa el planificador
scheduler = Rufus::Scheduler.new

# Define una tarea que se ejecutará cada 3 días a partir de ahora
scheduler.every '3d', :first_at => Time.now do
  # Compra BTC con 12 USDT
  buy_btc(client, '0.0005', '24000')
end

# Permite que el planificador se ejecute continuamente en segundo plano
scheduler.join