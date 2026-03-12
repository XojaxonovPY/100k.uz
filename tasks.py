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
    c.run(
        "python manage.py loaddata product.json category.json district.json image.json region.json seller.json tag.json option.json attr.json setting.json product_tag.json user.json")


@task
def dump(c):
    c.run("python manage.py dumpdata apps.Product > user.json")


@task
def celery(c):
    c.run("celery -A root worker --pool=solo -l info")


@task
def flower(c):
    c.run("celery -A root flower")


@task
def beat(c):
    c.run("celery -A root beat -l info -S django")
