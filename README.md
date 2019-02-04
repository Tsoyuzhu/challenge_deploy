# Task Description:
Please find a dataset with peoples names and their gender. 

The task is to create a Machine Learning application (e.g. Tensorflow or Keras) in Flask/Django API (with swagger API Documentation) predict the gender of peoples first names. The endpoints should have the ability to retrain and serve the machine learning model. 

A requirements.txt file in and Instructions on how to run the app locally in your README.md must be included. 

 # Bonus Task:
Note that these tasks are optional and will not be judged as strictly as the items mentioned above.
- Write a Dockerfile that will create an image of your compiled back-end code
- Write a bash script that compiles your back-end code and builds your Dockerfile.

# Instructions

# API Documentation
Swagger UI Documentation for the app API can be viewed at the route '/api/doc'. If the app is being hosted locally, the url may be 'localhost:5000/api/doc'.

# ML Model
- Building a ML model without any prior knowledge has proven to be interesting and challenging. The model is a neural network built using the Keras Sequential API. The training data is formed from the Names column of the data set and the training labels are taken from the gender column of the data set. The names and labels needed to be converted to vectors in order for the neural network to train on them.
- The model was trained in a jupyter notebook which can be found in the root of the app directory. The model was then downloaded as an h5 file which the backend loads using the keras load_model() method.

# Assumptions:
- It is assumed that the gender specified in the second column of the csv data is correct, i.e probability of the gender belonging to that name is 1.  
- It is NOT assumed that the user will provide a valid string as a prediction input.
- It is NOT assumed that the user will provide a valid test data set. The system will reject datasets with improper format. 

# Considerations:
- Data persistence and user authentication is not implemented for this application. This means that each user that visits the application and submits a  retraining request will not receive a unique model to retrain. Similarly, they will not be able to retrieve a model they have previously trained. This funcionality could be implemented in future by storing each user's training data in a database with their user ID.

- A key decision was made to extract information from an uploaded csv file client side and then process the resulting information serverside. It would be inefficient to save the uploaded file to the app file system each time the model would about to be trained. Furthermore, it is difficult to determine the safety of the file contents. By performing the data validation clientside with javascript, we can check if the file contents are valid and stop the operation before the request reaches serverside. Similarly, by validating a name to be predicted clientside, we can still print an error message and avoid an unecessary request.

- One main consideration was choosing a method of vectorisation which preserved information within a name which the neural network might learn from. I reason that two significant factors which influence gender classification from names are the letters in the name, and the sequence of letters in the name. The vectorisation method must preserve these two factors. The vectorisation method maps each letter in the name to the letters order in the alphabet, i.e a -> 1, b -> 2, c -> 3 and so on. The final vector is an array of integers. Letters or miscellaneous characters with no value are mapped to 0. Bag of words vectorisations were avoided due to lack of experience and because there was no corpus to operate upon. Despite avoiding the bag of words vectorisation, it is entirely possible that it is a valid method which i lacked the experience to implement. Given that the model maintains an average prediction accuracy of 70%, I did not replace the proposed vectorisation algorithm but this could be improved upon in future.

- The vectorisation method I have implemented pulls letters from the name using a python dictionary. The dictionary is only capable of mapping lowercase alphabetical characters to integers. This means that space characters, hiphens or other chars will not produce a meaningful mapping. It is necessary to process the user's input to ensure it only contains characters useful to the vectorisation algorithm. In addition to this, the first layer of the neural network will only accept a numpy array of shape (20,). This meant that user inputs which map to vectors of less than 20 needed to be zero padded and vectors of greater than 20 needed to be trimmed, resulting in a truncation error. This truncation error is justified by the fact that all of names within the training dataset are less than 20 characters long. If the name is longer, the model likely is unlikely to form an accurate prediction based off its set of training data.