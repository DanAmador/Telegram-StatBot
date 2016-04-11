defmodule Fagbot.BotController do
  alias Fagbot.Bot
  use Fagbot.Web, :controller

	def get_me(conn, _params) do
	  case Nadia.get_me do
	    {:ok, elems} ->
	    	 json conn, elems
	  end
	end


	def send_message(conn, %{"id" => id, "message" => message}) do
		case Nadia.send_message(id, message) do
		{:ok, message}   ->
			text conn, message
		end
	end

	def get_messages(conn, %{"chat_id" => chat_id} )do
	 messages = "test"
#	 TODO read mongoDB for requested chat id
	 json conn,messages
	end
end
