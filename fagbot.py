from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')


if __name__ == '__main__':
    app.run()
