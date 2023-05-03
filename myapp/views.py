import time
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageUploadForm
from django.http import HttpResponse, JsonResponse
# from DeepImageSearch import Index,LoadData,SearchImage
from DeepImageSearch import Load_Data, Search_Setup
import DeepImageSearch.config as config
from .models import Image,MyModel,WebcamImage



class mysearch_setup(Search_Setup):
    def run_index_train(self):
        """
        Indexes the images in the image_list and creates an index file for fast similarity search.
        """


        data = self._start_feature_extraction()
        self._start_indexing(data)
        self.image_data = pd.read_pickle(config.image_data_with_features_pkl(self.model_name))
        self.f = len(self.image_data['features'][0])

    def run_index_output(self):

        print("\033[93m Meta data already Present, Please Apply Search!")
        print(os.listdir(f'metadata-files/{self.model_name}'))
        self.image_data = pd.read_pickle(config.image_data_with_features_pkl(self.model_name))
        self.f = len(self.image_data['features'][0])
# Create your views here.

@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        try:
            print("hi")
            print("request.POST",request.POST)
            print("request.FILES",request.FILES)
            form = ImageUploadForm(request.POST, request.FILES)
            uploaded_file = request.FILES.get('file')
            print("form",uploaded_file)
            if form.is_valid():
                form.save()
            st =Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
            imgurl=Search_Setup.get_similar_images(image_path='media/user_images/'+str(uploaded_file),number_of_images=5)
            print("url",imgurl)
            image_data_list = []
            for i in imgurl.values():
                print(i.split('/')[2])
                image_data_list.append('images/'+i.split('/')[3])
            print(image_data_list)
            image_matched_sites = MyModel.objects.filter(image__in=image_data_list).values('image','text')
            print("image_matched_sites--->",image_matched_sites)
            im_data = {}
            for i in image_matched_sites:
                im_data[i.get('image')] = i.get('text')
            print("im data---->",im_data)
            data = []
            link_img_data ={}
            for i in image_data_list:
                link_img_data[i] = im_data.get(i)
                # data.append(link_img_data)
            print("data---->",link_img_data)



            return JsonResponse({"data":link_img_data})
        except Exception as e:
            print("Error:",str(e))
            return JsonResponse({"data":None})
    print("ppppppp")
    return render(request, 'index.html')


@csrf_exempt
def image_scan(request):
    if request.method == 'POST':
        # try:
        print("hi")
        print(request.POST)
        image_file = request.FILES['file']
        print("image_file-->",image_file)
        webcam_image = Image(file=image_file)
        webcam_image.save()

        image_list = Load_Data().from_folder(['.'+settings.MEDIA_URL+'images'])
        st = mysearch_setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
        st.run_index_output()
        imgurl=st.get_similar_images(image_path='media/user_images/'+str(image_file),number_of_images=1)
        print("url",imgurl)
        image_data_list = []
        for i in imgurl.values():
            print(i.split('/')[2])
            image_data_list.append('images/'+i.split('/')[3])
        print(image_data_list)
        image_matched_sites = MyModel.objects.filter(image__in=image_data_list).values('image','text')
        print("image_matched_sites--->",image_matched_sites)
        im_data = {}
        for i in image_matched_sites:
            im_data[i.get('image')] = i.get('text')
        print("im data---->",im_data)
        data = []
        link_img_data ={}
        for i in image_data_list:
            link_img_data[i] = im_data.get(i)
            # data.append(link_img_data)
        print("data---->",link_img_data)

        os.remove('media/user_images/'+str(image_file))
        Image.objects.filter(file=image_file).delete()

        return JsonResponse({"data":link_img_data})
        # except Exception as e:
        #     print("Error:",str(e))
        #     return JsonResponse({"data":None})





# def image_upload(request):
#     context = dict()
#     if request.method == 'POST':
#         username = request.POST["username"]
#         image_path = request.POST["src"]  # src is the name of input attribute in your html file, this src value is set in javascript code
#         image = NamedTemporaryFile()
#         image.write(urlopen(path).read())
#         image.flush()
#         image = File(image)
#         name = str(image.name).split('\\')[-1]
#         name += '.jpg'  # store image in jpeg format
#         image.name = name
#         if image is not None:
#             obj = Image.objects.create(username=username, image=image)  # create a object of Image type defined in your model
#             obj.save()
#             context["path"] = obj.image.url  #url to image stored in my server/local device
#             context["username"] = obj.username
#         else :
#             return redirect('/')
#         return redirect('any_url')
#     return render(request, 'index.html', context=context)  # context is like respose data we are sending back to user, that will be rendered with specified 'html file'.         

# @csrf_exempt
# def image_upload(request):
#     if request.method == 'POST' and request.FILES:
#         image_file = request.FILES['file']
#         webcam_image = WebcamImage(image=image_file)
#         webcam_image.save()
#         # webcam_image = WebcamImage(image=image_file)
#         # webcam_image.save()
#         return JsonResponse({'status': 'success'})
#     return render(request, 'index.html')