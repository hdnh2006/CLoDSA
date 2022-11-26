from __future__ import absolute_import
from builtins import str
from builtins import object
from mahotas.demos import image_path

from .iaugmentor import IAugmentor
from imutils import paths
import os
import cv2
from joblib import Parallel, delayed
import psutil
from tqdm_joblib import tqdm_joblib


def readAndGenerateImageSegmentation(outputPath, transformers, labelextension, i_and_imagePath):
    (i, imagePath) = i_and_imagePath
    image = cv2.imread(imagePath)
    name = imagePath.split(os.path.sep)[-1]
    labelPath = os.path.join(os.sep.join(imagePath.split(os.path.sep)[:-2]), "labels") + os.sep +  name[0:name.rfind(".")] + labelextension

    label = cv2.imread(labelPath)

    for (j, transformer) in enumerate(transformers):
        (newimage, newlabel) = transformer.transform(image,label)
        # print(newimage.shape, newlabel.shape)
        cv2.imwrite(outputPath +  "images/" + str(i) + "_" + str(j) + "_" + name,
                    newimage)
        cv2.imwrite(outputPath + "labels/" + str(i) + "_" + str(j) + "_" + name[0:name.rfind(".")]+labelextension,
                    newlabel)

# This class serves to generate images for a semantic segmentation
# problem where all the images are organized in two folders called
# images and labels. Both folders must contain the same number of images
# and with the same names (but maybe different extensions). Example
# - Folder
# |- images
#    |- image1.jpg
#    |- image2.jpg
#    |- ...
# |- labels
#    |- image1.tiff
#    |- image2.tiff
#    |- ...
# where Folder/labels/image1.tiff is the annotation of the image Folder/images/image1.jpg.
# Hence, both images must have the same size.
class FolderLinearSemanticSegmentationAugmentor(IAugmentor):

    def __init__(self,inputPath,parameters):
        IAugmentor.__init__(self)
        self.inputPath = inputPath
        self.imagesPath = os.path.join(inputPath, "images") + os.sep
        self.labelsPath = os.path.join(inputPath, "labels") + os.sep
        # output path represents the folder where the images will be stored
        if parameters["outputPath"]:
            self.outputPath = parameters["outputPath"]
        else:
            raise ValueError("You should provide an output path in the parameters")
        if parameters["labelsExtension"]:
            self.labelsExtension = parameters["labelsExtension"]
        else:
            self.labelsExtension = ".tiff"
        if not os.path.exists(os.path.join(self.outputPath,"images")):
            os.makedirs(os.path.join(self.outputPath,"images"))
        if not os.path.exists(os.path.join(self.outputPath,"labels")):
            os.makedirs(os.path.join(self.outputPath,"labels"))

    def readImagesAndAnnotations(self):
        self.imagePaths = list(paths.list_files(self.imagesPath,validExts=(".jpg", ".jpeg", ".png", ".bmp",".tiff",".tif")))
        self.labelPaths = list(paths.list_files(self.labelsPath,validExts=(".jpg", ".jpeg", ".png", ".bmp",".tiff",".tif")))

        if (len(self.imagePaths)!=len(self.labelPaths)):
            raise Exception("The number of files is different in the folder of images and in the folder of labels")



    def applyAugmentation(self):
        self.readImagesAndAnnotations()
        cores_count = psutil.cpu_count(logical=False)
        if cores_count is None:
            cores_count = 1
            
        # Progress bar tqdm style        
        with tqdm_joblib(desc="Running augmentations for each image", total=len(self.imagePaths)):
            Parallel(n_jobs=cores_count)(delayed(readAndGenerateImageSegmentation)
                                        (self.outputPath,self.transformers,self.labelsExtension,x)
                                        for x in enumerate(self.imagePaths))
        # This also works same
        # Without any Parallel api
        # if len(self.imagePaths) == len(self.labelPaths):
        #     for i in enumerate(self.imagePaths):
        #         readAndGenerateImageSegmentation(self.outputPath,self.transformers,self.labelsExtension, i)
        # else:
        #     print("[Debug]:  images and labels are not having same length")



# Example
# augmentor = FolderLinearSemanticSegmentationAugmentor(
#     "/home/joheras/pythonprojects/ssai-cnn/maps/mass_buildings/test/",
#     "/home/joheras/pythonprojects/ssai-cnn/maps/mass_buildings/test/dataset-generated/",
#     ".tif"
# )

# from techniques.averageBlurringAugmentationTechnique import averageBlurringAugmentationTechnique
# from techniques.bilateralBlurringAugmentationTechnique import bilateralBlurringAugmentationTechnique
# from techniques.gaussianNoiseAugmentationTechnique import gaussianNoiseAugmentationTechnique
# from techniques.rotateAugmentationTechnique import rotateAugmentationTechnique
# from techniques.flipAugmentationTechnique import flipAugmentationTechnique
# from techniques.noneAugmentationTechnique import noneAugmentationTechnique
# from generator import Generator
# import time
# augmentor.addGenerator(Generator(noneAugmentationTechnique()))
# augmentor.addGenerator(Generator(averageBlurringAugmentationTechnique()))
# augmentor.addGenerator(Generator(bilateralBlurringAugmentationTechnique()))
# augmentor.addGenerator(Generator(gaussianNoiseAugmentationTechnique()))
# augmentor.addGenerator(Generator(rotateAugmentationTechnique()))
# augmentor.addGenerator(Generator(flipAugmentationTechnique()))
# start = time.time()
# augmentor.applyAugmentation()
# end = time.time()
# print(end - start)
