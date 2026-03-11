CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO messages (content)
SELECT 'Initial seed message from init.sql'
WHERE NOT EXISTS (
  SELECT 1 FROM messages WHERE content = 'Initial seed message from init.sql'
);
