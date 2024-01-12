# Python code to convert video to audio
import moviepy.editor as mp
from pathlib import Path
from dotenv import load_dotenv
import os

from haystack import Pipeline
from haystack.components.audio import RemoteWhisperTranscriber
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.writers import DocumentWriter
from haystack.document_stores import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack.document_stores import DuplicatePolicy

from pydub import AudioSegment
import math

def create_directories():
    Path("./movie_files").mkdir(parents=True, exist_ok=True)
    Path("./audio_files").mkdir(parents=True, exist_ok=True)
    Path("./chunked_audio").mkdir(parents=True, exist_ok=True)


def chunk_audio(file_path, chunk_length_ms, output_path):
    audio = AudioSegment.from_file(file_path)
    chunk_length = len(audio)
    num_chunks = math.ceil(chunk_length / chunk_length_ms)
    for i in range(0, num_chunks):
        start = i * chunk_length_ms
        end = start + chunk_length_ms
        chunk = audio[start:end]
        chunk.export(f"./{output_path}/chunk_{i}.mp3", format="mp3")

def convert_video_to_audio(file_name):
    path_to_video = f"./movie_files/{file_name}"
    path_to_audio = f"./audio_files/{file_name.split('.')[0]}.mp3"


    print("Transforming video to audio...")

    # Generate Video File Clip
    clip = mp.VideoFileClip(path_to_video)

    # Generate Audio File
    clip.audio.write_audiofile(path_to_audio)

    # make a directory under chunked_audio with the file_name as the folder name
    Path(f"./chunked_audio/{file_name.split('.')[0]}").mkdir(parents=True, exist_ok=True)


    print("Chunking audio...")
    # Chunk audio file
    chunk_audio(path_to_audio, 180000, f"./chunked_audio/{file_name.split('.')[0]}")


# Usage
load_dotenv(".env")
openaikey = os.getenv("OPENAI")
elastic_search_cloud_id = os.getenv("elastic_search_cloud_id")
elastic_search_host = os.getenv("elastic_search_host")
elastic_username = os.getenv("elastic_username")
elastic_password = os.getenv("elastic_password")


# Insert Local Video File Path
file_names = ["./movie_files/my_video1.mov",
              "./movie_files/my_video2.mov",]

# Convert Video to Audio
for file_name in file_names:
    convert_video_to_audio(file_name)

print("Initializing indexing pipeline...")
# Build indexing pipeline - local development only
#document_store = ElasticsearchDocumentStore(hosts= "http://localhost:9200/")
document_store = ElasticsearchDocumentStore(hosts=elastic_search_host,
                                            basic_auth=(elastic_username, elastic_password))

embedder = SentenceTransformersDocumentEmbedder()
transcriber = RemoteWhisperTranscriber(api_key=openaikey)
documentcleaner = DocumentCleaner()
splitter = DocumentSplitter(split_by="sentence", 
                              split_length=10)
p = Pipeline()
p.add_component(instance=transcriber, name="transcriber")
p.add_component(instance=documentcleaner, name="cleaner")
p.add_component(instance= splitter, name="splitter")
p.add_component(instance=embedder, name="embedder")
p.add_component(instance=DocumentWriter(document_store=document_store), name="writer")

p.connect("transcriber.documents", "cleaner.documents")
p.connect("cleaner.documents", "splitter.documents")
p.connect("splitter.documents", "embedder.documents")
p.connect("embedder.documents", "writer.documents")
p.draw("./images/indexing_pipeline.png")
audio_files = [str(f) for f in Path("./chunked_audio").rglob("*.mp3")]
p.run({"transcriber": {"sources": audio_files}})

