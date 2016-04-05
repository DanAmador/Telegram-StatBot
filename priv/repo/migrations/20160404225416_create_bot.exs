defmodule Fagbot.Repo.Migrations.CreateBot do
  use Ecto.Migration

  def change do
    create table(:bots) do

      timestamps
    end

  end
end
