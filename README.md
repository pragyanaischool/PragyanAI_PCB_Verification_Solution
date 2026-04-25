# PragyanAI_PCB_Verification_Solution
pcb_ai_system/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── analyze.py
│   │   │   ├── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── parser_service.py
│   │   │   ├── graph_service.py
│   │   │   ├── rule_engine.py
│   │   │   ├── simulation_service.py
│   │   │   ├── report_service.py
│   │   │   ├── visual_service.py
│   │   │
│   │   ├── ai/
│   │   │   ├── llm.py
│   │   │   ├── vlm.py
│   │   │   ├── agents.py
│   │   │   ├── prompts.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   ├── crud.py
│   │   │
│   │   ├── utils/
│   │   │   ├── file_utils.py
│   │   │   ├── cache.py
│   │   │   ├── logger.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── start.sh
│
├── frontend/
│   ├── app.py
│   ├── components/
│   │   ├── uploader.py
│   │   ├── dashboard.py
│   │   ├── chat_ui.py
│   │
│   ├── utils/
│   │   ├── api_client.py
│
├── models/
│   ├── gnn_model.py
│   ├── train.py
│
├── data/
│   ├── sample_pcbs/
│
├── uploads/
│
├── .env
├── README.md
