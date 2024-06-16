from orm.models import Model


class Product(Model):

    id: int
    name: str
    description: str

    __db_table__ = 'product'


if __name__ == '__main__':
    print(Product.objects.all())
