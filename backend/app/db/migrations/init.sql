-- Enable the uuid-ossp extension to allow the use of uuid_generate_v4()
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the 'tasks' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- Using uuid_generate_v4() for UUID generation
    query TEXT,
    multi_agent_framework TEXT,
    llm_model TEXT,
    enable_internet BOOLEAN,
    status TEXT,
    task_metadata JSONB DEFAULT '{}',
    final_response TEXT,
    input_file_names JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Optionally, create an index on task_id for faster queries
CREATE INDEX IF NOT EXISTS idx_task_id ON tasks(task_id);
