import cv2
import os

main_folder = "/Users/kumar/personal_finance/"

def vconcat_resize(img_list, interpolation= cv2.INTER_CUBIC): 
    # take minimum width 
    w_min = min(img.shape[1] for img in img_list)

    # resizing images 
    im_list_resize = [cv2.resize(img, 
                      (w_min, int(img.shape[0] * w_min / img.shape[1])), 
                                 interpolation = interpolation) 
                      for img in img_list] 
    # return final image 
    return cv2.vconcat(im_list_resize) 

def get_final_image():
    month = "jan_2024"
    current_folder = main_folder + month + "/"
    splitwise_folder = current_folder + "splitwise/"
    files_in_folder = os.listdir(splitwise_folder)
    print("splitwise_folder ------> ", splitwise_folder)
    print("image files ------> ", files_in_folder)
    images = []
    for file in files_in_folder:
        img_file = splitwise_folder + file
        img = cv2.imread(img_file)
        images.append(img)
    img_v_resize = vconcat_resize(images)
    
    # write the output image
    final_image = current_folder + 'splitwise_combined_image.png'
    cv2.imwrite(final_image, img_v_resize)
    print("FINAL OUTPUT ------> ", final_image)


def process_splitwise_data():
    print("process_splitwise_data started ...")
    get_final_image()

process_splitwise_data()