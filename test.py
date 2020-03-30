import os
path='course_videos/CUC-1206073804'
for root, dirs, files in os.walk(path):
    print(root, dirs, files)
    if root != path:
        continue
    for name in files:
        if name.endswith('.mp4'):
            print(os.path.join(root, name))