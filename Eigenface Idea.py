import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import random

NUMBER_OF_IMAGES = 20

def loadImage(filePath):
    colour_img = cv.imread(filePath)
    gray_image = cv.cvtColor(colour_img, cv.COLOR_BGR2GRAY)

    h, w = gray_image.shape

    image = np.array(gray_image)

    np.transpose(image)
    return image, h, w

def loadImages(objType):
    images = []

    trainingImages = os.listdir("Training Images - Eigen/" + objType + "/")
    trainingImages = random.choices(trainingImages, k=NUMBER_OF_IMAGES)
    
    for i in trainingImages:
        fileName = "Training Images - Eigen/" + objType + "/" + i
        colour_img = cv.imread(fileName)
        gray_image = cv.cvtColor(colour_img, cv.COLOR_BGR2GRAY)

        h, w = gray_image.shape
        gray_image = np.reshape(gray_image, [h*w], order='C')

        images.append(gray_image)

    images = np.array(images)
    images = np.reshape(images, [NUMBER_OF_IMAGES, h*w], order='C')
    images = np.transpose(images)
    return images, h, w

def createEigenValues(classDir):

    original_tensors, h, w = loadImages(classDir)

    d = h * w

    images = np.double(original_tensors)

    meanMatrix = np.mean(images, axis=1)[:, np.newaxis]

    images = images - meanMatrix

    s = np.cov(images)

    eigvectorPath = classDir + ".V.npy"
    eigvalPath = classDir + ".D.npy"
    bestVectorsPath = classDir + ".bestVectors.npy"
    wPath = classDir + ".W.npy"
    meanMatrixPath = classDir + ".MMatrix.npy"
    
    if (os.path.exists(bestVectorsPath) and os.path.exists(wPath) and os.path.exists(meanMatrixPath)):
        bestVectors = np.load(bestVectorsPath)
        eigval = np.load(wPath)
        meanMatrix = np.load(meanMatrixPath)
    else:
        #[V, D] = np.linalg.eig(s) (Need to do more research into eigenvalues)
        print("Generating eigen values")
        eigval, eigvectors = np.linalg.eigh(s)
        eigval = np.sort(eigval)[::-1]
        eigvectors = np.fliplr(eigvectors)
        
        #Calculating eigen values is very resource intensive even for small images so saving the results helps testing
        #V.tofile("subject01.V")
        #D.tofile("subject01.D", dtype=np.float64)
        eigsum = sum(eigval)
        csum = 0
        for i in range(eigval.shape[0]):
            csum = csum + eigval[i]
            tv = csum / eigsum
            if tv > 0.95:
                k95 = i
                break

        bestVectors = np.array(eigvectors[:, :k95]).transpose()
        w = np.array([np.dot(bestVectors, images[:, i]) for i in range(10)])
        
        np.save(bestVectorsPath, bestVectors)
        np.save(wPath, w)
        np.save(meanMatrixPath, meanMatrix)

 
plt.figure()
plt.subplot(4, 4, 1)

def test(fileDir, typeTest):
    
    image, h, w = loadImage(fileDir)
    d = h * w


    #print(V[:, 0].reshape(h, w))
    image = image.astype(np.float32)

    bestVectors = np.load(typeTest + ".bestVectors.npy")
    w = np.load(typeTest + ".W.npy")
    meanMatrix = np.load(typeTest + ".MMatrix.npy")
    
    #w = np.array([np.dot(bestVectors, images[:, i]) for i in range(10)])

    #Test unknown image

    normImage = (image.reshape(1, d) - meanMatrix.transpose()).reshape(d)
    wImage = np.dot(bestVectors, normImage)

    diff = w - wImage
    norms = np.linalg.norm(diff, axis=1)
    return min(norms)

def classTest(classType):
    global classes
    images = os.listdir("Training images - Eigen/" + classType + "/")
    successes = 0
    i = 1
    for image in images:
        results = [test("Training images - Eigen/" + classType + "/" + image, objType) for objType in classes]
        TestMinimum, testClass = min(zip(results, classes))
        if testClass == classType:
            successes += 1
        else:
            print(classType, i, results)
    return successes / len(images)

classes = ["Power Drill", "File", "Hammer", "Scissors", "Screwdriver"]
for obj in classes:
    print("Creating " + obj + " eigen values")
    createEigenValues(obj)

NUM_OF_DRILL_PICTURES = 86
NUM_OF_FILE_PICTURES = 43

for objType in classes:
    successPercent = classTest(objType)
    print(objType, ":", successPercent)


DrillTrue = test("Training images - Eigen/Power Drill/11.JPG", "Power Drill")
DrillFalse = test("Training images - Eigen/Power Drill/11.JPG", "File")
FileTrue = test("Training images - Eigen/File/11.JPG", "File")
FileFalse = test("Training images - Eigen/File/11.JPG", "Power Drill")

print("Drill min:, ", DrillTrue, DrillFalse)
print("File min:, ", FileTrue, FileFalse)

print(fileSuccesses / NUM_OF_FILE_PICTURES)
print(drillSuccesses / NUM_OF_DRILL_PICTURES)
plt.show()


