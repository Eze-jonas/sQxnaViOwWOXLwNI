**MonReader: Blind Assistive Reading System**

**Introduction**

MonReader is an assistive reading system designed to support visually impaired users by identifying when a book page is stable for capture, extracting text from the captured image, and converting the extracted text into speech.

The system consists of two major software components:

1. Page-Flip Detection Model (Image Classification)

2. OCR–TTS Pipeline (Optical Character Recognition and Text-to-Speech)

Together, these components form an integrated end-to-end intelligent system for automated text-to-audio conversion.

**project 1:** 

Page-Flip Detection Model

**Objective**

This component implements an image classification model that detects whether a book page is flipping or stable (non-flipping), enabling the system to identify the optimal moment for image capture.

**Dataset**

The dataset was sourced from an AI and computer vision solutions provider specializing in intelligent systems for object recognition, motion detection, and visual data analysis.

The dataset consists of separate training and test sets stored in distinct folders.

**Dataset Summary**

**Training Set**

* Flip images: 1,162
* Notflip images: 1,230

**Test Set**

* Flip images: 290
* Notflip images: 307

**Exploratory Data Analysis (EDA)**

Exploratory Data Analysis showed:

Images are in RGB format
Resolution: 1920 × 1080 (Full HD)
Class distribution is  approximately balanced

**Data Preprocessing and Augmentation**
* Training Set Augmentation

The training set was augmented on-the-fly using:

* RandomRotation(10)
* ColorJitter(brightness=0.2, contrast=0.2)
* GaussianBlur(kernel_size=3)

**Image Transformations**

Images were:

* Resized
* Converted to tensors
* Normalized

**Train-Validation Split**

The training dataset was split using stratified sampling:

* Training: 90%
* Validation: 10%

**Model Architecture and Training**

The model was developed using PyTorch and trained using a transfer learning approach with ResNet50 as a fixed feature extractor.

**Training Configuration**

* Backbone frozen
* Final classification layer trained
* Binary classification task

**Optimization**

* Loss Function: CrossEntropyLoss
* Optimizer: Adam
* Learning Rate: 0.001
* Batch Size: 32
* Epochs: 10

**Validation and Test Evaluation**

The trained model was evaluated on:

* Validation set
* Independent test set

The test set used the same preprocessing pipeline:

* Resize
* Tensor conversion
* Normalization

**Results**

* Training Set Classification Report

                 precision     recall     f1-score     support

        flip         0.95         0.98         0.97      1045

        notflip      0.98         0.95         0.97       1107

        accuracy                               0.97        2152

        macro avg    0.97         0.97         0.97        2152

        weighted avg 0.97         0.97        0.97         2152

**Training Confusion Matrix**

    [[1028 17]
    [53 1054]]

**Validation Set Classification Report**

               precision   recall   f1-score   support

    flip        0.97     0.97       0.97       117
    notflip     0.98     0.98       0.98       123

    accuracy                         0.97       240



    
**Validation Confusion Matrix**

    [[114 3]
    [3 120]]

**Test Set Classification Report**

             precision   recall   f1-score   support

    flip        0.95     0.97       0.96       290

    notflip     0.97     0.95       0.96       307

    accuracy                         0.96       597

**Test Confusion Matrix**

    [[280 10]
     [15 292]]

**project 1 Conclusion**

This component successfully developed a page-flip detection model capable of identifying stable pages for image capture.

Using transfer learning with ResNet, the model achieved strong and consistent performance across training, validation, and test sets, with a test F1-score of 96%, demonstrating good generalization for practical deployment.

**project 1 Recommendations**

Future improvements may include:

* Fine-tuning selected ResNet layers
* Expanding the dataset for greater diversity
* Hyperparameter optimization
* Additional augmentation techniques
* Real-time inference testing


**project 2: OCR–TTS Pipeline**

**Objective**

This component processes an image captured by MonReader, extracts text using OCR, and converts the extracted text into speech to assist visually impaired users in reading.

**System Architecture**

Camera Input → Page Flip Detection → Stable Page Detected → Image Capture → OCR (Gemini) → Text Preprocessing → Tacotron2 TTS → Audio Output

**Software Components**

1. OCR Module

This module implements:

* run_gemini_ocr()

Inputs:

* Preloaded image
* preConfigured Gemini client

Function:

Extracts text using Gemini API (gemini-2.5-flash)

2. TTS Module

This module implements:

* preprocess_text_for_tts()
* Cleans OCR text
* Segments text into chunks
* Maximum chunk size: 250 characters
* generate_audio()
* Converts text chunks to speech
* Uses preloaded Tacotron2 model
* Returns audio files
* combine_audio()
* Concatenates generated audio files
* Returns final audio output path

3. Pipeline Module

Implements:

* ocr_tts()

This function orchestrates:

* OCR
* Text preprocessing
* Speech synthesis

into a unified pipeline.

4. Flask Application (app.py)

This serves as the main system entry point.

Functions include:

* Loading input images
* Configuring Gemini client
* Initializing Tacotron2
* Calling OCR and TTS modules
* Providing a user interface using HTML and Bootstrap

**Containerization and Cloud Deployment**

The Flask application was:

* Tested locally
* Containerized using Docker
* Validated in a local containerized environment
* Pushed to Docker Hub
* Deployed on AWS for production use

  **How to Run the Flask Application**

The application is deployed on an AWS EC2 virtual machine and accessed remotely via SSH.

1. Connect to the EC2 instance via SSH

**ssh -i "C:\Users\USER\Music\ocr_tts_pem\ocr_tts_key.pem" ubuntu@13.62.18.160**

2. (One-time setup) Add user to Docker group

This allows running Docker commands without sudo:

**sudo usermod -aG docker ubuntu**

Then refresh group permissions:

**newgrp docker**

3. Start the Docker container

**docker start ocr_app**

4. Access the application in a browser

Open the following URL:

**http://<EC2_PUBLIC_IP>:80**

This loads the web interface where an image can be uploaded for OCR and TTS processing.

**project 2 Conclusion**

This project demonstrated the development of a complete OCR–TTS pipeline capable of extracting text from images and converting it into speech.

By integrating Gemini OCR with Tacotron2, the system provides an effective automated text-to-audio solution.

Its modular architecture, Docker containerization, and AWS deployment demonstrate scalability and production readiness.

**project 2 Recommendations**

Future improvements may include:

* Improving OCR robustness under difficult image conditions
* Optimizing TTS latency and audio quality
* Implementing asynchronous or queue-based processing
* Supporting multilingual OCR and TTS
* Adding load balancing and monitoring for production deployment

**Overall MonReader Conclusion**

This project developed an integrated assistive reading system combining:

* Page-flip detection
* Optical character recognition
* Text-to-speech synthesis
* Cloud deployment

Together, these components form a complete MonReader system capable of detecting stable book pages, capturing visual text, extracting textual content, and converting it into speech for visually impaired users.

The project demonstrates practical application of machine learning, deep learning, software engineering, and cloud deployment in building an end-to-end intelligent assistive system.
