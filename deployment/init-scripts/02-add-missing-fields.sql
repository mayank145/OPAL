-- Add missing fields to match legacy FATS system
-- This script adds the missing fields from the legacy system

USE opal;

-- Add missing fields to fault table
ALTER TABLE fault 
ADD COLUMN operator VARCHAR(20) AFTER section,
ADD COLUMN todo VARCHAR(80) AFTER sdescribe,
ADD COLUMN section2 VARCHAR(30) AFTER status,
ADD COLUMN views INT(6) DEFAULT 0 AFTER dislikes;

-- Add missing fields to fats_comments table  
ALTER TABLE fats_comments
ADD COLUMN todo VARCHAR(80) AFTER fats_id,
ADD COLUMN solution VARCHAR(80) AFTER todo;

-- Add indexes for new fields
CREATE INDEX idx_fault_operator ON fault(operator);
CREATE INDEX idx_fault_todo ON fault(todo);
CREATE INDEX idx_fault_views ON fault(views);
CREATE INDEX idx_fats_comments_todo ON fats_comments(todo);
CREATE INDEX idx_fats_comments_solution ON fats_comments(solution);

-- Show updated table structures
DESCRIBE fault;
DESCRIBE fats_comments;
