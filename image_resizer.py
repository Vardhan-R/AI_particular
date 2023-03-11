from PIL import Image
import sys, time

rating_int = int(sys.argv[1]) # 0 ==> s; 1 ==> q; 2 ==> e
start = int(sys.argv[2])
end = int(sys.argv[3])

for i in range(start, end):
    try:
        im = Image.open(f"category_{rating_int}/category_{rating_int}_img_{i}.jpg")
        resized_img = im.resize((128, 128))
        im.close()

        resized_img.save(f"category_{rating_int}_formatted/category_{rating_int}_formatted_img_{i}.png")

        resized_img.close()

        print(f"Saved \033[31m{i - start + 1}\033[0m / {end - start}.")
    except:
        print(f"Error: try failed. i = {i}.")

print("End of program.")