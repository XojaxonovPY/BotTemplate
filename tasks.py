from invoke import task

@task
def extract(c):
    c.run("pybabel extract --input-dirs=. -o locales/messages.pot")

@task
def init_uz(c):
    c.run("pybabel init -i locales/messages.pot -d locales -D messages -l uz")

@task
def init_ru(c):
    c.run("pybabel init -i locales/messages.pot -d locales -D messages -l ru")

@task
def compile(c):
    c.run("pybabel compile -d locales -D messages")

@task
def update(c):
    c.run("pybabel update -d locales -D messages -i locales/messages.pot")

@task
def webs(c):
    c.run("uvicorn web.app:app --host localhost --port 8005")

@task
def mig(c):
    c.run('alembic revision --autogenerate -m "Create a baseline migrations"')

@task
def upgrade(c):
    c.run("alembic upgrade head")

@task
def downgrade(c):
    c.run("alembic downgrade head")

@task
def alembic_init(c):
    c.run("alembic init migrations")