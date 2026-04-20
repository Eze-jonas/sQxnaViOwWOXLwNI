**MonReader: AI-Powered Assistive Reading System**

An end-to-end assistive reading system designed to help visually impaired users convert printed text into speech.

The system combines:

* Computer Vision for page-flip detection
* OCR for text extraction
* Text-to-Speech (TTS) for audio generation
* Cloud Deployment using Docker and AWS

**Problem**

Capturing text from books while pages are turning can cause blurred images and poor OCR results.

This project addresses that by first detecting whether a page is stable before image capture, then extracting text and converting it into speech.

**Solution Architecture**

Camera Input → Page Flip Detection → Stable Page Detected → Image Capture → OCR (Gemini) → Text Preprocessing → Tacotron2 TTS → Audio Output

**Features**
* Page-Flip Detection Model
* Binary image classification:
* Flip
* NotFlip
* Transfer learning using ResNet50

**Performance:**
Test Accuracy: 96%

Test F1-Score: 96%

Confusion Matrix:

    [[280 10]
    [15 292]]

**OCR–TTS Pipeline**

Built a modular OCR-to-Speech pipeline with:

**OCR Module**
* Gemini API integration
* Image-to-text extraction

**TTS Module**

* Text preprocessing
* Tacotron2 speech generation
* Audio chunk merging

**Pipeline Orchestration**
* Unified OCR + TTS workflow

**Deployment**

The system was:

* Tested locally
* Containerized using Docker
* Pushed to Docker Hub
* Deployed on AWS

**Tech Stack**
* Machine Learning
* Python
* PyTorch
* ResNet50
* Transfer Learning
* OCR and Speech
* Gemini API
* Tacotron2

**Web and Deployment**
*Flask
*Docker
*Docker Hub
*AWS

**Results**

* Developed an integrated AI pipeline for assistive reading
* Achieved strong image classification performance
* Built modular OCR-TTS workflow
* Deployed a production-ready containerized application

**Future Improvements**
* Fine-tune ResNet backbone
* Improve OCR robustness
* Reduce TTS latency
* Add multilingual support
* Add load balancing and monitoring
* Integrate the pipeline into a full MonReader assistive reading device


