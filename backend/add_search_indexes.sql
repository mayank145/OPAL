-- Add indexes to improve search performance
-- Run this SQL script to optimize the fault table

USE opal;

-- Add index on solution field for faster searching
CREATE INDEX idx_fault_solution ON fault(solution);

-- Add index on operator field for faster searching  
CREATE INDEX idx_fault_operator ON fault(operator);

-- Add index on section for filtering
CREATE INDEX idx_fault_section ON fault(section);

-- Add index on status for filtering
CREATE INDEX idx_fault_status ON fault(status);

-- Add index on assigned_to for filtering/searching
CREATE INDEX idx_fault_assigned_to ON fault(assigned_to);

-- Verify indexes were created
SHOW INDEX FROM fault;
