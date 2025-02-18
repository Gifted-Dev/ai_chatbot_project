from app.models import Base  # Adjust the import as per your project structure
from app.services.database import engine  # Your SQLAlchemy engine

# Drop all tables defined in the metadata
Base.metadata.drop_all(bind=engine)

# Recreate all tables based on the current model definitions
Base.metadata.create_all(bind=engine)