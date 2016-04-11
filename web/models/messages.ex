defmodule Messages do
	use Ecto.Model
	use Ecto.Repo,
		otp_app: :fagbot,
		adapter: Mongo.Ecto

	@primary_key {:id, :binary_id, autogenerate: true}
	    schema "Messages" do
    		field :from
    		field :chat_id, :integer, default: 0
    		field :update_id, :integer, default: 0
    		field :date, :integer, default: 0
			field :message
        end

	def changeset(model, params \\ :empty) do
		model
		|> change(params)
	end
end