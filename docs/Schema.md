# Database Schema

## Users Table

- **UserID** (Primary Key): Unique identifier for each user.
- **Username**: User's chosen name.
- **Email**: User's email address.
- **PasswordHash**: Hashed password for authentication.

## Projects Table

- **ProjectID** (Primary Key): Unique identifier for each project.
- **UserID** (Foreign Key): Identifier linking to the Users table.
- **ProjectName**: Name of the project.
- **Description**: A brief description of the project.

## Images Table

- **ImageID** (Primary Key): Unique identifier for each image.
- **ProjectID** (Foreign Key): Identifier linking to the Projects table.
- **FilePath**: Path or URL where the image is stored.
- **UploadTime**: Timestamp of when the image was uploaded.

## Labels Table

- **LabelID** (Primary Key): Unique identifier for each label.
- **ProjectID** (Foreign Key): Identifier linking to the Projects table.
- **ImageID** (Foreign Key): Identifier linking to the Images table.
- **Label**: The class or label assigned to the image.

## TrainingConfigurations Table

- **ConfigID** (Primary Key): Unique identifier for the training configuration.
- **ProjectID** (Foreign Key): Identifier linking to the Projects table.
- **LearningRate**: Learning rate used in the training.
- **Epochs**: Number of epochs.
- **BatchSize**: Batch size.
- **OtherParameters**: JSON or serialized form of additional parameters.

## TrainingSessions Table

- **SessionID** (Primary Key): Unique identifier for each training session.
- **ConfigID** (Foreign Key): Identifier linking to the TrainingConfigurations table.
- **Status**: Current status of the training session (e.g., running, completed).
- **StartTime**: Start time of the training session.
- **EndTime**: End time of the training session.

# API Schema

## Data Upload API

### POST `/api/projects/{projectId}/data/images`

- **Purpose**: Upload image files to a specific project.
- **Request Body**: Form data with files.
- **Response**: JSON with upload summary and any errors.

### POST `/api/projects/{projectId}/data/labels`

- **Purpose**: Upload label data for images in a project.
- **Request Body**: JSON mapping image identifiers to labels.
- **Response**: JSON with confirmation and any validation errors.

## Training API

### PUT `/api/projects/{projectId}/training/configure`

- **Purpose**: Configure training parameters for a project.
- **Request Body**: JSON with training parameters (learning rate, epochs, batch size).
- **Response**: JSON with confirmation.

### POST `/api/projects/{projectId}/training/start`

- **Purpose**: Start a new training session with the current configuration.
- **Response**: JSON with session ID and status.

### GET `/api/projects/{projectId}/training/{sessionId}/status`

- **Purpose**: Get the current status of a training session.
- **Response**: JSON with session status, progress, and real-time metrics.

### GET `/api/projects/{projectId}/training/{sessionId}/results`

- **Purpose**: Get the results of a completed training session.
- **Response**: JSON with accuracy, loss, confusion matrix, and model details.
