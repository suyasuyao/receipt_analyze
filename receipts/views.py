from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Receipt
from .forms import ReceiptModelForm

import numpy as np
import requests
import json
import base64

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
        # analyze_imgage = form.cleaned_data['image']
        # immage_array = np.asarray(Image.open(analyze_imgage)
        # image_path = form.instance.image.path
        # analyze_text = text_detection(image_path)
        # print(image_path)
        # print(analyze_text)
        # form.instance.sum_total()
        #        form.instance.sum_total = 3333

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


def text_detection(image_path):
    API_KEY = "AIzaSyAD2HjhCEDFEIETt78Ak3UQf2dlVnND_CY"
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)
    with open(image_path, "rb") as img:
        image_content = base64.b64encode(img.read())
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

    # if __name__ == "__main__":
    #     img_path = "画像のpath"
    #     res_json = text_detection(img_path)
    #     res_text = res_json["responses"][0]["textAnnotations"][0]["description"]
    #     # print(json.dumps(res_json, indent=4, sort_keys=True, ensure_ascii=False))
    #     print(res_text)
    #     with open("result.json", "w") as js:
    #         # json.dump(res_json, js, indent=4, ensure_ascii=False)
    #         js.write(res_text)

#
# class Upload(generic.CreateView):
#     model = Receipt
#     form_class = ReceiptModelForm
#     success_url = '/receipt'
