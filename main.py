from flask import Flask
from health import health_blueprint
from csr import csr_blueprint
from cronjob import scheduler

app = Flask(__name__)


def main():
    app.config.from_prefixed_env()
    app.register_blueprint(health_blueprint)
    app.register_blueprint(csr_blueprint)
    scheduler.start()
    scheduler.print_jobs()
    app.run(debug=True)


if __name__ == '__main__':
    main()
