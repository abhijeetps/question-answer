# Question and Answer

App that lets you answer questions from the document uploaded.

## Features

- App let's you upload questions in JSON and adds documents in PDF from where we have to find answers to questions.
- App provides and API that we integrate with any frontend.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY`

`PINECONE_API_KEY`

`PINECONE_ENVIRONMENT`

`PINECONE_INDEX`

You can simply perform the following command to prepare the env template.

`cp .env.example .env`

Add the value to the environment variables on your end.

## Run Locally

Clone the project

```bash
  git clone https://github.com/abhijeetps/question-answer
```

Go to the project directory

```bash
  cd question-answer
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Add environment variables to _.env_ file.

Start the server

```bash
  uvicorn server:app --reload
```

## Authors

- [@abhijeetps](https://www.github.com/abhijeetps)
