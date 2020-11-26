from website import create_app
import config as configuration

app = create_app()


if __name__ == "__main__":
    app.run(debug=configuration.Development)
