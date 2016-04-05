defmodule Fagbot.BotController do
  use Fagbot.Web, :controller

  alias Fagbot.Bot

	def get_me(conn, _params) do
	  info = elem(Nadia.get_me,1)
	  case Nadia.get_me do
	    {:ok, elems} ->
	    	 json conn, elems
	  end
	end
	

end
