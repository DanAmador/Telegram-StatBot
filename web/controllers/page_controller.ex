defmodule Fagbot.PageController do
  use Fagbot.Web, :controller

  def index(conn, _params) do
    render conn, "index.html"
  end
end
