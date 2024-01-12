## RAG from video

This is a full stack project that uses a video as input, populates an ElasticSearch instance with vectors through an indexing pipeline, and initializes a retriver pipeline with a Solara app.

### Requirements

- Python 3.11
- Docker

### Installation

1. Clone the repository
2. Create a virtual environment with with Python 3.11 and activate it
3. Install the requirements through the requirements.txt file

### Execution of indexing pipeline

```bash
python indexing_pipeline.py
```

### Execution of retriever pipeline through the Solara app

```bash
cd app/
solara run app.py
```