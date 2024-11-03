# easy_llm_agent_deploy
LLM agent deployment example - set up your .env install and login through gcloud cli then run `bash deploy.sh`

## Tasks
- [x] Minimal LangGraph agent
- [x] Multi-turn chat UI
- [x] Deployment script
  - [x] GCP
  - [ ] AWS
  - [ ] Azure
  - [ ] DigitalOcean
- [ ] Agent state DB persistence
- [ ] Tracing and APMs
- [ ] Logging conversations
- [x] Minimal CI
- [x] Secret detection
- [ ] CD
- [ ] Streaming responses

## Project structure
Folders:

**.github**: Actions, includes CI and secret detection

**llm_agent**: Agent and UI code

**tests**: Unit tests

Files:

**.env**: env file with LLM API KEY, use .env.example as an example

**deploy.sh**: Deploy to Cloud Run

**Dockerfile**: Dockerfile to build the app

**run.sh**: use `bash run.sh prod` to run the app locally


## References:

* https://stackoverflow.com/questions/76322463/how-to-initialise-a-global-object-or-variable-and-reuse-it-in-every-fastapi-endp/76322910#76322910 
* https://github.com/zauberzeug/nicegui/blob/main/examples/chat_app/main.py