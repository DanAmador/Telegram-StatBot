defmodule Fagbot.BotControllerTest do
  use Fagbot.ConnCase

  alias Fagbot.Bot
  @valid_attrs %{}
  @invalid_attrs %{}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  test "lists all entries on index", %{conn: conn} do
    conn = get conn, bot_path(conn, :index)
    assert json_response(conn, 200)["data"] == []
  end

  test "shows chosen resource", %{conn: conn} do
    bot = Repo.insert! %Bot{}
    conn = get conn, bot_path(conn, :show, bot)
    assert json_response(conn, 200)["data"] == %{"id" => bot.id}
  end

  test "does not show resource and instead throw error when id is nonexistent", %{conn: conn} do
    assert_error_sent 404, fn ->
      get conn, bot_path(conn, :show, -1)
    end
  end

  test "creates and renders resource when data is valid", %{conn: conn} do
    conn = post conn, bot_path(conn, :create), bot: @valid_attrs
    assert json_response(conn, 201)["data"]["id"]
    assert Repo.get_by(Bot, @valid_attrs)
  end

  test "does not create resource and renders errors when data is invalid", %{conn: conn} do
    conn = post conn, bot_path(conn, :create), bot: @invalid_attrs
    assert json_response(conn, 422)["errors"] != %{}
  end

  test "updates and renders chosen resource when data is valid", %{conn: conn} do
    bot = Repo.insert! %Bot{}
    conn = put conn, bot_path(conn, :update, bot), bot: @valid_attrs
    assert json_response(conn, 200)["data"]["id"]
    assert Repo.get_by(Bot, @valid_attrs)
  end

  test "does not update chosen resource and renders errors when data is invalid", %{conn: conn} do
    bot = Repo.insert! %Bot{}
    conn = put conn, bot_path(conn, :update, bot), bot: @invalid_attrs
    assert json_response(conn, 422)["errors"] != %{}
  end

  test "deletes chosen resource", %{conn: conn} do
    bot = Repo.insert! %Bot{}
    conn = delete conn, bot_path(conn, :delete, bot)
    assert response(conn, 204)
    refute Repo.get(Bot, bot.id)
  end
end
