from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import math, numpy as np, requests, sys, time

rating_int = int(sys.argv[1]) # 0 ==> s; 1 ==> q; 2 ==> e
rating_str = chr(-5 * rating_int ** 2 + 3 * rating_int + 115)
old_images_target = int(sys.argv[2]) # [file_name, rating_int, old_images_target]

PATH = "D:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# get left edge links
fp = open(f"category_{rating_int}/category_{rating_int}_left_edge_links.txt", 'r')
left_edge_links = fp.readlines()
fp.close()
left_edge_links[0] = left_edge_links[0][:-1]
left_edge_links[1] = left_edge_links[1][:-1]
left_edge_ids = []
for i in left_edge_links:
    left_edge_ids.append(i.split("%")[1])

# get links of newly uploaded images
try:
    image_links = []
    b = False
    pg = 0 + 1 # starts from pg. 2
    while True:
        pg += 1
        driver.get(f"https://yande.re/post?page={pg}&tags=rating%3A{rating_str}")

        for i in range(1, 41):
            img_lnk = driver.find_element(By.XPATH, f'/html/body/div[8]/div[1]/div[2]/div[4]/ul/li[{i}]/a').get_attribute("href")
            if img_lnk.split("%")[1] in left_edge_ids:
                b = True
                break
            image_links.append(img_lnk)
            print(f"Image link {i} on page {pg} has been found.")
        if b:
            break
    print("Got newly uploaded images' links.")
except:
    print("Error: try failed while getting newly uploaded images' links.")

# update left edge links
left_edge_links = image_links[:3] + left_edge_links
# temp = len(image_links)
# if temp > 2:
#     left_edge_links = image_links[:3]
# elif temp == 2:
#     left_edge_links = image_links + [left_edge_links[0]]
# elif temp == 1:
#     left_edge_links = image_links + left_edge_links[:2]
# for i in range(3):
#     try:
#         left_edge_links = [image_links[i]] + left_edge_links
#     except:
#         break
fp = open(f"category_{rating_int}/category_{rating_int}_left_edge_links.txt", 'w')
fp.write("\n".join(left_edge_links[:3]))
fp.close()

# save the found links
# fp = open(f"category_{rating_int}/category_{rating_int}_links.txt", 'w')
# fp.write("\n".join(image_links))
# fp.close()

# get img cnt
fp = open(f"category_{rating_int}/category_{rating_int}_image_count.txt", 'r')
img_cnt = int(fp.readline()[:-1])
fp.close()

# get offset
fp = open(f"category_{rating_int}/category_{rating_int}_offset.txt", 'r')
offset = int(fp.readline())
fp.close()

# get right edge links
fp = open(f"category_{rating_int}/category_{rating_int}_right_edge_links.txt", 'r')
right_edge_links = fp.readlines()
fp.close()
right_edge_links[0] = right_edge_links[0][:-1]
right_edge_links[1] = right_edge_links[1][:-1]
right_edge_ids = []
for i in right_edge_links:
    right_edge_ids.append(i.split("%")[1])

img_cnt += len(image_links) - offset

pg = img_cnt // 40 + 1 + 1 # starts from pg. 2
img = img_cnt % 40 + 1

# calculate the new offset
try:
    b = False
    while True:
        driver.get(f"https://yande.re/post?page={pg}&tags=rating%3A{rating_str}")
        while img > 1:
            img_lnk = driver.find_element(By.XPATH, f'/html/body/div[8]/div[1]/div[2]/div[4]/ul/li[{img - 1}]/a').get_attribute("href")
            if img_lnk.split("%")[1] in right_edge_ids:
                b = True
                break
            offset += 1
            img -= 1
        if b:
            break
        img = 41
        pg -= 1
    print("Calculated the new offset.")
except:
    print("Error: try failed while trying to calculate the new offset.")

if img == 41:
    img = 1
    pg += 1

# get old images' links
try:
    # image_links = []
    old_images_cnt = 0
    prev_pg = 0
    while old_images_cnt < old_images_target:
        if prev_pg != pg:
            driver.get(f"https://yande.re/post?page={pg}&tags=rating%3A{rating_str}")
            prev_pg = pg
        # while img < 41 and old_images_cnt < old_images_target:
        #     image_links.append(driver.find_element(By.XPATH, f'/html/body/div[8]/div[1]/div[2]/div[4]/ul/li[{img}]/a').get_attribute("href"))
        #     print(f"Image link {img} on page {pg} has been found.")
        #     img += 1
        #     old_images_cnt += 1
        # img = 1
        # pg += 1
        image_links.append(driver.find_element(By.XPATH, f'/html/body/div[8]/div[1]/div[2]/div[4]/ul/li[{img}]/a').get_attribute("href"))
        print(f"Image link {img} on page {pg} has been found.")
        pg += img // 40
        img = img % 40 + 1
        old_images_cnt += 1
    print("Got old images' links.")
except:
    print("Error: try failed while getting old images' links.")

driver.quit()

# update right edge links
right_edge_links = image_links[-1:-4:-1] + right_edge_links
fp = open(f"category_{rating_int}/category_{rating_int}_right_edge_links.txt", 'w')
fp.write("\n".join(right_edge_links[:3]))
fp.close()

# save all the collected links
fp = open(f"category_{rating_int}/category_{rating_int}_links.txt", 'w')
fp.write("\n".join(image_links))
fp.close()

# update offset
fp = open(f"category_{rating_int}/category_{rating_int}_offset.txt", 'w')
fp.write(str(offset - 10)) # if 10 or fewer new images are added to the already downloaded region, then this should help correct for that (although those images wouldn't be downloaded)
fp.close()

# end of program update
fp = open(f"category_{rating_int}/category_{rating_int}_communication.txt", 'w')
fp.write("1")
fp.close()

time.sleep(1)

fp = open(f"category_{rating_int}/category_{rating_int}_communication.txt", 'w')
fp.write("0")
fp.close()