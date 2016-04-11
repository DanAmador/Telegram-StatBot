defmodule Fagbot.BotController do
  require Logger
  alias Messages
  alias Stats
  alias Fagbot.Bot
  use Fagbot.Web, :controller
  import Ecto.Changeset

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

	def storeUpdates do
	 	updates = pull_updates
		Enum.each(updates,fn message ->  update_db(message) end)
	end

	
	defp update_db(message) do
		params = message |> Map.from_struct |> fill_message_schema
		if params[:message] != nil do
		Messages.changeset(%Messages{},params) |> Repo.insert
		end
	end
	
	defp fill_message_schema(map_result) do
	value = [from: map_result.message.from.first_name <> " "<> map_result.message.from.last_name,
		chat_id: map_result.message.chat.id, update_id: map_result.update_id,
		date: map_result.message.date, message: map_result.message.text ]

	  value
	end

	defp pull_updates do
	      case Nadia.get_updates do
            {:ok, updates} ->
              if length(updates) > 0  do
				updates
              end
            {:error, %Nadia.Model.Error{reason: err}} ->
              Logger.error("Nadia.get_updates: #{err}")
          end

	end

end
