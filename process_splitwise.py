import cv2
import os
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


main_folder = "/Users/kumar/personal_finance/"
month = "jan_2024"

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
    print("get_final_image started ...")
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

def read_from_splitwise_final_image():
    print("read_from_splitwise_final_image started ...")
    current_folder = main_folder + month + "/"
    file_path = current_folder + 'splitwise_combined_image.png'
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("Splitwise File not found")
        return
    
    # read the image
    image = cv2.imread(file_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    options = f"-l eng --psm 6"
    results = pytesseract.image_to_data(rgb_image,config=options, output_type=Output.DICT) 
    print("results ------> ", results)
    print("results text length ------> ", len(results["text"]))
    coords = [(results["left"][i], results["top"][i], results["width"][i], results["height"][i]) 
        for i in range(len(results["text"])) 
        if int(results["conf"][i]) > 0]
    print("coords length ------> ", len(coords))
    image_copy = image.copy()
    for coord in coords:
            x, y, w, h = coord
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = image_copy[y:y + h, x:x + w]
            extracted_text = pytesseract.image_to_string(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB), config=options).strip()
            print("extracted_text ------> ", extracted_text)
    # show_image(image_copy, "Bounding boxes")
    
def read_from_temp_splitwise_images():
    print("read_from_temp_splitwise_images started ...")
    current_folder = main_folder + month + "/temp/"
    files_in_folder = os.listdir(current_folder)
    print("temp_folder ------> ", current_folder)
    print("image files ------> ", files_in_folder)
    print("image files length ------> ", len(files_in_folder))
    for file in files_in_folder:
        print("file ------> ", file)
        try:
            img_file = current_folder + file
            img = cv2.imread(img_file)
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            options = f"-l eng --psm 6"
            extracted_text = pytesseract.image_to_string(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB), config=options).strip()
            print("extracted_text ------> ", extracted_text)
        except Exception as e:
            print("Exception in read_from_temp_splitwise_images ------> ", e)
            continue

def read_from_sample_image():
    print("read_from_sample_image started ...")
    img_file = "/Users/kumar/personal_finance/jan_2024/temp/split_image4.png"
    img = cv2.imread(img_file)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    options = f"-l eng --psm 6"
    extracted_text = pytesseract.image_to_string(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB), config=options).strip()
    _, width ,_ = img.shape
    print("extracted_text ------> ", extracted_text)
    positions = split_number_with_custom_ratio(width, [10, 45, 25, 25])
    positions = np.round(positions).astype(int)
    positions = [sum(positions[:i+1]) for i in range(len(positions))]

    print("positions ------> ", positions)
    print("shape -->" ,img.shape)
    # Draw vertical lines on the image
    image_with_lines = draw_vertical_lines(img, positions)
    write_image(image_with_lines, 'vertical_lines.png')

    split_images = split_image_vertical(img, positions)
    print("split_images length ------> ", len(split_images))
    for i, split_image in enumerate(split_images):
        write_image(split_image, f'split_image{i}.png')
        rgb_image = cv2.cvtColor(split_image, cv2.COLOR_BGR2RGB)
        options = f"-l eng --psm 6"
        extracted_text = pytesseract.image_to_string(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB), config=options).strip()
        print("extracted_text sub image------> ", extracted_text)



def split_image_to_row_images():
    print("split_image_to_row_images started ...")
    current_folder = main_folder + month + "/"
    file_path = current_folder + 'splitwise_combined_image.png'
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("Splitwise File not found")
        return
    
    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

   # Create a LineSegmentDetector object
    lsd = cv2.createLineSegmentDetector(0)

    # Detect lines in the image
    lines = lsd.detect(gray_image)[0]
    print("total lines detected ------> ", len(lines))

    # Convert lines to integers
    lines = np.round(lines).astype(int)

    horizontal_lines = [line[0] for line in lines if abs((line[0][3] - line[0][1]) / (line[0][2] - line[0][0] + 1e-5)) < 0.1]
    horizontal_lines.sort(key=lambda line: line[1])
    print("horizontal_lines length------> ", len(horizontal_lines))
    
    # Filter lines based on length (exclude lines less than 800 pixels)
    filtered_lines = filter_lines_by_length(horizontal_lines, 800)
    print("filtered_lines length ------> ", len(filtered_lines))
    
    line_image = image.copy()
    for line in filtered_lines:
        x1, y1, x2, y2 = line.flatten()
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    write_image(line_image, 'line_segments.png')
    # Split the image at the y-coordinates of horizontal lines
    split_images = []
    for i in range(len(filtered_lines) + 1):
        if i == 0:
            split_images.append(image[:filtered_lines[i][1], :])
        elif i == len(filtered_lines):
            split_images.append(image[filtered_lines[i - 1][1]:, :])
        else:
            split_images.append(image[filtered_lines[i - 1][1]:filtered_lines[i][1], :])

    print("split_images length------> ", len(split_images))

    for i, split_image in enumerate(split_images):
        height, width, channels = split_image.shape
        if height > 40 and width > 500:
            write_temp_image(split_image, f'split_image{i}.png')

    print("FUNC END")

def filter_lines_by_length(lines, max_length):
    return [line for line in lines if calculate_line_length(line) >= max_length]

def calculate_line_length(line):
    x1, y1, x2, y2 = line.flatten()
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return length
         
def write_image(image, file_name):
    current_folder = main_folder + month + "/"
    try:
        file_path = current_folder + file_name
        cv2.imwrite(file_path, image)
    except Exception as e:
        print("Exception in write_image ------> ", e)
        return

def write_temp_image(image, file_name):
    current_folder = main_folder + month + "/temp/"
    try:
        file_path = current_folder + file_name
        cv2.imwrite(file_path, image)
    except Exception as e:
        print("Exception in write_image temp------> ", e)
        return

def show_image(img, title="SHOW_IMAGE"):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()  # Display the image

def split_number_with_custom_ratio(number, ratio):
    # Calculate the total ratio parts
    total_ratio_parts = sum(ratio)
    # Calculate the individual parts based on the custom ratio
    parts = [number * r / total_ratio_parts for r in ratio]
    return parts

def draw_vertical_lines(image, line_positions, color=(0, 0, 255), thickness=2):
    image_copy = image.copy()
    for x in line_positions:
        cv2.line(image_copy, (x, 0), (x, image.shape[0]), color, thickness)
    return image_copy

def split_image_vertical(image, vertical_positions):
    # Sort the vertical positions
    vertical_positions.sort()
    # Split the image based on vertical positions
    split_images = []
    for i in range(len(vertical_positions) + 1):
        if i == 0:
            split_images.append(image[:, :vertical_positions[i]])
        elif i == len(vertical_positions):
            split_images.append(image[:, vertical_positions[i-1]:])
        else:
            split_images.append(image[:, vertical_positions[i-1]:vertical_positions[i]])

    return split_images


def process_splitwise_data():
    print("process_splitwise_data started ...")
    # get_final_image()
    # split_image_to_row_images()
    # read_from_splitwise_final_image()
    # read_from_temp_splitwise_images()
    read_from_sample_image()

process_splitwise_data()


