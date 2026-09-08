```shell
                 HUMAN
                   │
                   ▼
          Django input form
                   │
                   ▼
          ProspectInput
          status = PENDING
                   │
                   │ enqueue
                   ▼
              Celery
                   │
                   ▼
        process_prospect_input()
                   │
                   ├── AI/MCP
                   │
                   ├── standardize name
                   ├── standardize role
                   ├── classify industry
                   ├── generate tags
                   ├── extract findings
                   └── prepare outreach
                   │
                   ▼
               Prospect
                   │
                   ▼
          ProspectInput
          status = COMPLETED
```