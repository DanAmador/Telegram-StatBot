defmodule Fagbot.BotTest do
  use Fagbot.ModelCase

  alias Fagbot.Bot

  @valid_attrs %{}
  @invalid_attrs %{}

  test "changeset with valid attributes" do
    changeset = Bot.changeset(%Bot{}, @valid_attrs)
    assert changeset.valid?
  end

  test "changeset with invalid attributes" do
    changeset = Bot.changeset(%Bot{}, @invalid_attrs)
    refute changeset.valid?
  end
end
