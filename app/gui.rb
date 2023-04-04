require 'shoes'
require_relative 'crub'

Shoes.app do
    button "Iniciar Bot" do
      Thread.new do
        run_bot
      end
    end
  end
  