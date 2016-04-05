defmodule Fagbot.BotView do
  use Fagbot.Web, :view

  def render("index.json", %{bots: bots}) do
    %{data: render_many(bots, Fagbot.BotView, "bot.json")}
  end

  def render("show.json", %{bot: bot}) do
    %{data: render_one(bot, Fagbot.BotView, "bot.json")}
  end

  def render("bot.json", %{bot: bot}) do
    %{id: bot.id}
  end
end
