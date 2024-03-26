import cv2 
# image_paths=['Image Processing/image1.jpg','Image Processing/image2.jpg', 'Image Processing/image3.jpg'] 
image_paths=['/home/team31/project/AMDimages/image1_cropped.jpg','/home/team31/project/AMDimages/image2_cropped.jpg',
              '/home/team31/project/AMDimages/image3_cropped.jpg', '/home/team31/project/AMDimages/image4_cropped.jpg']
            #   '/home/team31/project/AMDimages/image5_cropped.jpg', '/home/team31/project/AMDimages/image6_cropped.jpg',
            #   '/home/team31/project/AMDimages/image7_cropped.jpg'] 
# initialized a list of images 
imgs = [] 
  
for i in range(len(image_paths)): 
    imgs.append(cv2.imread(image_paths[i])) 
    imgs[i]=cv2.resize(imgs[i],(0,0),fx=1,fy=1) 
    # this is optional if your input images isn't too large 
    # you don't need to scale down the image 
    # in my case the input images are of dimensions 3000x1200 
    # and due to this the resultant image won't fit the screen 
    # scaling down the images  
# showing the original pictures 
# cv2.imshow('1',imgs[0]) 
# cv2.imshow('2',imgs[1]) 
# cv2.imshow('3',imgs[2]) 
  
stitchy=cv2.Stitcher.create() 
(dummy,output)=stitchy.stitch(imgs) 
  
if dummy != cv2.STITCHER_OK: 
  # checking if the stitching procedure is successful 
  # .stitch() function returns a true value if stitching is  
  # done successfully 
    print("stitching ain't successful") 
else:  
    print('Your Panorama is ready!!!') 
  
# final output 
# cv2.imshow('final result',output) 
cv2.imwrite('/home/team31/project/AMDimages/Panorama.jpg', output)
  
cv2.waitKey(0)