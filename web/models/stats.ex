defmodule Stats do
  	use Calendar
	use Ecto.Model
	use Ecto.Repo,
		otp_app: :fagbot,
		adapter: Mongo.Ecto

    @primary_key {:id, :binary_id, autogenerate: true}
    schema "Stats" do
		field :chat_id
		field :chat_name
		field :participants, {:array, :map}
		field :total_messages, :integer, default: 0
		field :total_stickers, :integer, default: 0
		field :date_created
    end


    def get_date do
    {:ok, parsed} =  DateTime.now_utc |> Calendar.Strftime.strftime("%a %d-%m-%y")
    parsed
    end

	def changeset(model, params \\ :empty) do
		model
		|> change(params)
	end
end