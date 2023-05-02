from django.contrib import admin
from django.conf import settings

# Register your models here.
from .models import MyModel
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
# from DeepImageSearch import Index,LoadData,SearchImage
from DeepImageSearch import Load_Data, Search_Setup
from myapp.views import mysearch_setup

class adminMyModel(ExtraButtonsMixin,admin.ModelAdmin):

    list_display = ("img_preview","text",)
    readonly_fields = ['img_preview']

    @button(html_attrs={'style': 'background-color:#DC6C6C;color:black'},label=('Train Model'))
    def confirm(self, request):
        image_list = Load_Data().from_folder(['.'+settings.MEDIA_URL+'images'])
        def _action(request):
            # st=Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
            st=mysearch_setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
            st.run_index_train()
            pass

        return confirm_action(self, request, _action, "Do you want to train the model?",
                          "Images are successfully trained", template='admin_extra_button/confirm.html')


    
admin.site.register(MyModel,adminMyModel)