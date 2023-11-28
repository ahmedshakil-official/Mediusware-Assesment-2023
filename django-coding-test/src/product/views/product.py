from django.db.models import Prefetch

from django.core.paginator import Paginator

from django.views.generic import ListView, CreateView, UpdateView

from product.filters import ProductFilter
from product.forms import ProductForm, VariantForm, ProductVariantPriceForm, ProductImageForm
from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = '/product/create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
        context['variant_form'] = VariantForm()
        context['product_image_form'] = ProductImageForm()
        context['product_variant_price_form'] = ProductVariantPriceForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variant_form = VariantForm(self.request.POST)
        variant_price_form = ProductVariantPriceForm(self.request.POST)
        image_form = ProductImageForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            self.object = form.save()

            print("Product saved:", self.object)

            if variant_form.is_valid():
                variant = variant_form.save(commit=False)
                variant.product = self.object
                variant.save()

                print("Variant saved:", variant)

            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.product = self.object
                image.save()

                print("Product Image saved:", image)

            return super().form_valid(form)
        else:
            print("Form is not valid:", form.errors)
            return self.render_to_response(self.get_context_data(form=form))


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    filterset_class = ProductFilter

    def get_queryset(self):
        products = Product.objects.prefetch_related('productvariant_set', 'productvariantprice_set').filter()
        return products


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.prefetch_related('productvariant_set', 'productvariantprice_set').filter()
        paginator = Paginator(products, self.paginate_by)

        # filtered_products = self.filterset_class(self.request.GET, queryset=Product.objects.all()).qs
        page = self.request.GET.get('page')
        context['products'] = paginator.get_page(page)
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())

        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update.html'
    success_url = '/product/list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        variant_prices = ProductVariantPrice.objects.filter(product=product)
        context['variant_forms'] = [ProductVariantPriceForm(instance=variant) for variant in variant_prices]
        context['product_form'] = ProductForm(instance=product)
        return context

    def form_valid(self, form):
        product_form = ProductForm(self.request.POST, instance=self.get_object())
        variant_forms = [ProductVariantPriceForm(self.request.POST, instance=variant) for variant in self.get_object().productvariantprice_set.all()]

        if all([product_form.is_valid(), form.is_valid()] + [vf.is_valid() for vf in variant_forms]):
            product_form.save()
            form.save()
            for vf in variant_forms:
                vf.save()
            return super().form_valid(form)
        return self.form_invalid(form)
