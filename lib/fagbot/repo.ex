defmodule Fagbot.Repo do
  use Ecto.Repo, otp_app: :fagbot, adapter: Mongo.Ecto
end
