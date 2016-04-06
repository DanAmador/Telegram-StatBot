defmodule Fagbot.BotController do
  use Fagbot.Web, :controller
  use Ecto.Repo,
    otp_app: :my_app,
    adapter: Mongo.Ecto

  alias Fagbot.Bot


	def get_me(conn, _params) do
	  case Nadia.get_me do
	    {:ok, elems} ->
	    	 json conn, elems
	  end
	end


	def send_message(conn, %{"id" => id, "message" => message}) do
		case Nadia.send_message(id, message) do
		{:ok, message}   ->
			text conn, :ok
		end
	end

	def get_messages(conn, %{"chat_id" => chat_id} )do
#	 messages = Nadia.request("getFullChat", [chat_id: id],nil)
	 messages = "test"
#	 TODO read mongoDB for requested chat id
	 json conn,messages
	end

	def storeUpdates do
	  case Nadia.get_updates  do
	    {:ok, results} ->
	    #TODO Store newest updates to mongo
	    results |> clean_nulls
	    #TODO clean nulls from updates
	  end
	end

	def show_updates(conn,_) do

	  json conn, storeUpdates
	end
end
