
INSERT INTO resources (resource_name, resource_type, location, description)
SELECT 'Computer Lab 1', 'Laboratory', 'Block A', 'Computer lab for student projects'
WHERE NOT EXISTS (
    SELECT 1 FROM resources WHERE resource_name = 'Computer Lab 1'
);

INSERT INTO resources (resource_name, resource_type, location, description)
SELECT 'Computer Lab 2', 'Laboratory', 'Block B', 'Computer lab for practical sessions'
WHERE NOT EXISTS (
    SELECT 1 FROM resources WHERE resource_name = 'Computer Lab 2'
);

INSERT INTO resources (resource_name, resource_type, location, description)
SELECT 'Seminar Hall', 'Hall', 'Main Block', 'Hall for meetings and presentations'
WHERE NOT EXISTS (
    SELECT 1 FROM resources WHERE resource_name = 'Seminar Hall'
);

INSERT INTO resources (resource_name, resource_type, location, description)
SELECT 'Project Room 1', 'Project Room', 'Block C', 'Room for group project discussions'
WHERE NOT EXISTS (
    SELECT 1 FROM resources WHERE resource_name = 'Project Room 1'
);
