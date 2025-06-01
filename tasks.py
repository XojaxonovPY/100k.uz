from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def superuser(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp apps")


@task
def load(c):
    c.run("python manage.py loaddata products.json categories.json disdricts.json images.json regions.json sellers.json tags.json options.json attrs.json settings.json")


@task
def dump(c):
    c.run("python manage.py dumpdata apps.ProductImage > images.json")


@task
def celery(c):
    c.run("celery -A DjangoMarket worker --pool=solo -l info")


@task
def flower(c):
    c.run("celery -A DjangoMarket flower")


@task
def beat(c):
    c.run("celery -A DjangoMarket beat -l info -S django")
