from PIL import Image
from tensorflow.python.keras import layers, models
import matplotlib.pyplot as plt, numpy as np, random, tensorflow as tf

# cat_0_img_cnt = 6500
# cat_2_img_cnt = 5500
# cat_0_training_img_cnt = 5850
# cat_2_training_img_cnt = 4950

cat_0_img_cnt = 1000
cat_2_img_cnt = 1000
cat_0_training_img_cnt = 10
cat_2_training_img_cnt = 10

# load training images
training_labels_arr = np.array([np.array([int(x > cat_0_training_img_cnt)]) for x in range(cat_0_training_img_cnt + cat_2_training_img_cnt)])
test_labels_arr = np.array([np.array([int(x > cat_0_img_cnt - cat_0_training_img_cnt)]) for x in range(cat_0_img_cnt - cat_0_training_img_cnt + cat_2_img_cnt - cat_2_training_img_cnt)])
print("Generated labels.")

fp = open("cat_0_pure_2.txt", 'r')
cat_0_imgs = np.array(fp.readlines(), dtype=np.float64).reshape((cat_0_img_cnt, 128, 128, 3))
fp.close()
print("Loaded category_0 images.")

fp = open("cat_2_pure_2.txt", 'r')
cat_2_imgs = np.array(fp.readlines(), dtype=np.float64).reshape((cat_2_img_cnt, 128, 128, 3))
fp.close()
print("Loaded category_2 images.")

training_images_arr = np.concatenate((cat_0_imgs[:cat_0_training_img_cnt], cat_2_imgs[:cat_2_training_img_cnt]))
test_images_arr = np.concatenate((cat_0_imgs[cat_0_training_img_cnt:], cat_2_imgs[cat_2_training_img_cnt:]))
print("Arranged images into arrays.")

# for i in range(5850):
#     im = Image.open(f"ai_dataset_3/category_0_formatted/category_0_formatted_img_{i}.png", 'r')

#     pixels_arr = np.array(list(im.getdata()))
#     im.close()
#     pixels_arr.resize(128, 128, 3)
#     training_images_lst.append(pixels_arr)

#     training_labels_lst.append(np.array([0])) # category_0 is labelled as 0

#     print(f"Opened image \033[31m{i}\033[0m. 5850 total images.")

# for i in range(4950):
#     im = Image.open(f"ai_dataset_3/category_2_formatted/category_2_formatted_img_{i}.png", 'r')

#     pixels_arr = np.array(list(im.getdata()))
#     im.close()
#     pixels_arr.resize(128, 128, 3)
#     training_images_lst.append(pixels_arr)

#     training_labels_lst.append(np.array([1])) # category_2 is labelled as 1

#     print(f"Opened image \033[34m{i}\033[0m. 4950 total images.")

# random.seed(10)
# random.shuffle(training_images_lst)
# random.seed(10)
# random.shuffle(training_labels_lst)

np.random.seed(10)
np.random.shuffle(training_images_arr)
np.random.seed(10)
np.random.shuffle(training_labels_arr)
print("Shuffled training images.")

np.random.seed(10)
np.random.shuffle(test_images_arr)
np.random.seed(10)
np.random.shuffle(test_labels_arr)
print("Shuffled test images.")

training_images_arr /= 255
test_images_arr /= 255
print("Normalised the data.")

# training_images_arr = np.array(training_images_lst) / 255.0
# training_labels_arr = np.array(training_labels_lst)

class_names = ["safe", "questionable", "explicit"]

# load test images
# test_images_lst = []
# test_labels_lst = []

# fp = open("ai_dataset_3/category_0_formatted/category_0_formatted_image_count.txt", 'r')
# # cat_0_img_cnt = int(fp.readline())
# cat_0_img_cnt = 6500
# fp.close()

# for i in range(5850, cat_0_img_cnt):
#     # im = Image.open(f"ai_dataset_3/category_0_formatted/category_0_formatted_img_{i}.png", 'r')

#     # pixels_arr = np.array(list(im.getdata()))
#     # im.close()
#     # pixels_arr.resize(128, 128, 3)
#     # test_images_lst.append(pixels_arr)

#     # test_labels_lst.append(np.array([0]))

#     print(f"Opened image \033[31m{i}\033[0m. {cat_0_img_cnt} total images.")

# for i in range(40):
#     im = Image.open(f"ai_dataset_2/category_1_formatted/category_1_formatted_img_{i}.png", 'r')

#     pixels_arr = np.array(list(im.getdata()))
#     im.close()
#     pixels_arr.resize(128, 128, 3)
#     test_images_lst.append(pixels_arr)

#     test_labels_lst.append(np.array([1]))

#     print(f"Opened image \033[32m{i}\033[0m. 40 total images.")

# fp = open("ai_dataset_3/category_2_formatted/category_2_formatted_image_count.txt", 'r')
# # cat_2_img_cnt = int(fp.readline())
# cat_2_img_cnt = 5500
# fp.close()

# for i in range(4950, cat_2_img_cnt):
#     im = Image.open(f"ai_dataset_3/category_2_formatted/category_2_formatted_img_{i}.png", 'r')

#     pixels_arr = np.array(list(im.getdata()))
#     im.close()
#     pixels_arr.resize(128, 128, 3)
#     test_images_lst.append(pixels_arr)

#     test_labels_lst.append(np.array([1]))

#     print(f"Opened image \033[34m{i}\033[0m. {cat_2_img_cnt} total images.")

# test_images_arr = np.array(test_images_lst) / 255.0
# test_labels_arr = np.array(test_labels_lst)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 50
history = model.fit(training_images_arr, training_labels_arr, epochs=epochs, batch_size=32,
                    validation_data=(test_images_arr, test_labels_arr))
# history = model.fit(training_images_arr, training_labels_arr, epochs=epochs, batch_size=32, verbose=1)

# model.save_weights(f'python_files/checkpoints/ann_3_simplified_{cat_0_img_cnt + cat_2_img_cnt}_images_{epochs}_epochs')
model.save_weights(f'python_files/checkpoints/ann_3_simplified_{cat_0_img_cnt + cat_2_img_cnt}_images_{epochs}_epochs')

plt.plot(history.history["accuracy"], label="training")
plt.plot(history.history["val_accuracy"], label="test")
plt.title(f"{cat_0_img_cnt + cat_2_img_cnt} Images")
plt.xlabel("epoch")
plt.ylabel("accuracy")
plt.xlim((0, epochs))
plt.ylim(0, 1)
plt.legend()
plt.show()

# model.load_weights('python_files/checkpoints/ann_3_2946_images')

# test_loss, test_acc = model.evaluate(test_images_arr, test_labels_arr, verbose=2)
# print(test_acc)

# predictions = model.predict(test_images_arr)

# for i in range(len(test_images_lst)):
#     print(f"Image {i}\t{np.argmax(predictions[i])}")

# tp = 0
# tn = 0
# fp = 0
# fn = 0

# for i in range(cat_0_img_cnt - 1400):
#     if np.argmax(predictions[i]):
#         fp += 1
#     else:
#         tn += 1

# for i in range(cat_0_img_cnt - 1400, len(test_images_lst)):
#     if np.argmax(predictions[i]):
#         tp += 1
#     else:
#         fn += 1

# print(f"True positives: {tp}")
# print(f"False positives: {fp}")
# print(f"False negatives: {fn}")
# print(f"True negatives: {tn}")
