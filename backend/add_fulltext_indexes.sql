-- Add FULLTEXT indexes for searching description fields
-- This allows fast searching of large text fields
-- Run this AFTER running add_search_indexes.sql

USE opal;

-- Add FULLTEXT index on issue description field
ALTER TABLE fault ADD FULLTEXT INDEX idx_fulltext_idescribe (idescribe);

-- Add FULLTEXT index on solution description field  
ALTER TABLE fault ADD FULLTEXT INDEX idx_fulltext_sdescribe (sdescribe);

-- Add FULLTEXT index on issue field (for better text searching)
ALTER TABLE fault ADD FULLTEXT INDEX idx_fulltext_issue (issue);

-- Add FULLTEXT index on solution field (for better text searching)
ALTER TABLE fault ADD FULLTEXT INDEX idx_fulltext_solution (solution);

-- Verify FULLTEXT indexes were created
SHOW INDEX FROM fault WHERE Index_type = 'FULLTEXT';
