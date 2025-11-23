# Setup
Run main server:
```
uvicorn app.main:app --reload
```

Run the embedding script:
```
python -m app.cli.process_spells
```

# Database Ops
```
from app.database import spells
spells.update_many({}, { "$unset": {"desc_embedding": ""}});
```