ALTER TABLE tasks ADD task_owner BINARY(16);
ALTER TABLE tasks FOREIGN KEY (task_owner) REFERENCES users(uuid) ON DELETE CASCADE;