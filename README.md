#### MonReader: Page Flip Detection using Deep Learning

#### Overview
MonReader is a new mobile document digitization experience for the blind, for researchers and for everyone else in need for fully automatic, highly fast and high-quality document scanning in bulk. It is composed of a mobile app and all the user needs to do is flip pages and everything is handled by MonReader: it detects page flips from low-resolution camera preview and takes a high-resolution picture of the document, recognizing its corners and crops it accordingly, and it dewarps the cropped document to obtain a bird's eye view, sharpens the contrast between the text and the background and finally recognizes the text with formatting kept intact, being further corrected by MonReader's ML powered redactor.


#### Dataset
The dataset was sourced from an AI and computer vision solutions provider specializing in:
- Object recognition
- Motion detection
- Visual data analysis

####  Dataset Details
| Set        | Flip | Not Flip | Total |
|------------|------|----------|-------|
| Training   | 1162 | 1230     | 2392  |
| Test       | 290  | 307      | 597   |

- Image format: RGB  
- Resolution: **1920 × 1080 (Full HD)**  

#### Exploratory Data Analysis (EDA)
- Images are high-resolution RGB images
- Approximately balanced distribution between classes
- Suitable for binary classification

#### Data Preprocessing

#### Augmentation (Training Set)
- RandomRotation(10)
- ColorJitter(brightness=0.2, contrast=0.2)
- GaussianBlur(kernel_size=3)

#### Transformations
- Resize
- Convert to tensor
- Normalize

#### Data Split
- **90% Training**
- **10% Validation**
- Stratified sampling applied

#### Model Architecture

- Model: **ResNet (Transfer Learning)**
- Approach: **Feature Extraction**
  - Backbone frozen
  - Only final layer trained
- Task: **Binary Classification (Flip vs Not Flip)**

#### Training Configuration

- Loss Function: **CrossEntropyLoss**
- Optimizer: **Adam**
- Learning Rate: **0.001**
- Epochs: **10**
- Batch Size: **32**

#### Model Performance

#### Training F1 Score: **97%**
Confusion Matrix:
[[1028 17]
[ 53 1054]]

#### Validation F1 Score: **97%**
Confusion Matrix:
[[114 3]
[ 3 120]]

#### Test F1 Score: **96%**
Confusion Matrix:
[[280 10]
[ 15 292]]

#### Evaluation Metrics
- Precision
- Recall
- F1-score
- Accuracy

The model shows **consistent performance across all datasets**, indicating good generalization and minimal overfitting.

## Conclusion
This project demonstrates the effectiveness of transfer learning for image classification tasks. Using a ResNet model as a fixed feature extractor, the system achieved **96% f1 score on unseen test data**.

The model is robust and suitable for real-world deployment in systems like MonReader, where accurate timing of image capture is critical.

#### Future Improvements
- Fine-tune the ResNet backbone for improved performance
- Increase dataset size for better generalization
- Apply additional augmentation techniques
- Evaluate using advanced metrics (ROC-AUC, PR curves)
- Deploy in a real-time pipeline (e.g., OCR + TTS system)

#### Tech Stack
- Python
- PyTorch
- torchvision
- NumPy
- Matplotlib

#### Use Cases
- Automated document scanning
- OCR preprocessing pipelines
- Assistive reading systems
- Smart cameras for document capture

#### Project Status
Completed  
Ready for deployment / integration  


