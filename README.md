## Tensorflow Transfer Learning Repository

This repository allows for transfer learning based on the Tensorflow InceptionV3 model.

The methodology broadly follows this tutorial: [link](tensorflow.org/tutorials/image_retraining).

An academic discussion of transfer learning can be found here: [link](https://arxiv.org/pdf/1310.1531v1.pdf).

The repository is divided into two folders, tensorflow and server.

- **tensorflow**: contains the files needed to retrain the InceptionV3 model to categorise an arbitrary data set.
- **server**: contains a basic python flask server which supports drop and drag serving of the model created by the tensorflow library.

Both folders contain Dockerfiles to allow reproducible deployment on local and remote systems.

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
