# VFRForWeb

VFRForWeb performs visual font recognition for the aim of improving the contemporary web development workflow.

For implementation in code and a comprehensive walkthrough of the process, please see [**the main Jupyter notebook**](<https://github.com/SiavasFiroozbakht/VFRForWeb/blob/master/VFRForWeb.ipynb>) in this repository.

## Libraries used

Most recent methodologies and libraries in Deep Learning were used:

- TensorFlow 2.0, most widely-used Deep Learning framework, in its most recent version
- TensorFlow Datasets, the most convenient API for researchers to import entire public datasets, regardless of structure, in only a few lines of code. The AdobeVFR dataset was personally contributed to this API and further used in this work.
- matplotlib, for plotting images and statistics
- imgaug, for image augmentation / pre-processing, for improving the learning curve of the model and reduce overfitting

## Data preprocessing

The dataset, which represents the entire collection of images used to train and validate the model, is downloaded and managed via Tensorflow Datasets, for which a contribution was also made to have AdobeVFR available in the API.

Once the data is downloaded, it is then shuffled, repeated 10 times and batched in sets of 128 images, which results in 10,000 unique augmented images per font (e.g. 200,000 for 20 fonts). The entire dataset is loaded and splitted manually in 80% training, 20% validation, and the latter is used for evaluating its performance.

Randomised image augmentation is performed on images with a combination of adding noise, blur, random cropping, and perspective transforms. These augmentations help the model generalise better and reduce overfitting.

For further improving feature detection and reducing overfitting, the original images are firstly repeated 10 times and augmented differently, resulting in a 10 times larger, unique dataset.

## Proposed architecture

The proposed architecture is built from scratch and consists of 11 layers (convolutional and max pooling layers) and is inspired by recent state-of-the-art work achieved in the image classification and visual font recognition domain. Reference models include DeepFont (2015), VGG16 (2014), AlexNet (2012) as architectures and many other features such as Xavier weight initialisation, batch normalisation layers, and custom dropout rates on the last layers. A high number of variations for hyperparameters were attempted, with best results being yielded from Stochastic Gradient Descent optimiser, 0.001 learning rate, 0.2 dropout rate, and sparse categorical cross-entropy loss function.

The model is built using Tensorflow 2.0 alpha, which is a significant improvement over the version 1 predecessor, and incorporates the Keras Deep Learning API by default. A previous model was also attempted to be created with PyTorch (an alternative to Keras / TensorFlow), although the results were not satisfactory and therefore disregarded.

## Train the model

The model benefits from custom callbacks for saving the model through checkpoints when the accuracy improves, and for automatically stopping the model from training when it does not improve over 20 epochs. These are characteristics implementable in Keras which benefit researchers by allowing the training phase of the model to be resumed at a later stage and for no model learning to be lost should it be interrupted.

*(An epoch represents an entire run over the training dataset.)*

## Evaluation

For evaluating the model, the common approach used for evaluating image classification neural networks is used: check the number of fonts which were correctly recognised as the top-1 prediction (i.e. the model is most sure that is the font in the image) and similarly for top-5 prediction (i.e. check whether the correct font is one of the 5 that the model predicted to be the most likely present in the image). The final loss function used (which provides the error rate) is sparse categorical cross-entropy, which is most suited for image classification over multiple number of classes as with VFR.

There have been a number of attempts in terms of various architectures and learning techniques with the aim of producing a model that generalises well on new data and font classes, minimises the error rate and maximises the accuracy for both training and validation:

- Simplified architecture similar to AlexNet and DeepFont consisting of 5 layers: less than 10% accuracy over 50 epochs. Attempted with augmented images.
- Resembled Stacked Convolutional Autoencoder architecture from DeepFont which has deemed to be better suited for real-world images rather than synthetic, for which it was therefore disregarded.
- Fine-tuned version of VGG16, with preserved pretrained weights on ImageNet, plus added flattening and multilayer perceptron layers (MLP) on top, suited especially for featured extraction of included font classes. Top-1 accuracy of 63% was gained after 62 epochs. Attempted with both original and augmented images, with the latter yielding better results. Attempted with various settings, including usage of different optimisers (Stochastic Gradient Descent, Adam, Adagrad); different dropout rates for Dense / MLP layers; different learning rates, momentum, decay rate, loss functions, etc.
- Fine-tuned version of VGG16, with preserved pretrained weights only on lower-level convolutional layers whose purpose is to detect basic shapes such as edges, corners, lines, etc. The higher-level layers were unfreezed to be trained together with the additional flattening and MLP layers. The results were similar to the previous model, but it took significantly longer to train due to the higher number of trainable parameters. Attempted with various settings as above.
- Bespoke architecture inspired from DeepFont (2015), VGG16 (2014) and AlexNet (2012), plus other applied techniques such as Xavier weight initialisation, batch normalisation layers, zero-padding, custom dropout rates on the Dense layers and others. Attempted with various settings as above, with best result choosing SGD as optimiser and a learning rate of 0.001, and dynamic momentum and decay rates. Achieved practically 98% top-1 accuracy and 100% top-5 accuracy on the dataset with augmented images after only 50 epochs, though 90%+ top-1 accuracy was gained after first 10 epochs. Tested on validation data as well on which the model was not trained, plus with manually created snapshots of fonts that were also correctly recognised.

| Architecture                                              | Top-1 Accuracy | Top-5 Accuracy |
| --------------------------------------------------------- | -------------- | -------------- |
| Simplified DF / AlexNet                                   | 6%             | 10%            |
| Resembled DF SCAE                                         | 50%            | -              |
| Fine-tuned VGG16, preserved weights                       | 63%            | 80%            |
| Fine-tuned VGG16, preserved weights for lower layers only | 70%            | 85%            |
| Bespoke architecture                                      | 98%            | 100%           |

An additional attempt was also made to integrate VFR with an existing solution for automatic web design prototyping, though the chosen project (pix2code) deemed to be excessively overfitting and did not permit further integration of the VFRForWeb model. Multiple approaches were considered, including using the publicly available model, a fine-tuned version and a Keras-made model.

## Appendix

### Creating the base model from the pre-trained convnets

The VGG16 model is a well-known architecture used in the ImageNet Large Scale Visual Recognition Competition (ILSVRC) in 2014, which won the competition by achieving the lowest error rates at the time of classifying 14 million images over 1000 classes through a state-of-the-art CNN architecture. 

AlexNet, similarly, won the competition in 2012 for the first time using CNNs and training the model on GPUs.