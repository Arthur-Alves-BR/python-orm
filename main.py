from typing import Optional

from orm.model import Model


class Product(Model):

    id: int
    name: str
    description: Optional[str] = None

    __db_table__ = 'product'


if __name__ == '__main__':
    products = Product.objects.all()
    print(products)
    # print(Product.objects.create(name='teste'))
