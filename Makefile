mig:
	python manage.py makemigrations
upg:
	python manage.py migrate
super:
	python manage.py createsuperuser
load:
	python manage.py loaddata product.json category.json district.json image.json region.json seller.json tag.json option.json attr.json setting.json product_tag.json user.json
dump:
	python manage.py dumpdata apps.User > user.json
celery:
	celery -A root worker --pool=solo -l info
flower:
	celery -A root flower
beat:
	celery -A root beat -l info -S django