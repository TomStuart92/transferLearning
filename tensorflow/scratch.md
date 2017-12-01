cd tensorflow
./configure

bazel build tensorflow/examples/image_retraining:retrain

bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ../trainingImages --random_crop 10 --random_scale 10 --random_brightness 10 --flip_left_right

bazel build tensorflow/examples/image_retraining:label_image && \
bazel-bin/tensorflow/examples/image_retraining/label_image \
--graph=/tmp/output_graph.pb \
--labels=/tmp/output_labels.txt \
--output_layer=final_result:0 \
--image=../testImages/test01.png






apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler -y
apt-get install --no-install-recommends libboost-all-dev -y

pip install https://github.com/Microsoft/MMdnn/releases/download/0.1.1/mmdnn-0.1.1-py2.py3-none-any.whl
