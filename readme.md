#### snowcap

##### specs
snowcap is a software for generating beautiful real estate descriptions from spoken or written content.

##### steps
 0. Audio transcripts are transcribed and translated into english. (optional)
 1. Text transcripts are joined together with each timestamp of transcript.
 2. A prompt is used to pull all details and the type of property from transcripts.
 3. Decide on, or generate, a Writing Instruction for the specific property.
 4. Write a description each media type with the Transcripts, Details, and Writing Instruction

##### functions
- scribe: translate and transcribe various audio formats into text
  - recieves post request including: audio file of various formats, property_name, and unix timestamp
  - uses whisper api to transcribe audio file
  - stores transcript, property_name, and timestamp in db
- glean: pull information from transcripts
  - receives get request including: property_id
  - fetches all transcripts for property in db
  - formats with transcripts and timestamps into large string
  - uses glean prompt to gather the information for that property
  - stores gleaned info as detailed property info in db
- notice: remind agent of what is missing from current transcripts
  - receives get request including: property_name
  - fetches large gleaned property object from db
  - uses notice prompt to generate a set of questions for missing info
  - creates notice in db
  - user can then scribe more information then glean again.
- fabricate: generate description of each transcript
  - receives property_id
  - fetches gleaned information from db
  - fetched information includes prop_type
  - prop_type maps to a specific writing instruction
  - uses writing guide and instructions to generate descriptions

#### use [technical]
- a recording will be made through the recorder front end.
- that audio recording is sent to /scribe (with property name)
- a transcription is made and stored
- user can either:
  - make more recordings
  - check their work to get info gaps through /discipline
    - fn glean is called and property info stored
    - fn discipline is called to check detailed property info
    - a discipline notice is given to the user to answer questions