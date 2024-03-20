# Data Upload API
The Data Upload API enables users to upload datasets for image classification or object detection projects.

## 1. Upload Image Data
- **Endpoint**: `POST /api/projects/{projectId}/data/images`
- **Description**: Uploads images for training to a specific project.
- **Body**:
  - `images`: File array of images to upload.
- **Response**: A summary of the upload, including any errors encountered.

## 2. Upload Label/Class Data
- **Endpoint**: `POST /api/projects/{projectId}/data/labels`
- **Description**: Uploads label for the images in a project.
- **Body**:
  - `labels`: JSON object mapping images to labels/classes.
- **Response**: Confirmation of successful label upload, including any errors.

# Training API
The Training API allows users to configure and initiate training sessions, monitor progress, and retrieve training results.

## 1. Configure Training Parameters
- **Endpoint**: `PUT /api/projects/{projectId}/training/configure`
- **Description**: Sets or updates training parameters for a project.
- **Body**:
  - `learningRate`: The learning rate for the training session.
  - `epochs`: Number of epochs to train for.
  - `batchSize`: Batch size used in training.
  - Maybe additional model-specific parameters as needed.
- **Response**: Confirmation of configuration.

## 2. Start Training Session
- **Endpoint**: `POST /api/projects/{projectId}/training/start`
- **Description**: Initiates a new training session with the current configuration and dataset.
- **Response**: Information about the training session, such as a unique session ID.

## 3. Get Training Status
- **Endpoint**: `GET /api/projects/{projectId}/training/{sessionId}/status`
- **Description**: Retrieves the current status of a training session.
- **Response**:
  - `status`: Current status (e.g., "running", "completed").
  - `progress`: Percentage of completion.
  - `metrics`: Real-time statistics if available (e.g., loss, accuracy).

## 4. Get Training Results
- **Endpoint**: `GET /api/projects/{projectId}/training/{sessionId}/results`
- **Description**: Returns the results and statistics upon training completion.
- **Response**:
  - `accuracy`: Final accuracy of the model.
  - `loss`: Final loss value.
  - `modelDetails`: Information about the trained model, including model size and architecture summary.
