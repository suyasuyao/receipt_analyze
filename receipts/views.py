from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Receipt

"""
Django Auth

The LoginRequired mixin
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-loginrequired-mixin

The login_required decorator
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
@login_required
"""
# Create your views here.

class IndexView2(generic.ListView):
    model = Receipt
    paginate_by = 5
    ordering = ['-updated_at']
    template_name = 'receipt/receipt_list.html'

    # def get_queryset(self):
    #     userid = self.request.user
    #     return Receipt.objects.filter(author_id=userid)


class UpdateView2(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Receipt
    fields = ['title', 'text']  # '__all__'

    success_url = reverse_lazy('receipts:index2')

    template_name = 'receipt/receipt_form.html'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super(UpdateView2, self).dispatch(request, *args, **kwargs)


class DetailView2(generic.DetailView):
    model = Receipt
    template_name = 'receipt/receipt_detail.html'


class CreateView2(LoginRequiredMixin, generic.edit.CreateView):  # The LoginRequired mixin
    model = Receipt
    fields = ['title', 'text']  # '__all__'
    success_url = reverse_lazy('receipts:index2')

    template_name = 'receipt/receipt_form.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        return super(CreateView2, self).form_valid(form)


class DeleteView2(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Receipt
    success_url = reverse_lazy('receipts:index2')

    template_name = 'receipt/receipt_confirm_delete.html'
    # receipts/post_confirm_delete.html

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')

        return super(DeleteView2, self).dispatch(request, *args, **kwargs)
