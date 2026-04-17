MonReader
This project developed an image classification model that detects whether a book page is flipping or not, helping MonReader determine the optimal moment to capture an image.

The dataset was sourced from an AI and computer vision solutions provider that develops intelligent systems for tasks such as object recognition, motion detection, and visual data analysis.
It consists of separate training and test sets stored in different folders. Exploratory Data Analysis (EDA) revealed that the images are in RGB format with full HD resolution (height = 1080, width = 1920). The training set contains 1,162 flip and 1,230 notflip images, while the test set contains 290 flip and 307 notflip images. 

#### Training Set Augumentation, Transformation and Split.
The training set was augmented on the fly using RandomRotation(10), ColorJitter(brightness=0.2, contrast=0.2), and GaussianBlur(kernel_size=3). The images were then resized, converted to tensors, and normalized.
The dataset was split into training (90%) and validation (10%) sets using a stratified sampling method.

#### Model Training
The model was trained using a transfer learning approach with a ResNet architecture as a fixed feature extractor. The backbone was frozen, and only the final classification layer was trained for binary classification. The model was optimized using the CrossEntropyLoss function and the Adam optimizer with a learning rate of 0.001. Training was conducted for 10 epochs with a batch size of 32.

#### Trained Model Validation
The trained model was evaluated on the validation set to monitor performance and generalization.

#### Test set Transformation and validated model test.
The test set was resized, converted to tensors, and normalized using the same preprocessing pipeline. The trained model was then evaluated on the test set.

#### Model Evaluation
The tesed model was evaluated using classification report model and the results are shown bellow.

===== Training Set Classification Report =====
              precision    recall  f1-score   support

        flip       0.95      0.98      0.97      1045
     notflip       0.98      0.95      0.97      1107

    accuracy                           0.97      2152
   macro avg       0.97      0.97      0.97      2152
weighted avg       0.97      0.97      0.97      2152


===== Training Set Confusion Matrix =====
[[1028   17]
 [  53 1054]]


 ===== Validation Set Classification Report =====
              precision    recall  f1-score   support

        flip       0.97      0.97      0.97       117
     notflip       0.98      0.98      0.98       123

    accuracy                           0.97       240
   macro avg       0.97      0.97      0.97       240
weighted avg       0.97      0.97      0.97       240


===== Validation Set Confusion Matrix =====
[[114   3]
 [  3 120]]


===== Test Set Classification Report =====
              precision    recall  f1-score   support

        flip       0.95      0.97      0.96       290
     notflip       0.97      0.95      0.96       307

    accuracy                           0.96       597
   macro avg       0.96      0.96      0.96       597
weighted avg       0.96      0.96      0.96       597


===== Test Set Confusion Matrix =====
[[280  10]
 [ 15 292]]

#### Conclusion
This project successfully developed an image classification model capable of detecting whether a book page is flipping or not. Using a transfer learning approach with a ResNet architecture as a fixed feature extractor, the model achieved high performance across training, validation, and test sets, with test f1-score reaching 96%.
The consistent performance across all datasets indicates that the model generalizes well and is effective for real-world application in determining the optimal moment for image capture in the MonReader system.

#### Recommendations.
* Future work could involve fine-tuning the ResNet backbone by unfreezing selected layers to further improve classification performance.
* Expanding the dataset with more diverse samples would enhance generalization, particularly under varying lighting and motion conditions.
* Additional augmentation techniques and hyperparameter tuning could be explored to further optimize performance.
* Incorporating real-time inference testing would help evaluate the model’s effectiveness in practical deployment scenarios.