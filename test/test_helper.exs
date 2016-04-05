ExUnit.start

Mix.Task.run "ecto.create", ~w(-r Fagbot.Repo --quiet)
Mix.Task.run "ecto.migrate", ~w(-r Fagbot.Repo --quiet)
Ecto.Adapters.SQL.begin_test_transaction(Fagbot.Repo)

