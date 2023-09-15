#### snowcap

##### specs
snowcap is a software for generating beautiful real estate descriptions from written or spoken content.

##### steps
 0. Audio transcripts are transcribed and translated into english. (optional)
 1. Text transcripts are joined together with each timestamp of transcript.
 2. A prompt is used to pull all details and the type of property from transcripts.
 3. Decide on, or generate, a Writing Instruction for the specific property.
 4. Write a description each media type with the Transcripts, Details, and Writing Instruction

##### functions
- scribe: translate and transcribe various audio formats into text
- glean: pull information from transcripts
- discipline: remind agent of what is missing from current transcripts.
- fabricate: generate description of each transcript