import cv2
import numpy as np
import webcolors


# def rgb_distance(color1, color2):
#     # Calculate the Euclidean distance between the two colors
#     distance = np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))
#     print(distance)
#     return distance


def cosine_similarity(color1, color2):
    # Convert the colors to numpy arrays
    color1 = np.array(color1)
    color2 = np.array(color2)
    
    # Calculate the dot product and magnitudes
    dot_product = np.dot(color1, color2)
    magnitude1 = np.linalg.norm(color1)
    magnitude2 = np.linalg.norm(color2)
    
    # Calculate cosine similarity
    cosine_sim = dot_product / (magnitude1 * magnitude2)
    print(cosine_sim)
    return cosine_sim

def are_colors_close(color1, color2, threshold=0.95):
    # Calculate the distance between the colors
    sim = cosine_similarity(color1, color2)
    # Check if the distance is below the threshold
    return sim > threshold



def detect_color_in_bboxes(image, user_color):
    print("detect color")
    roi = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate histogram of hue values in the ROI
    hist = cv2.calcHist([roi], [0], None, [180], [0, 180])

    # Find the most dominant hue value
    dominant_hue = np.argmax(hist)

    # Convert the dominant hue to an RGB color
    # Create an HSV color with the dominant hue and full saturation and value
    dominant_hsv = np.uint8([[[dominant_hue, 255, 255]]])

    dominant_rgb = cv2.cvtColor(dominant_hsv, cv2.COLOR_HSV2BGR)[0][0]

    # Extract red, green, and blue components
    red, green, blue = int(dominant_rgb[2]), int(dominant_rgb[1]), int(dominant_rgb[0])
    dc = [red,green,blue]
    # f = False
    print(dc)
    for color in user_color:
        if(are_colors_close(dc,color)):
            # f = True
            # print(True)
            print(color)
            return True
        # else:
        #     print(False)
    # return f


    # # Define the hue values for common colors
    # color_hue_values = {
    #     'red': 0,
    #     'orange': 15,
    #     'yellow': 30,
    #     'green': 60,
    #     'cyan': 90,
    #     'blue': 120,
    #     'purple': 150
    # }

    # Check if the detected hue value matches the hue value of the user input color
    # if user_color.lower() in color_hue_values:
    #     user_hue_value = color_hue_values[user_color.lower()]
    #     #print(color_hue_values[dominant_hue])
    #     if abs(user_hue_value - dominant_hue) < 10:  # Allowing a 10-degree hue tolerance
    #         return True
    print("not present")
    return False


def get_only_human_color(d):
    l1 = []
    l2 = []
    for key in d:
        if(key=='man' or key == 'woman' or key == 'person' or key == 'human' or key == 'boy' or key == 'girl'):
            for i in d[key]:
                try:
                    # Convert color name to RGB
                    rgb_value = webcolors.name_to_rgb(i)
                    # Extract red, green, and blue components
                    red = rgb_value.red
                    green = rgb_value.green
                    blue = rgb_value.blue
                    l1.append(i)
                    l2.append([red,green,blue])
                except ValueError as e:
                    continue
    return l1,l2