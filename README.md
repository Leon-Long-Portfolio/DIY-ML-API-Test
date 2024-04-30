# DIY ML API Application

## Project Overview

1. RESTFUL APIs for DIY ML API App includes User Management, Project Management, Image Uploader, Training Configuration, and Training Analysis.
2. Each module is tested utilizing the test_app.
3. Database: Implemented relational-based SQL
4. Queueing and Multi-threading capacity for asynchronous activity

## Project Design

### RESTFUL API Definitions


### SQL Database Design


## Project Planning

### Phase 1 - Software Development: REST APIs and Modularity

#### Phase 1.1

Data Upload Module:
- API user should be able to upload data (images) for training in a project
- API user should be able to upload label or class data for images in a project

Training Module:
- API user should be able to add or remove training points
- API user should be able to configure training parameters
- API user should be able to run and track iterations of training
- API user should be able to analyze data before training

#### Phase 1.2

User Module (Authentication and Authorization):
- A project is associated with a user

Project Module:
- API user should be able to create a ML image classification or Object detection project for Training and Inference

Data Analysis Module:
- API user should be able when the training is completed to get training stats

Test Model Module:
- API user should be able to test a model using new dataset and get results

Model Module:
- API user should be able to deploy a model to be used for inference and should be able to get a unique API to use for a project-iteration combination
- ALL APIs should be independent of the ML model and data

Inference Module:
- API user should be able to use inference API to run and get results on an image

### Phase 2 - Database Implementation: Relational-Base SQL and Possible MongoDB Schema Implementation

Base on the requirements, the following preliminary schema shows the various tables with their respective relationships. The SQL schema consists of multiple tables including User, Project, Image, TrainingConfig, TrainingResult, and InferenceResult. Each table is designed to efficiently store and manage different aspects of machine learning training processes.

#### User
id: Primary key, integer
username: String, unique, non-nullable
password_hash: String

Relationships:
projects: One-to-many with Project

#### Project
id: Primary key, integer
user_id: Foreign key from User, non-nullable, cascades on delete
project_type: String, non-nullable
name: String, nullable

Relationships:
images: One-to-many with Image
training_config: One-to-one with TrainingConfig

#### Image
id: Primary key, integer
filename: String, non-nullable
label: String, nullable
feature_size: Float, nullable
project_id: Foreign key from Project, non-nullable, cascades on delete

#### TrainingConfig
id: Primary key, integer
project_id: Foreign key from Project, non-nullable, cascades on delete
learning_rate: Float, non-nullable, default 0.001
epochs: Integer, non-nullable, default 10
batch_size: Integer, non-nullable, default 32

Relationships:
project: Back-populates from Project

### MongoDB Schema Possible Implementation

Based on the application's requirements, here's a possible MongoDB schema:

#### User Collection
username: String, unique
password_hash: String
projects: Array of references to Project documents

#### Project Document
user_id: Reference to User document
project_type: String
name: String
images: Array of references to Image documents
training_config: Embedded document (TrainingConfig)

#### Image Document
filename: String
label: String
feature_size: Float
project_id: Reference to Project document

#### TrainingConfig Embedded Document
learning_rate: Float
epochs: Integer
batch_size: Integer

This MongoDB schema uses both embedded documents and references. The training_config in the Projects collection is embedded directly within each project document because its life cycle depends on the existence of the project. Images, training results, and inference results are stored in separate collections and linked by references to maintain flexibility.

### Justification for Using SQL

#### 1. Structured Query Language (SQL):
SQL databases use a query language that allows for complex queries and data manipulation. This is particularly useful for the application as it requires comprehensive data retrieval capabilities, especially for the trainig results.

#### 2. Data Integrity: 
SQL databases support ACID (Atomicity, Consistency, Isolation, Durability) properties which ensure reliable handling of data. This is important for the project as data integrity and transactions are crucial for correct model analysis.

#### 3. Relationships and Normalization: 
SQL databases are effective at handling relationships between data entities, a property that is makes the backbone of the relational database used. The normalization process helps eliminate redundancy and dependency, which ensures data consistency.

#### Summary:
SQL databases provide greater support for structured data handling, complex queries and transactions, ensuring data integrity and consistency. The properties of SQL are important for managing the relational structure of the data in the project.

### Phase 3 - Queue Implementation

### Phase 4 - Data Protection
