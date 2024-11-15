# Skin Lesion Detection

Skin Lesion Detection is a web application that enables users to classify skin lesions into seven categories using a custom deep learning model named **DermaNet**. The project is built using **HTML**, **CSS**, and **Flask** with **MongoDB** for data storage.

---

## Table of Contents

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [DermaNet Model Architecture](#dermanet-model-architecture)  
4. [Skin Lesion Classes](#skin-lesion-classes)  
5. [Installation](#installation)  
6. [Usage](#usage)  

---

## Features

- **User Authentication:** Login/signup module with MongoDB for secure user data management.  
- **Image Upload Module:** Upload skin lesion images for classification.  
- **Prediction Module:** Provides the predicted class of the lesion and care suggestions.  
- **Custom Deep Learning Model:** Implements the **DermaNet** model for accurate classification.  
- **Responsive Frontend:** Developed with **HTML** and **CSS**.  

---

## Technologies Used

- **Frontend:** HTML, CSS  
- **Backend:** Flask  
- **Database:** MongoDB  
- **Deep Learning Framework:** TensorFlow/Keras  

---

## DermaNet Model Architecture

The **DermaNet** model consists of convolutional layers, separable convolutional layers, upsampling layers, and dense layers for classification. Below is the detailed architecture:

| **Layer Type**           | **Number of Filters/Units** | **Kernel Size** | **Activation** | **Other Operations**                | **Output Shape**  |
|---------------------------|----------------------------|-----------------|----------------|-------------------------------------|-------------------|
| **Input**                | -                          | -               | -              | -                                   | `(input_shape)`   |
| **Conv2D**               | 32                         | `(2, 2)`        | `swish`        | BatchNormalization, MaxPooling     | `(shape1)`        |
| **Conv2D**               | 32                         | `(2, 2)`        | `swish`        | BatchNormalization, MaxPooling     | `(shape2)`        |
| **Conv2D**               | 64                         | `(2, 2)`        | `swish`        | BatchNormalization, MaxPooling     | `(shape3)`        |
| **SeparableConv2D**      | 128                        | `(2, 2)`        | `swish`        | BatchNormalization, Dropout, MaxPooling | `(shape4)`   |
| **Conv2DTranspose**      | 64                         | `(2, 2)`        | `swish`        | BatchNormalization                 | `(shape5)`        |
| **Conv2DTranspose**      | 32                         | `(2, 2)`        | `swish`        | BatchNormalization                 | `(shape6)`        |
| **GlobalAveragePooling2D** | -                        | -               | -              | -                                   | `(shape7)`        |
| **Dense**                | 128                        | -               | `swish`        | Dropout                             | `(shape8)`        |
| **Dense**                | 128                        | -               | `swish`        | Dropout                             | `(shape9)`        |
| **Dense**                | 128                        | -               | `swish`        | Dropout                             | `(shape10)`       |
| **Output (Dense)**       | 7                          | -               | `softmax`      | -                                   | `(7,)`            |

---

## Skin Lesion Classes

The application classifies skin lesions into the following categories:

1. **Nevus (nv)**  
2. **Melanoma (mel)**  
3. **Seborrheic Keratosis (bkl)**  
4. **Basal Cell Carcinoma (bcc)**  
5. **Vascular Lesion (vasc)**  
6. **Actinic Keratosis (akiec)**  
7. **Dermatofibroma (df)**  

---

## Installation

Follow the steps below to set up the project:

### 1. Clone the Repository
```bash
git clone https://github.com/priya036/Skin-Lesion-Detection.git
cd Skin-Lesion-Detection
```

### 2. Set Up a Virtual Environment
```bash
python -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB
- Ensure MongoDB is installed and running locally or use a cloud-based MongoDB service (e.g., MongoDB Atlas).
- Update the `app.py` file with your MongoDB connection string.


### 5. Run the Application
```bash
python app.py
```
---

## Usage

1. **Login/Signup:**  
   Navigate to the login page and sign in or create a new account.

2. **Upload Image:**  
   Go to the **Upload Module** and upload a skin lesion image.

3. **Get Prediction:**  
   View the predicted class and associated remedies for the lesion.
