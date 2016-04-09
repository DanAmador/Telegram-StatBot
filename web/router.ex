defmodule Fagbot.Router do
  use Fagbot.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", Fagbot do
    pipe_through :browser # Use the default browser stack

    get "/", PageController, :index
  end

   scope "/api", Fagbot do
 	resources "/bots", BotController, except: [:new, :edit]

     pipe_through :api
     get "/me", BotController, :get_me
	 post "/message", BotController, :send_message
	 get "/message", BotController, :get_messages
	 get "/updates", BotController, :show_updates
	 get "/test", BotController, :test
   end
end
