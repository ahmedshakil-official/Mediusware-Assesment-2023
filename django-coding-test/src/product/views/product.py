from django.db.models import Prefetch

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import generic
from django.views.generic import ListView

from product.filters import ProductFilter
from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    filterset_class = ProductFilter

    def get_queryset(self):
        products = Product.objects.prefetch_related('productvariant_set', 'productvariantprice_set').all()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.prefetch_related('productvariant_set', 'productvariantprice_set').all()
        paginator = Paginator(products, self.paginate_by)

        filtered_products = self.filterset_class(self.request.GET, queryset=Product.objects.all()).qs
        page = self.request.GET.get('page')
        context['products'] = paginator.get_page(page)
        context['filter'] = self.filterset_class(self.request.GET, queryset=Product.objects.all())
        context['filter_form'] = context['filter'].form

        return context
