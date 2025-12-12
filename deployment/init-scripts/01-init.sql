-- OPAL Unified System - MariaDB Initialization Script
-- This script adds missing columns to existing legacy tables (does NOT create new tables)
-- The system uses existing legacy tables: fault, fcomments, items, days

USE opal;

-- Add missing columns to fault table (if they don't exist)
-- Note: fault.idno is INT(11) in legacy, not VARCHAR
ALTER TABLE fault 
    ADD COLUMN IF NOT EXISTS todo CHAR(80),
    ADD COLUMN IF NOT EXISTS operator CHAR(20),
    ADD COLUMN IF NOT EXISTS views INT(6) DEFAULT 0,
    ADD COLUMN IF NOT EXISTS section2 CHAR(30),
    ADD COLUMN IF NOT EXISTS is_blank BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS status CHAR(10) DEFAULT 'open',
    ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium',
    ADD COLUMN IF NOT EXISTS assigned_to VARCHAR(100),
    ADD COLUMN IF NOT EXISTS created_by VARCHAR(100),
    ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Note: fcomments table already exists with structure:
-- idno INT(11) PRIMARY KEY AUTO_INCREMENT
-- faultidno INT(11) - references fault.idno
-- todo CHAR(80)
-- solution CHAR(80)
-- operator CHAR(20)
-- datein DATETIME
-- sdescribe MEDIUMTEXT

-- Note: items table already exists - used for summit logs (TO/IO entries)
-- Filter by logcrew IN ('TO', 'IO') for TO-IO entries

-- Note: days table already exists - used for daily crew assignments and weather

-- Create indexes for performance (if they don't exist)
CREATE INDEX IF NOT EXISTS idx_fault_issue ON fault(issue);
CREATE INDEX IF NOT EXISTS idx_fault_section ON fault(section);
CREATE INDEX IF NOT EXISTS idx_fault_datein ON fault(datein);
CREATE INDEX IF NOT EXISTS idx_fault_status ON fault(status);
CREATE INDEX IF NOT EXISTS idx_fault_priority ON fault(priority);
CREATE INDEX IF NOT EXISTS idx_fault_blank ON fault(is_blank);

-- Create full-text search index for FATS (if not exists)
-- Note: This may fail if index already exists, that's okay
SET @index_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.STATISTICS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'fault' 
    AND INDEX_NAME = 'ft_fault_search'
);

SET @sql = IF(@index_exists = 0, 
    'ALTER TABLE fault ADD FULLTEXT ft_fault_search(issue, idescribe, solution, sdescribe)',
    'SELECT "Full-text index already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Mark blank entries (entries with no content)
UPDATE fault 
SET is_blank = TRUE 
WHERE (issue IS NULL OR issue = '') 
AND (idescribe IS NULL OR idescribe = '')
AND (solution IS NULL OR solution = '')
AND (sdescribe IS NULL OR sdescribe = '')
AND is_blank IS NULL;

-- Show table information
SHOW TABLES;
SELECT COUNT(*) as total_faults FROM fault;
SELECT COUNT(*) as total_comments FROM fcomments;
SELECT COUNT(*) as total_items FROM items WHERE logcrew IN ('TO', 'IO');
SELECT COUNT(*) as total_days FROM days;
