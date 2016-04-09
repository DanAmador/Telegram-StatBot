defmodule Messages do
  @moduledoc false
  	use Calendar
	use Ecto.Repo,
		otp_app: :fagbot,
		adapter: Mongo.Ecto
	use Ecto.Model

  @primary_key {:id, :binary_id, autogenerate: true}
  schema "messages" do
  	field :chat_id
  	field :chat_name
    field :participants, {:array, :map}
    field :total_messages, :integer, default: 0
    field :total_stickers, :integer, default: 0
  	field :date_created
  end
	  def changeset(model, params \\ %{}) do
        model
        |> change(params)
      end

      def get_date do
      {:ok, parsed} =  DateTime.now_utc  |> Calendar.Strftime.strftime "%a %d-%m-%y"
      parsed
      end
end