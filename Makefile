mig:
	python manage.py makemigrations
upg:
	python manage.py migrate
admin:
	 python manage.py  createsuperuser
apps:
	 python manage.py startapp apps

dump:
	python manage.py dumpdata apps.ProductImage > images.json

load:
	 python manage.py loaddata products.json categories.json disdricts.json images.json regions.json sellers.json tags.json options.json attrs.json settings.json
celery:
		celery -A DjangoMarket worker --pool=solo -l info
flower:
	celery -A DjangoMarket flower


beat:
	celery -A DjangoMarket beat -l info -S django