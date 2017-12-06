import coremltools

# You'll need to edit your batch_input_shape in the model.json to [null, 299, 299, 3] if you want xcode to properly associate an image as the input type.

coreml_model = coremltools.converters.keras.convert(("./model.json", "./weights.h5"), input_names='image', image_input_names='image', class_labels=["mortice_deadlock", "multipoint_lock", "automatic_deadlatch"] )
coreml_model.save("locks.mlmodel")
