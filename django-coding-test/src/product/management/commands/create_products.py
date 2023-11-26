import random
from django.core.management.base import BaseCommand
from product.models import Product, ProductVariant, Variant, ProductVariantPrice


class Command(BaseCommand):
    help = 'Create 50 Products with product variants and variant prices'

    def handle(self, *args, **options):
        for _ in range(50):
            product = Product.objects.create(
                title=f"Product {_}",
                sku=f"SKU{_}",
                description=f"Description for Product {_}"
            )

            for variant_num in range(3):
                variant = Variant.objects.get(id=variant_num + 1)
                product_variant = ProductVariant.objects.create(
                    variant_title=f"Variant {variant_num + 1}",
                    variant=variant,
                    product=product
                )

                for _ in range(2):
                    price = random.uniform(10, 100)
                    stock = random.randint(0, 50)
                    ProductVariantPrice.objects.create(
                        product_variant_one=product_variant,
                        price=price,
                        stock=stock,
                        product=product
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 Products with variants and prices.'))