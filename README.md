# DIY ML API Application

## Project Overview

1. RESTFUL APIs for DIY ML API App includes User Management, Project Management, Image Uploader, Training Configuration, and Training Analysis.
2. Each module is tested utilizing the test_app.
3. Database: Implemented relational-based SQL
4. Queueing and Multi-threading capacity for asynchronous activity

## Project Planning

### Phase 1
Software Development: REST APIs and Modularity

Data Upload Module:
- API user should be able to upload data (images) for training in a project
- API user should be able to upload label or class data for images in a project

Training Module:
- API user should be able to add or remove training points
- API user should be able to configure training parameters
- API user should be able to run and track iterations of training
- API user should be able to analyze data before training

User Module (Authentication and Authorization)
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

### Phase 2
Database Implementation: Relational-Base SQL

