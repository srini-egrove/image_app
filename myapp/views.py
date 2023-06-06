import time
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageUploadForm
from django.http import HttpResponse, JsonResponse
# # from DeepImageSearch import Index,LoadData,SearchImage
from DeepImageSearch import Load_Data, Search_Setup
# import DeepImageSearch.config as config
from .models import Image,MyModel,WebcamImage
# import tensorflow as tf
# import numpy as np
import cv2
import easyocr
from spellchecker import SpellChecker
from urllib.parse import urlparse
from fuzzywuzzy import fuzz
import re

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

# @csrf_exempt
# def image_upload(request):
#     if request.method == 'POST':
#         try:
#             print("hi")
#             print("request.POST",request.POST)
#             print("request.FILES",request.FILES)
#             form = ImageUploadForm(request.POST, request.FILES)
#             uploaded_file = request.FILES.get('file')
#             print("form",uploaded_file)
#             if form.is_valid():
#                 form.save()
#             image_list = Load_Data().from_folder(['.'+settings.MEDIA_URL+'images'])
#             st = mysearch_setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
#             st.run_index_output()
#             imgurl=st.get_similar_images(image_path='media/user_images/'+str(uploaded_file),number_of_images=3)

#             # st =Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=len(image_list))
#             # imgurl=Search_Setup.get_similar_images(image_path='media/user_images/'+str(uploaded_file),number_of_images=5)
#             print("url",imgurl)
#             image_data_list = []
#             for i in imgurl.values():
#                 print(i.split('/')[2])
#                 image_data_list.append('images/'+i.split('/')[3])
#             print(image_data_list)
#             image_matched_sites = MyModel.objects.filter(image__in=image_data_list).values('image','text')
#             print("image_matched_sites--->",image_matched_sites)
#             im_data = {}
#             for i in image_matched_sites:
#                 im_data[i.get('image')] = i.get('text')
#             print("im data---->",im_data)
#             data = []
#             link_img_data ={}
#             for i in image_data_list:
#                 link_img_data[i] = im_data.get(i)
#                 # data.append(link_img_data)
#             print("data---->",link_img_data)
#             # os.remove('media/user_images/'+str(uploaded_file))
#             # Image.objects.filter(file=uploaded_file).delete()



#             return JsonResponse({"data":link_img_data})
#         except Exception as e:
#             print("Error:",str(e))
#             return JsonResponse({"data":None})
#     print("ppppppp")
#     return render(request, 'index.html')
# def preprocess_image(image_path):
#     image = cv2.imread(image_path)
#     image = cv2.resize(image, (224, 224))  # Resize the image to the desired input shape
#     image = image / 255.0  # Normalize the pixel values
#     image = np.expand_dims(image, axis=0)  # Add a batch dimension
#     return image


# @csrf_exempt
# def image_upload(request):
#     if request.method == 'POST':
#         try:
#             print("hi")
#             print("request.POST",request.POST)
#             print("request.FILES",request.FILES)
#             form = ImageUploadForm(request.POST, request.FILES)
#             uploaded_file = request.FILES.get('file')
#             print("form",uploaded_file)
#             if form.is_valid():
#                 form.save()
#             im_data = {1:'https://www.broadwayworld.com/shows/A-Beautiful-Noise-333542.html',2:'https://www.broadwayworld.com/shows/Bad-Cinderella-333897.html',3:"https://www.broadwayworld.com/shows/Bob-Fosse's-Dancin'-333641.html",4:'https://www.broadwayworld.com/shows/White-Girl-in-Danger-334233.html',5:'https://www.broadwayworld.com/shows/Dog-Man-The-Musical-334386.html',6:'https://www.broadwayworld.com/shows/Grey-House-334403.html',7:'https://www.broadwayworld.com/shows/The-Book-of-Mormon-329767.html',8:'https://www.broadwayworld.com/shows/The-Phantom-of-the-Opera-6624.html',9:'https://www.broadwayworld.com/shows/Six-333248.html',10:'https://www.broadwayworld.com/shows/Sweeney-Todd-334066.html',}
#             model = tf.keras.models.load_model('media/test2_vgg_model.h5')
#             image_path = 'media/user_images/'+str(uploaded_file)
#             preprocessed_image = preprocess_image(image_path)

#             # Make predictions on the image
#             predictions = model.predict(preprocessed_image)
#             predicted_name = predictions[0]
#             print("Predicted Name:", predicted_name)
#             # Preprocess the input image

#             sorted_array = np.sort(predicted_name)[::-1]
#             top_1_values = sorted_array[:1]
#             print(top_1_values)
#             positions = np.where(predicted_name == top_1_values)[0]
#             matched_position = positions+1
#             print("matched_position:",matched_position)
#             print("url-->",im_data[matched_position[0]])
#             link_data = im_data[matched_position[0]]
#             data_percentage = (round(float(top_1_values), 2))*100
#             print("%:",data_percentage)

#             os.remove('media/user_images/'+str(uploaded_file))
#             Image.objects.filter(file=uploaded_file).delete()




#             return JsonResponse({"data":str(link_data),"match_percentage":int(data_percentage)})
#         except Exception as e:
#             print("Error:",str(e))
#             return JsonResponse({"data":None})
#     print("ppppppp")
#     return render(request, 'index.html')


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

        # os.remove('media/user_images/'+str(image_file))
        # Image.objects.filter(file=image_file).delete()

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


#-----OCR Method----------

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
            image_path = 'media/user_images/'+str(uploaded_file)
            # import easyocr

            # Create an OCR reader
            reader = easyocr.Reader(['en'],gpu=False)

            # Read the image and extract the text
            result = reader.readtext(image_path,detail = 0)
            print(result)


            spell = SpellChecker()

            # find those words that may be misspelled
            misspelled = spell.unknown(result)
            list1=[]
            for word in misspelled:
                print("word-->",word)
                # Get the one `most likely` answer
                correct_word = spell.correction(word)
                print("most like-->",spell.correction(word))
                if correct_word != None:
                    list1.append(correct_word)
                else:
                    list1.append(word)
            print(list1)
            url_list = MyModel.objects.values_list('text', flat=True).distinct()
            # email_list = Email.objects.values_list('email', flat=True).distinct()
            print("url_list--->",url_list)
            list2 = []
            for path in url_list:
                test = urlparse(path)
                output =test.path
                path_list = output.split('/')
                site_data = path_list[-1]
                ss=re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', site_data)
                list2.append(" ".join(ss))
            print(list2)


           
            nearest_match = None
            max_similarity = 0

            for word1 in list1:
                for word2 in list2:
                    similarity = fuzz.token_set_ratio(word1, word2)
                    if similarity > max_similarity:
                        max_similarity = similarity
                        nearest_match = (word1, word2)

            data = list2.index(nearest_match[1])
            print(data)
            url_data = list(url_list)
            print(url_data[data])
            return JsonResponse({"data":str(url_data[data])})



        except Exception as e:
            print("Error:",str(e))
            return JsonResponse({"data":None})
    print("ppppppp")
    return render(request, 'index.html')