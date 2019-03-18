from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Receipt

from PIL import Image
import numpy as np
import requests
import json
import base64
import cv2

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


class UpdateView2(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Receipt
    fields = ['title', 'text', 'image']  # フォームに表示するカラム

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
    fields = ['title', 'text', 'image']  # フォームに表示するカラム
    success_url = reverse_lazy('receipts:index2')

    template_name = 'receipt/receipt_form.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        analyze_imgage = form.cleaned_data['image']
        analyze_json = text_detection(analyze_imgage)
        description = analyze_json['responses'][0]['textAnnotations'][0]['description']
        form.instance.text = description

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


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        analyze_imgage = form.cleaned_data['image']
        analyze_json = text_detection(analyze_imgage)
        description = analyze_json['responses'][0]['textAnnotations'][0]['description']
        form.instance.text = description

        return super(C2, self).form_valid(form)


def text_detection(image_path):
    # 注意
    API_KEY = "AIzaSyAj9Gwi_5JkYkgyZp-NiLPRvW57BK9gq7Q"
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)

    immage_array = np.asarray(Image.open(image_path))

    result, dst_data = cv2.imencode('.jpg', immage_array)
    image_content = base64.b64encode(dst_data)

    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content.decode('utf-8')  # base64でエンコードしたものjsonにするためdecodeする
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()
