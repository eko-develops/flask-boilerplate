# flask-boilerplate

A basic setup for a Flask application with a SQLite database.

## Initial Database Creation

Creating the inital databases normally occurs during development or when first setting up the server for production. You can use the following command to create the database and tables depending on the models defined with SQLAlchemy:

`flask --app flask_server shell`

Now that we're in the application context, we can use the following command to create the database:

`db.create_all()`

## Running the Application

To run the application, use the following command:

`flask --app flask_server run [--debug]`

This command is telling Flask where to find the application and to run it. Our function that creates the Flask application is named `create_app`, so we do not need to provide the name. The debug command is optional to show an interactive debugger when a page raises an exception, and restarts the server whenever changes to the code are made.

### Debug Flag

The developers of Flask recommend only using the `--debug` flag directly in the command line when running the application. If the `--debug` flag is directly used in the code, _"it can't be read early by the `flask run` command, and some systems or extensions may have already configured themselves based on a previous value."_

## Environment Variables

The configuration is setup to take values from the `.env` file in the root of the project. Here is where you will define the database URI, credentials, secret keys, and other [Flask configuration options](https://flask.palletsprojects.com/en/2.3.x/config/#). They will then be loaded when the application starts. **This file must not be added to version control.**

There are several more options available to setup and load environment variables found in the [documentation](https://flask.palletsprojects.com/en/2.3.x/config/#configuring-from-python-files).

This boilerplate only uses a single environment variable in `.env` to get started, `FLASK_SQLALCHEMY_DATABASE_URI`. Set this to a SQLite URI to get started quick or use any other database that is supported by `SQLAlchemy`.

## Database Migrations

If any changes are made to the database such as new models, change in column names or constraints, etc, a migration will need to be performed to reflect the changes. This Flask boilerplate uses `Flask-Migrate` to create and run migrations.

### How To Perform A Migration (First Migration)

If a migration has never been performed on the database before, we will need to create a migration repository. **This directory should be added to version control**. This directory will be created in the root of the project. Use the following command to create the migrations folder:

`flask --app flask_server db init`

You can then generate the migration using the following command. This does not run the migration, but just creates the migration file. Leave a descriptive message of what has been changed for the migration.

`flask --app flask_server migrate -m "Initial migration"`

_Important Note: The migration script needs to be reviewed and edited, as Alembic is not always able to detect every change you make to your models. In particular, Alembic is currently unable to detect table name changes, column name changes, or anonymously named constraints. A detailed summary of limitations can be found in the Alembic autogenerate documentation. Once finalized, the migration script also needs to be added to version control._

Once the migration script has been reviewed and edited if needed, you can run the final command to apply the migration:

`flask --app flask_server upgrade`

### Repeat Migrations

If you have already ran a migration once, use only the `migrate` and `upgrade` commands when the database models change.

### Sync Database In Another System

To sync the database in another system, pull the migrations folder from version control and run the `upgrade` command.

## Dependencies

[Python 3.11.5](https://docs.python.org/release/3.11.5/whatsnew/changelog.html#python-3-11-5)  
[Flask 2.3.3](https://flask.palletsprojects.com/en/2.3.x/)  
[python-dotenv 1.0.0](https://github.com/theskumar/python-dotenv#readme)  
[Flask-SQLAlchemy 3.0.5](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

- [Result Methods (all(), scalars(), etc)](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)

[Flask-Migrate 4.0.4](https://flask-migrate.readthedocs.io/en/latest/#)

## Todo

- [Handle multiple configuration files](https://flask.palletsprojects.com/en/2.3.x/config/#development-production)
  - Default
  - Development
  - Production
