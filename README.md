## Tensorflow Transfer Learning Repository

This repository allows for transfer learning based on the Tensorflow InceptionV3 model.

The methodology broadly follows this tutorial: [link](tensorflow.org/tutorials/image_retraining).

An academic discussion of transfer learning can be found here: [link](https://arxiv.org/pdf/1310.1531v1.pdf).

The repository is divided into five folders.

- **tensorflow**: contains the files needed to retrain the InceptionV3 model to categorise an arbitrary data set.
- **server**: contains a basic python flask server which supports drop and drag serving of the model created by the tensorflow library.
- **keras**: another retraining implementation written in Keras. This allows us to convert it to a coreML model for iOS.
- **converter**: a simple converter to take a keras model and weights and return a coreML model.
- **app**: a simple iOS app to use the coreML model outputted from the converter

All folders, except the app contain Dockerfiles to allow reproducible deployment on local and remote systems.

## Tensorflow

The tensorflow folder is set up to allow for easy transfer learning. It contains two folders and a Dockerfile.

To train a new classifier:

1. Collect training set. You're looking to get a wide selection of pictures showing a diverse set of angles etc of examples of the categories.       
2. Take about 20% of your trainingSet and move it to the testImages folder. We'll use these at the end to see how well our model performs.    
3. Place a folder named after the category you want to train in the `trainingImages` folder. The name of the folder will become the output label for the category.       
4. Build (`docker build .`) and run (`docker run -it <containerId> bash`) the docker container. This may take some time as we have to build both tensorflow and bazel from source.     
5. Configure the tensorflow build (`cd tensorflow && ./configure`).     
6. Build the underlying InceptionV3 model (`bazel build tensorflow/examples/image_retraining:retrain`).     
7. Retrain the model (`bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ../trainingImages --random_crop 10 --random_scale 10 --random_brightness 10 --flip_left_right`). See below for a discussion of the flags.   
8. Grab the trained model from the /tmp directory. You need the `output_graph.pb` and `output_labels.txt` files. These are your new model and can be used with the server below.   
9. Test the model with an image from the testImage directory with:   

```
bazel build tensorflow/examples/image_retraining:label_image && \
bazel-bin/tensorflow/examples/image_retraining/label_image \
--graph=/tmp/output_graph.pb \
--labels=/tmp/output_labels.txt \
--output_layer=final_result:0 \
--image=../testImages/test01.png
```

### Training Flags

When we train the model in step 7 there are a set of optional flags which may improve the performance of the algorithm but vastly increase the time it takes to train:

--random_crop (number between 5 - 10)   
--random_scale (number between 5 - 10)  
--random_brightness (number between 5 - 10)  
--flip_left_right

Each of these apply a transformation to the pictures in the training set to artificially make one picture appear to be several. However you need to think about if these make sense.

An OCR system with documents doesn't really make sense to have each of the pictures flipped left to right!

Think about which you use as it can take up to 10hours to train a model with all these flags on.

## Server

The server needs only two changes to be able to run image recognition on the model trained above.

1. Copy the .pb file which is found in /tmp in the tensorflow docker image after training to the lib folder and rename it classify_image_graph_def.pb.   
2. Update the labels in classification_lables.pbtxt to represent the category labels your model will separate the data into.   

The server exposes two routes:
- A `GET /` route which exposes a basic webform to allow posting of new images.   
- A `POST /` route which expects a multi-part form with the image uploaded under an image entry. It will return a JSON containing the trained labels and their predicted percentage.

The server can be run on localhost:5000 by using:

```
cd server
docker build .    ===> gives containerId
docker run -it -p 5000:5000 <containerId>
```

We use kubectl and AWS ECS to deploy the server. To push a new version of the server to ECS:

```
`aws ecr get-login --no-include-email --region eu-west-1`
docker build -t locks-ocr:v3 .
docker tag locks-ocr:v3 355555488900.dkr.ecr.eu-west-1.amazonaws.com/locks-ocr:v3
docker push 355555488900.dkr.ecr.eu-west-1.amazonaws.com/locks-ocr:v3
```

Then to deploy using kubectl

1. Update the locksOCR-deployment.yaml file to point at the version you pushed above.
2. Run `kubectl apply -f ./locksOCR-deployment.yaml`

## Keras

To train the model with Keras use `python train.py --train_dir <pathToTrainingDirectory> --val_dir <pathToValidationDirectory>`

This will train the model and output a weights.pb file and a model.json.
The model.json is actually a text file which will need to be transformed to pure json before it can be used.

## Converter

To Use:

1. Copy the files outputted from the Keras model into the converter folder.
2. Edit your batch_input_shape in the model.json to [null, 299, 299, 3] if you want xcode to properly associate an image as the input type.
3. Build and run the docker container:

```
docker build .    ===> gives containerId
docker run -it <containerId>
# from inside container shell
    python converter.py
# from outside container once finished
    docker cp <containerId>:/app/locks.mlmodel ./locks.mlmodel
```

## App

To Build:

1. Open in XCode
2. Drag the locks.mlmodel file into the build file.
3. Edit the viewcontroller.swift file as needed to integrate model.