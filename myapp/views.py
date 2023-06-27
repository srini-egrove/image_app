import re
import os
import requests
from django.shortcuts import render
from .forms import ImageUploadForm
from django.http import HttpResponse, JsonResponse
from .models import BroadwayData,Image
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse
from fuzzywuzzy import fuzz

# Create your views here.

def get_shows_details(url_list):
    list_of_sites = []
    for path in url_list:
        test = urlparse(path)
        output =test.path
        path_list = output.split('/')
        site_data = path_list[-1]
        logo_site_strings=re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', site_data)
        list_of_sites.append(" ".join(logo_site_strings))
    return list_of_sites


@csrf_exempt
def image_to_text(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        uploaded_file = request.FILES.get('user_image_file')
        print("form",uploaded_file)
        if form.is_valid():
            form.save()
        image_path = 'https://b5d6-49-207-181-102.ngrok-free.app/media/user_images/'+str(uploaded_file)
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
        # Google lens URL 
        url = f'https://lens.google.com/uploadbyurl?url={image_path}&hl=en'
        print("Request URL:",url)
        google_lens_api= requests.get(url,headers=headers)
        html = google_lens_api.text
        get_script_tag_pattern = r'<script nonce="[^"]*">(.*?)</script>'
        script_contents = re.findall(get_script_tag_pattern, html, re.DOTALL)
        test_data= " ".join(script_contents)
        pattern = r'\[\[.*?\[(.*?)\]\]\]'
        matches = re.findall(pattern, test_data)

        text_data = ""
        for i in matches:
            if '"en",[[[' in i or '"fr",[[[' in i or '"rw",[[[' in i:
                if text_data:
                    if len(i) < len(text_data):
                        text_data = i
                else:
                    text_data  = i

        text_data = re.findall(r'\b[A-Za-z]+\b', text_data)
        if text_data:
            print("okokokok")
            remove_common_words_filter = ["the", "is", "null", "of", "for", "www", "com", "musicales", "google", "http", "https", "Image", "Search", "search", "jpg", "png", "Broadway", "images", "Musical", "New", "MUSICAL", "THE", "true", "en","PLAYBILL", "IMPERIAL", "THEATRE", "The" ]
            filtered_text_data = [word for word in text_data if len(word) >1 if word not in remove_common_words_filter]

            google_lens_output = [" ".join(filtered_text_data)]
            
        else:
            print("elseeee")
            google_lens_broadway_urls = []
            pattern_toget_broadway_links = r'https://www\.broadway\S*'
            broadway_links = re.findall(pattern_toget_broadway_links, html)
            for i in broadway_links:
                split_urls= i.split(',')
                for j in split_urls:
                    if j.startswith("https://www.broadway"):
                        google_lens_broadway_urls.append(j)
            print("google_lens_broadway_urls--",google_lens_broadway_urls)
            google_lens_output = get_shows_details(google_lens_broadway_urls)

        url_list = BroadwayData.objects.values_list('shows_links', flat=True).distinct()
        print("Input Data:",google_lens_output)
        print("Datasets:",url_list)
        list_of_sites = get_shows_details(url_list)
        nearest_match = None
        max_similarity = 0
        for google_lens_data in google_lens_output:
            for word in list_of_sites:
                similarity = fuzz.token_set_ratio(google_lens_data, word)
                if similarity > max_similarity:
                    max_similarity = similarity
                    nearest_match = (google_lens_data, word)


        print("nearest_match-->",nearest_match)
        if nearest_match:
            broadway_sites_data = list(url_list)
            matched_data_index = list_of_sites.index(nearest_match[1])
            os.remove('media/user_images/'+str(uploaded_file))
            Image.objects.filter(user_image_file=uploaded_file).delete()

            return JsonResponse({"data":str(broadway_sites_data[matched_data_index])})
        else:
            os.remove('media/user_images/'+str(uploaded_file))
            Image.objects.filter(user_image_file=uploaded_file).delete()
            return JsonResponse({"data":"no_data"})
    return render(request, 'index.html')
