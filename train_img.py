# from DeepImageSearch import Index,LoadData,SearchImage
# image_list = LoadData().from_folder(['/home/egrove/image_project/adminstration/media/images'])
# Index(image_list).start()

from DeepImageSearch import Load_Data, Search_Setup

# Load images from a folder
image_list = Load_Data().from_folder(['/home/egrove/image_project/adminstration/media/images'])
print("len-->",len(image_list))
 # Set up the search engine, You can load 'vit_base_patch16_224_in21k', 'resnet50' etc more then 500+ models 
st = Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=100)

# Index the images
st.run_index()

# Get metadata
# metadata = st.get_image_metadata_file()

# # Add new images to the index
# st.add_images_to_index(['image_path_1', 'image_path_2'])

# Get similar images
ss = st.get_similar_images(image_path='/home/egrove/image_project/adminstration/media/user_images/input_img28_4_2023_12_1_13example.jpg', number_of_images=10)
print("sss--->",ss)
# # Plot similar images
# st.plot_similar_images(image_path='image_path', number_of_images=9)

# # Update metadata
# metadata = st.get_image_metadata_file()