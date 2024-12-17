
# NER and Intent Classification with FastAPI

  

This project demonstrates how to deploy **Named Entity Recognition (NER)** and **Intent Classification** models using **FastAPI**. It is structured in a modular way, allowing you to serve both models through separate endpoints for easy integration and scalability.

  

## Features

  

-  **Named Entity Recognition (NER)**: Extracts entities (such as names, locations, dates) from text using a fine-tuned NER model.

-  **Intent Classification**: Classifies the intent of a sentence using a fine-tuned classification model.

-  **FastAPI**: Fast, asynchronous web framework for building APIs, with automatic validation and interactive API documentation.

-  **Modular Design**: Separated modules for NER and Intent Classification models to ensure maintainability and scalability.

  

## Prerequisites

  

To run the project, you'll need to have the following installed:

  

- Python 3.7+

-  `pip` (Python package manager)

  

### Install Required Libraries

  

Clone the repository and install the dependencies:

  

```bash

git  clone  https://github.com/Mohamedalcafory/MedicaTaskManager.git

pip  install  -r  requirements.txt
```
  

### Requirements

transformers: Hugging Face's  library  to  load  pre-trained  models.

torch:  PyTorch,  a  deep  learning  framework  required  for  the  models.

fastapi:  Web  framework  for  building  APIs.

uvicorn:  ASGI  server  for  serving  the  FastAPI  app.

To  install  the  required  libraries,  you  can  run:

```bash

pip install transformers torch fastapi uvicorn
```
  

## Project Structure
	intent_ner_fastapi/
	├── app.py                  # Main FastAPI entry point
	├── models/
	│   ├── __init__.py         # Initialization for models module
	│   ├── ner_model.py        # Model loading and NER logic
	│   ├── ner_predictor.py    # NER prediction logic
	│   ├── intent_model.py     # Intent classification model loading and logic
	│   └── intent_predictor.py # Intent prediction logic
	├── schemas/
	│   ├── __init__.py         # Initialization for schemas module
	│   ├── ner_request.py      # Pydantic schema for NER request
	│   └── intent_request.py   # Pydantic schema for intent request
	└── utils/
	    ├── __init__.py         # Initialization for utilities
	    └── tokenizer.py        # Tokenizer and utility functions
	    
## How to Use

1.  **Prepare your fine-tuned models**: Make sure that you have your fine-tuned models for both NER and intent classification. Place them in the appropriate directories (`./fine_tuned_ner_model` and `./fine_tuned_intent_model`).
    
2.  **Start the FastAPI server**:
    
    Run the following command to start the FastAPI app:
    ```bash
    uvicorn app:app --reload 
    ```
3.  **Test the API**:
    You can interact with the API using any HTTP client (e.g., Postman, cURL, or directly from your browser).
    
    -   **Extract Entities (NER)**:  
        POST request to `/extract_entities/` with the JSON body:
        
        `{
          "sentence": "update medical history for Sophia Lewis"
        }` 
        
        The response will include the extracted entities.
        
    -   **Classify Intent**:  
        POST request to `/classify_intent/` with the JSON body
        
        `{
          "sentence": "add new patient Joe Doe 45 years old with diabetes"
        }` 
        
        The response will return the predicted intent.
        

### API Documentation

FastAPI automatically generates interactive API documentation using **Swagger UI**. You can access it by visiting:

`http://127.0.0.1:8000/docs` 

The documentation provides an easy-to-use interface to test the endpoints directly from the browser.

## Contact
For any inquiries or questions, please contact Mohamed.alcafory.456@gmail.com

### Key Sections in the README:

1. **Project Overview**: A brief introduction to what the project does.
2. **Prerequisites**: Details on dependencies and instructions to install them.
3. **Project Structure**: Explanation of the folder structure.
4. **How to Use**: Instructions to get the FastAPI server running and examples for testing the API.
5. **API Documentation**: Mention of the automatically generated Swagger UI documentation.
