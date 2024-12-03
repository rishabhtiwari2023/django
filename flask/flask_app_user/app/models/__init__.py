from .user_model import User,UserGroup,Log,Session
# commands:

# Initialize migrations (if you haven't already):

# bash
# Copy code
# flask db init
# Generate a migration:

# bash
# Copy code
# flask db migrate -m "Create user table"
# Apply the migration to create the tables:

# bash
# Copy code
# flask db upgrade