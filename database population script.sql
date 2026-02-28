-- Clear existing data
TRUNCATE TABLE feedback, eventoutcomes, eventregistrations, events, users RESTART IDENTITY CASCADE;

-- Insert 20 volunteers
-- Password for all volunteers: Volunteer123! (hashed with bcrypt)
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('emily_wilson', '$2b$12$iiW8VLmBrFtSWAAR1mQWLunL5yYCe0O4Dadep8q8oZG9fxPRcWtRG', 'Emily Wilson', 'emily.wilson@email.com', '+64 21 123 4567', '123 Ocean Drive, North Beach', 'emily.jpg', 'Beach cleanups, Marine conservation', 'volunteer', 'active'),
('james_chen', '$2b$12$Ultraz34Ld1lsjRVsK.7Uuldur9CugvRwRuodeMXXTmJX7hC4Vhne', 'James Chen', 'james.chen@email.com', '+64 22 234 5678', '45 Valley Road, Central City', NULL, 'Tree planting, Recycling', 'volunteer', 'active'),
('sarah_parker', '$2b$12$RGJ9uvHn0kqWrIJzgTSrlOQT0kZfbVn21d00CLF1mViyrC7BHompu', 'Sarah Parker', 'sarah.parker@email.com', '+64 27 345 6789', '78 Forest Lane, Eastside', 'sarah.jpg', 'Forest conservation, Wildlife protection', 'volunteer', 'active'),
('michael_torres', '$2b$12$B7eBMJpoSW6myL3KP72o1.HWQVcnKZ6/lwzvcTL4M45X74vaG8vxS', 'Michael Torres', 'michael.torres@email.com', '+64 21 456 7890', '234 River Road, Southtown', NULL, 'River cleanups, Water quality', 'volunteer', 'active'),
('lisa_wong', '$2b$12$64atIJ7JAhctSOr3juuaWe6ykjXHCG7tbvA.DCMbWjw5IR/ryXLUG', 'Lisa Wong', 'lisa.wong@email.com', '+64 22 567 8901', '56 Harbour View, Marina', 'lisa.jpg', 'Marine debris, Plastic pollution', 'volunteer', 'active'),
('david_kumar', '$2b$12$kuYLrodcL.q/y6POSN6oguG5h1.qPYbhmPbCDEFVWqaPJYuSO5ihO', 'David Kumar', 'david.kumar@email.com', '+64 27 678 9012', '89 Park Avenue, Central', NULL, 'Community gardening, Composting', 'volunteer', 'active'),
('emma_thompson', '$2b$12$3OC3QMhCiko9YQPBTAez/.Bu1JHT22kz2mfyNfeTaoxb99k20fzL2', 'Emma Thompson', 'emma.thompson@email.com', '+64 21 789 0123', '12 Mountain Road, West Hills', 'emma.jpg', 'Trail maintenance, Native plants', 'volunteer', 'active'),
('ryan_obrien', '$2b$12$nsaJaaMrLSBFqMcY9mo1W.i1.Sxo8uCXwrHS9SYKrMQM.vNdRdaym', 'Ryan O''Brien', 'ryan.obrien@email.com', '+64 22 890 1234', '34 Coastal Highway, Sunset Beach', NULL, 'Beach ecology, Bird watching', 'volunteer', 'active'),
('olivia_martinez', '$2b$12$vR4gj1Ju8GJ0oCDSPlURE.eLp.ZYoGv/aVjPpSS7Irm3H/RwfkDNO', 'Olivia Martinez', 'olivia.martinez@email.com', '+64 27 901 2345', '67 Creek Street, West Creek', 'olivia.jpg', 'Stream restoration, Water testing', 'volunteer', 'active'),
('thomas_williams', '$2b$12$h9Uiv6tOBvB0qVTq7FxhWO8igTYgKQf447GO6jeHvont.EZ8jjOWy', 'Thomas Williams', 'thomas.williams@email.com', '+64 21 012 3456', '89 Station Road, Railway', NULL, 'Urban sustainability, Recycling', 'volunteer', 'active'),
('grace_lee', '$2b$12$Ly4XZbKwKSCJcLsi71qlXuU.Nc..FzQSPcD5BnQUE3GN71pg.A84S', 'Grace Lee', 'grace.lee@email.com', '+64 22 123 4567', '123 Garden Lane, Community Gardens', 'grace.jpg', 'Organic gardening, Native plants', 'volunteer', 'active'),
('benjamin_clark', '$2b$12$d32Lx13BH6aSdeCRC9ZzZeyShnCpEZy04zWLTwL2BsVa50eGgtc02', 'Benjamin Clark', 'benjamin.clark@email.com', '+64 27 234 5678', '456 Forest Drive, Eastside Woods', NULL, 'Forest restoration, Wildlife', 'volunteer', 'active'),
('sophie_taylor', '$2b$12$wWzFxJzgBvpqt7Na0ZR4KOr3Rm7LobDVVlGbbj.iNqnXrQPNN.rQa', 'Sophie Taylor', 'sophie.taylor@email.com', '+64 21 345 6789', '78 Beach Road, North Beach', 'sophie.jpg', 'Marine conservation, Plastic free', 'volunteer', 'active'),
('daniel_anderson', '$2b$12$0QbTZRq8d.I0QX5vSkLbT.ydWVaXlCpryl0D9/QbIY5bRYzTS3RGO', 'Daniel Anderson', 'daniel.anderson@email.com', '+64 22 456 7890', '90 River Parade, South Riverbank', NULL, 'River protection, Clean water', 'volunteer', 'active'),
('chloe_robinson', '$2b$12$YgQQFOadpeGqBpQHMpSIDeuoBH.6oM.6oHo5qUyezter0.bKu9LVG', 'Chloe Robinson', 'chloe.robinson@email.com', '+64 27 567 8901', '234 Park Street, Central Park', 'chloe.jpg', 'Park maintenance, Community events', 'volunteer', 'active'),
('matthew_white', '$2b$12$JS7ZKmqbJXdFPbkS1hT7/OCsUen2.5PZlf5nUvV1lHXp6jKQX9ya2', 'Matthew White', 'matthew.white@email.com', '+64 21 678 9012', '567 Harbour Esplanade, Harbor Front', NULL, 'Harbor cleanups, Marine debris', 'volunteer', 'active'),
('hannah_brown', '$2b$12$656kmv174rU8tSsW30OSv.AHQX8qUxzTLGUUMws00ZrNP1BDZN2xi', 'Hannah Brown', 'hannah.brown@email.com', '+64 22 789 0123', '89 Mountain Terrace, Mountain Vista', 'hannah.jpg', 'Trail conservation, Alpine ecology', 'volunteer', 'active'),
('lucas_garcia', '$2b$12$gFwmcuxAxAngS88usVFubuXuzlV0XUaOCgGNP0qVM6uoGSeImL/na', 'Lucas Garcia', 'lucas.garcia@email.com', '+64 27 890 1234', '123 West Creek Road, West Creek', NULL, 'Wetland preservation, Bird habitat', 'volunteer', 'active'),
('mia_johnson', '$2b$12$SMpAxKfMfY/Gsu1u0vnMKuoMocEDIZHDB5x4AK4fGZV5HVXN2urta', 'Mia Johnson', 'mia.johnson@email.com', '+64 21 901 2345', '456 Sunset Parade, Sunset Beach', 'mia.jpg', 'Beach ecology, Dune restoration', 'volunteer', 'active'),
('alexander_nguyen', '$2b$12$XyPrR2PnollYQcmM3Sx0VO.alyJaSY0YBE1Ma6gFzJeS94XNjQG.K', 'Alexander Nguyen', 'alexander.nguyen@email.com', '+64 22 012 3456', '789 Railway Terrace, Railway Walk', NULL, 'Urban greening, Sustainability', 'volunteer', 'active');

-- Insert 5 event leaders
-- Password for event leaders: Leader123!
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('rachel_green', '$2b$12$KvKoskAtMFv.bbxlyP5HOuniMb5P.r9gMkjiQq2L0D4VsN6F2HSg2', 'Rachel Green', 'rachel.green@ecocleanup.org', '+64 21 345 6789', '45 Coordinator Way, Central City', 'rachel.jpg', 'Community organizing, Beach conservation', 'event_leader', 'active'),
('mark_sutherland', '$2b$12$2xqG0E40hFUABQzy/Ge6COeEU6GIht6NJ92B6Od8XJhhvIcxj8.lK', 'Mark Sutherland', 'mark.sutherland@ecocleanup.org', '+64 22 456 7890', '78 Leader Lane, North Beach', NULL, 'Forest conservation, Youth engagement', 'event_leader', 'active'),
('jennifer_patel', '$2b$12$bW.L8sktwilZ72cqGDl5auM.bqcqaMYgIEJSS9UThNTMRy9Dkt96i', 'Jennifer Patel', 'jennifer.patel@ecocleanup.org', '+64 27 567 8901', '123 Organizer Street, Eastside', 'jennifer.jpg', 'River protection, Environmental education', 'event_leader', 'active'),
('robert_fisher', '$2b$12$FpOr6cv1cIDgyU5SCHHDKOeb4mK4xaGd5K5e653SiDu07wkkeqG5m', 'Robert Fisher', 'robert.fisher@ecocleanup.org', '+64 21 678 9012', '567 Captain Avenue, Harbor Front', NULL, 'Marine conservation, Plastic reduction', 'event_leader', 'active'),
('maria_rodriguez', '$2b$12$Ee8/BPgQI5FJQxfPm.lj9uGH/.yaS4vnsSA.2Jg39lqsBb1asfCsy', 'Maria Rodriguez', 'maria.rodriguez@ecocleanup.org', '+64 22 789 0123', '890 Park Boulevard, Southtown', 'maria.jpg', 'Community gardens, Sustainable living', 'event_leader', 'active');

-- Insert 2 admins
-- Password for admins: Admin123!
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES
('admin_smith', '$2b$12$t3tpvGVplKHrgJtgLBcXdOZ7G2W8oc.6Pb0pD48KdmIbsQFlfOXQy', 'John Smith', 'admin.smith@ecocleanup.org', '+64 21 111 2222', '1 Admin Plaza, Central City', 'admin_smith.jpg', 'System administration, Environmental policy', 'admin', 'active'),
('admin_wilson', '$2b$12$ohSEeRn/y2sY8zQe3MlIGO0EvugI7tS7A60JJoLA1NUGLAHJq76Au', 'Sarah Wilson', 'admin.wilson@ecocleanup.org', '+64 22 333 4444', '2 Management Drive, Central City', NULL, 'Program management, Sustainability', 'admin', 'active');

-- Insert 25 events (10 past, 15 upcoming)
INSERT INTO events (event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions) VALUES
-- Past Events (January - February 2026) - event_ids 1-10
('New Year Beach Cleanup', 21, 'North Beach parking lot', 'Beach Cleanup', '2026-01-05', '09:00', '12:00', 180, 'Start the year with a beach cleanup.', 'Gloves, bags, pickers provided', 'Wear sturdy shoes, bring water'),
('Summer Riverbank Clean', 22, 'South River Park entrance', 'River Cleanup', '2026-01-12', '10:00', '14:00', 240, 'Summer cleanup of riverbank.', 'Gloves, waders available', 'Be careful near water, sun protection'),
('Central Park Maintenance', 23, 'Main Pavilion area', 'Park Cleanup', '2026-01-18', '13:00', '16:00', 180, 'Maintain central park areas.', 'Bags and gloves provided', 'Stay hydrated, watch for children'),
('Eastside Trail Clearance', 24, 'Eastside trailhead', 'Trail Maintenance', '2026-01-25', '09:30', '13:30', 240, 'Clear winter debris from trails.', 'Tools provided', 'Stay on marked trails'),
('Harbor Front Cleanup', 25, 'Marina boat ramp', 'Harbor Cleanup', '2026-01-28', '14:00', '17:00', 180, 'Clean harbor front area.', 'Bags, gloves, grabbers', 'Be aware of boat traffic'),
('West Creek Restoration', 21, 'West Creek bridge', 'Creek Cleanup', '2026-02-02', '09:00', '12:00', 180, 'Restore West Creek area.', 'All supplies provided', 'Uneven ground, wear boots'),
('Mountain Vista Trail Day', 22, 'Lower trail parking', 'Trail Cleanup', '2026-02-08', '08:00', '12:00', 240, 'Clean mountain trails.', 'Trail tools provided', 'Strenuous activity, bring lunch'),
('Community Garden Prep', 23, 'Garden shed', 'Garden Maintenance', '2026-02-14', '10:00', '14:00', 240, 'Prepare garden for spring.', 'Gardening tools available', 'Bring gardening gloves'),
('Railway Walk Cleanup', 24, 'Old station building', 'Path Cleanup', '2026-02-18', '13:00', '16:00', 180, 'Clean railway walking path.', 'Bags and gloves', 'Watch for uneven surfaces'),
('Sunset Beach Cleanup', 25, 'Lighthouse viewing area', 'Beach Cleanup', '2026-02-22', '09:00', '13:00', 240, 'Clean sunset beach area.', 'Beach cleanup equipment', 'Protect nesting areas'),

-- Upcoming Events (March - June 2026) - event_ids 11-25
('North Beach Spring Clean', 21, 'North Beach parking lot', 'Beach Cleanup', '2026-03-15', '09:00', '12:00', 180, 'Spring beach cleanup event.', 'Gloves, bags, pickers provided', 'Wear sturdy shoes, bring water, sun protection'),
('Riverbank Restoration', 22, 'South River Park entrance', 'River Cleanup', '2026-03-22', '10:00', '14:00', 240, 'Restore riverbank areas.', 'Gloves, waders available', 'Be careful near water, wear old clothes'),
('Central Park Picnic Cleanup', 23, 'Main Pavilion area', 'Park Cleanup', '2026-03-29', '13:00', '16:00', 180, 'Clean up after picnic-goers.', 'Bags and gloves provided', 'Stay hydrated, watch for children playing'),
('Eastside Trail Maintenance', 24, 'Eastside trailhead', 'Trail Maintenance', '2026-04-05', '09:30', '13:30', 240, 'Maintain trails and remove debris.', 'Tools provided, bring gloves', 'Stay on marked trails, watch for wildlife'),
('Harbor Front Cleanup', 25, 'Marina boat ramp', 'Harbor Cleanup', '2026-04-12', '14:00', '17:00', 180, 'Clean the harbor front area.', 'Bags, gloves, grabbers', 'Be aware of boat traffic, wear bright colors'),
('West Creek Spring Clean', 21, 'West Creek bridge', 'Creek Cleanup', '2026-04-19', '09:00', '12:00', 180, 'Spring cleaning of West Creek.', 'All supplies provided', 'Uneven ground, wear boots'),
('Mountain Vista Trail Day', 22, 'Lower trail parking', 'Trail Cleanup', '2026-04-26', '08:00', '12:00', 240, 'Clean mountain trails.', 'Trail tools provided', 'Strenuous activity, bring lunch'),
('Community Garden Work Day', 23, 'Garden shed', 'Garden Maintenance', '2026-05-03', '10:00', '14:00', 240, 'Help maintain community garden.', 'Gardening tools available', 'Bring gardening gloves, sunscreen'),
('Railway Walk Cleanup', 24, 'Old station building', 'Path Cleanup', '2026-05-10', '13:00', '16:00', 180, 'Clean the railway walking path.', 'Bags and gloves', 'Watch for uneven surfaces'),
('Sunset Beach Conservation', 25, 'Lighthouse viewing area', 'Beach Cleanup', '2026-05-17', '09:00', '13:00', 240, 'Conserve sunset beach area.', 'Beach cleanup equipment', 'Protect nesting areas, follow guide'),
('North Beach Dune Restoration', 21, 'North Beach dunes', 'Dune Restoration', '2026-05-24', '09:00', '12:00', 180, 'Restore dune ecosystems.', 'Planting tools provided', 'Learn about native dune plants'),
('Riverbank Plastic Hunt', 22, 'South River canoe launch', 'Plastic Collection', '2026-05-31', '10:00', '13:00', 180, 'Hunt for plastic waste.', 'Specialized collection bags', 'Wear boots for muddy areas'),
('Central Park Pond Cleanup', 23, 'Pond near playground', 'Pond Cleanup', '2026-06-07', '13:00', '16:00', 180, 'Clean the pond area.', 'Netting equipment', 'Stay away from water edge'),
('Eastside Invasive Removal', 24, 'Forest interior trail', 'Invasive Species', '2026-06-14', '09:30', '12:30', 180, 'Remove invasive plant species.', 'Removal tools provided', 'Learn to identify invasive species'),
('Harbor Marine Debris', 25, 'Pier 3', 'Marine Debris', '2026-06-21', '14:00', '17:00', 180, 'Collect marine debris.', 'Marine collection gear', 'Life jackets provided');

-- Insert event registrations for PAST events (event_ids 1-10) with attendance status
INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at) VALUES
-- Event 1 (Jan 5)
(1, 1, 'attended', '2025-12-15 10:00:00'), (1, 2, 'attended', '2025-12-16 11:30:00'), 
(1, 3, 'attended', '2025-12-17 09:15:00'), (1, 4, 'attended', '2025-12-18 14:20:00'),
(1, 5, 'no_show', '2025-12-19 08:45:00'), (1, 6, 'attended', '2025-12-20 16:30:00'),
(1, 7, 'attended', '2025-12-21 10:10:00'), (1, 8, 'attended', '2025-12-22 13:40:00'),
-- Event 2 (Jan 12)
(2, 9, 'attended', '2025-12-20 09:00:00'), (2, 10, 'attended', '2025-12-21 11:20:00'),
(2, 11, 'attended', '2025-12-22 14:15:00'), (2, 12, 'attended', '2025-12-23 10:30:00'),
(2, 13, 'attended', '2025-12-24 09:45:00'), (2, 14, 'no_show', '2025-12-25 15:00:00'),
(2, 15, 'attended', '2025-12-26 11:00:00'), (2, 16, 'attended', '2025-12-27 13:30:00'),
-- Event 3 (Jan 18)
(3, 17, 'attended', '2025-12-28 10:20:00'), (3, 18, 'attended', '2025-12-29 14:40:00'),
(3, 19, 'attended', '2025-12-30 09:10:00'), (3, 20, 'attended', '2025-12-31 16:00:00'),
(3, 1, 'attended', '2026-01-02 08:30:00'), (3, 2, 'attended', '2026-01-03 12:15:00'),
-- Event 4 (Jan 25)
(4, 3, 'attended', '2026-01-04 10:45:00'), (4, 4, 'attended', '2026-01-05 13:20:00'),
(4, 5, 'attended', '2026-01-06 09:30:00'), (4, 6, 'attended', '2026-01-07 15:50:00'),
(4, 7, 'attended', '2026-01-08 11:40:00'), (4, 8, 'attended', '2026-01-09 14:10:00'),
-- Event 5 (Jan 28)
(5, 9, 'attended', '2026-01-10 10:00:00'), (5, 10, 'attended', '2026-01-11 13:45:00'),
(5, 11, 'attended', '2026-01-12 09:20:00'), (5, 12, 'attended', '2026-01-13 16:30:00'),
(5, 13, 'attended', '2026-01-14 10:15:00'), (5, 14, 'attended', '2026-01-15 14:30:00'),
-- Event 6 (Feb 2)
(6, 15, 'attended', '2026-01-16 08:45:00'), (6, 16, 'attended', '2026-01-17 12:00:00'),
(6, 17, 'attended', '2026-01-18 09:30:00'), (6, 18, 'attended', '2026-01-19 15:20:00'),
(6, 19, 'attended', '2026-01-20 11:10:00'), (6, 20, 'attended', '2026-01-21 13:40:00'),
-- Event 7 (Feb 8)
(7, 1, 'attended', '2026-01-22 10:30:00'), (7, 2, 'attended', '2026-01-23 14:15:00'),
(7, 3, 'attended', '2026-01-24 09:00:00'), (7, 4, 'attended', '2026-01-25 16:20:00'),
(7, 5, 'attended', '2026-01-26 10:45:00'), (7, 6, 'attended', '2026-01-27 13:30:00'),
-- Event 8 (Feb 14)
(8, 7, 'attended', '2026-01-28 09:15:00'), (8, 8, 'attended', '2026-01-29 15:40:00'),
(8, 9, 'attended', '2026-01-30 11:00:00'), (8, 10, 'attended', '2026-01-31 14:20:00'),
(8, 11, 'attended', '2026-02-01 10:10:00'), (8, 12, 'attended', '2026-02-02 13:50:00'),
-- Event 9 (Feb 18)
(9, 13, 'attended', '2026-02-03 09:30:00'), (9, 14, 'attended', '2026-02-04 16:00:00'),
(9, 15, 'attended', '2026-02-05 11:45:00'), (9, 16, 'attended', '2026-02-06 10:00:00'),
(9, 17, 'attended', '2026-02-07 14:30:00'), (9, 18, 'attended', '2026-02-08 09:20:00'),
-- Event 10 (Feb 22)
(10, 19, 'attended', '2026-02-09 15:10:00'), (10, 20, 'attended', '2026-02-10 11:30:00'),
(10, 1, 'attended', '2026-02-11 13:45:00'), (10, 2, 'attended', '2026-02-12 10:20:00'),
(10, 3, 'attended', '2026-02-13 16:30:00'), (10, 4, 'attended', '2026-02-14 09:00:00');

-- Insert event registrations for UPCOMING events (event_ids 11-25) with 'registered' status
INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at) VALUES
(11, 5, 'registered', '2026-02-15 12:15:00'), (11, 6, 'registered', '2026-02-16 14:40:00'), (11, 7, 'registered', '2026-02-17 10:30:00'),
(12, 8, 'registered', '2026-02-18 09:00:00'), (12, 9, 'registered', '2026-02-19 11:20:00'), (12, 10, 'registered', '2026-02-20 14:15:00'),
(13, 11, 'registered', '2026-02-21 10:30:00'), (13, 12, 'registered', '2026-02-22 09:45:00'), (13, 13, 'registered', '2026-02-23 15:00:00'),
(14, 14, 'registered', '2026-02-24 11:00:00'), (14, 15, 'registered', '2026-02-25 13:30:00'), (14, 16, 'registered', '2026-02-26 10:20:00'),
(15, 17, 'registered', '2026-02-27 14:40:00'), (15, 18, 'registered', '2026-02-28 09:10:00'), (15, 19, 'registered', '2026-03-01 16:00:00'),
(16, 20, 'registered', '2026-03-02 08:30:00'), (16, 1, 'registered', '2026-03-03 12:15:00'), (16, 2, 'registered', '2026-03-04 10:45:00'),
(17, 3, 'registered', '2026-03-05 13:20:00'), (17, 4, 'registered', '2026-03-06 09:30:00'), (17, 5, 'registered', '2026-03-07 15:50:00'),
(18, 6, 'registered', '2026-03-08 11:40:00'), (18, 7, 'registered', '2026-03-09 14:10:00'), (18, 8, 'registered', '2026-03-10 10:00:00'),
(19, 9, 'registered', '2026-03-11 13:45:00'), (19, 10, 'registered', '2026-03-12 09:20:00'), (19, 11, 'registered', '2026-03-13 16:30:00'),
(20, 12, 'registered', '2026-03-14 10:15:00'), (20, 13, 'registered', '2026-03-15 14:30:00'), (20, 14, 'registered', '2026-03-16 08:45:00'),
(21, 15, 'registered', '2026-03-17 12:00:00'), (21, 16, 'registered', '2026-03-18 09:30:00'), (21, 17, 'registered', '2026-03-19 15:20:00'),
(22, 18, 'registered', '2026-03-20 11:10:00'), (22, 19, 'registered', '2026-03-21 13:40:00'), (22, 20, 'registered', '2026-03-22 10:30:00'),
(23, 1, 'registered', '2026-03-23 14:15:00'), (23, 2, 'registered', '2026-03-24 09:00:00'), (23, 3, 'registered', '2026-03-25 16:20:00'),
(24, 4, 'registered', '2026-03-26 10:45:00'), (24, 5, 'registered', '2026-03-27 13:30:00'), (24, 6, 'registered', '2026-03-28 09:15:00'),
(25, 7, 'registered', '2026-03-29 15:40:00'), (25, 8, 'registered', '2026-03-30 11:00:00'), (25, 9, 'registered', '2026-03-31 14:20:00');

-- Insert event outcomes for PAST events (event_ids 1-10)
INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by, recorded_at) VALUES
(1, 7, 25, 18, 'Removed large debris from beach. Found and disposed of fishing line.', 21, '2026-01-05 15:30:00'),
(2, 7, 32, 22, 'Cleared 200m of riverbank. Removed shopping trolley from water.', 22, '2026-01-12 16:45:00'),
(3, 6, 18, 12, 'Cleaned playground area. Planted 10 native shrubs.', 23, '2026-01-18 17:20:00'),
(4, 6, 22, 15, 'Cleared fallen branches from 3km of trail. Repaired trail markers.', 24, '2026-01-25 14:10:00'),
(5, 6, 28, 20, 'Cleaned marina area. Collected hazardous materials for proper disposal.', 25, '2026-01-28 18:00:00'),
(6, 6, 19, 13, 'Removed debris from creek. Documented water quality samples.', 21, '2026-02-02 13:45:00'),
(7, 6, 15, 10, 'Cleaned summit area. Removed graffiti from lookout points.', 22, '2026-02-08 15:20:00'),
(8, 6, 12, 8, 'Prepared 15 garden beds for spring planting. Built new compost bin.', 23, '2026-02-14 16:30:00'),
(9, 6, 21, 16, 'Cleaned 2km of railway path. Repaired 3 benches along the route.', 24, '2026-02-18 17:10:00'),
(10, 6, 30, 24, 'Removed driftwood and debris from beach. Protected nesting sites.', 25, '2026-02-22 14:50:00');

-- Insert feedback for PAST events (event_ids 1-10)
INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at) VALUES
(1, 1, 5, 'Great start to the year! Beach looks fantastic.', '2026-01-06 18:30:00'),
(1, 2, 4, 'Well organized, will definitely join again.', '2026-01-06 19:15:00'),
(1, 3, 5, 'Loved the community spirit!', '2026-01-07 08:20:00'),
(1, 4, 5, 'Great turnout for January!', '2026-01-07 09:45:00'),
(1, 6, 4, 'Good organization, nice weather helped.', '2026-01-08 17:30:00'),
(1, 7, 5, 'Beach is so clean now!', '2026-01-08 20:10:00'),
(1, 8, 5, 'Wonderful experience, met great people.', '2026-01-09 10:15:00'),
(2, 9, 5, 'River looks beautiful again!', '2026-01-13 17:45:00'),
(2, 10, 4, 'Good organization, will come again.', '2026-01-13 20:10:00'),
(2, 11, 5, 'Great to see so many volunteers!', '2026-01-14 09:30:00'),
(2, 12, 5, 'Found so much trash but river is cleaner now.', '2026-01-14 16:20:00'),
(2, 13, 4, 'Well organized event.', '2026-01-15 11:45:00'),
(2, 15, 5, 'Amazing what we accomplished!', '2026-01-15 19:30:00'),
(2, 16, 5, 'Great team effort!', '2026-01-16 08:15:00'),
(3, 17, 4, 'Park looks much better now.', '2026-01-19 18:00:00'),
(3, 18, 5, 'Fun activity for a Saturday!', '2026-01-19 20:45:00'),
(3, 19, 5, 'Kids loved helping out.', '2026-01-20 09:20:00'),
(3, 20, 4, 'Good organization, plenty of supplies.', '2026-01-20 15:30:00'),
(3, 1, 5, 'Great community event!', '2026-01-21 17:45:00'),
(3, 2, 5, 'Park is pristine now!', '2026-01-21 19:10:00'),
(4, 3, 5, 'Trails are now clear and safe.', '2026-01-26 16:30:00'),
(4, 4, 4, 'Good workout and good cause!', '2026-01-26 19:20:00'),
(4, 5, 5, 'Beautiful trail maintenance day.', '2026-01-27 10:30:00'),
(4, 6, 5, 'Love seeing the trails cared for.', '2026-01-27 14:45:00'),
(4, 7, 4, 'Well organized trail day.', '2026-01-28 09:15:00'),
(4, 8, 5, 'Great team, great results!', '2026-01-28 17:50:00'),
(5, 9, 5, 'Harbor looks fantastic!', '2026-01-29 17:10:00'),
(5, 10, 5, 'Professional organization, felt safe.', '2026-01-29 21:00:00'),
(5, 11, 4, 'Good cleanup event.', '2026-01-30 11:30:00'),
(5, 12, 5, 'Marina area is spotless now.', '2026-01-30 16:45:00'),
(5, 13, 5, 'Great turnout for January!', '2026-01-31 09:20:00'),
(5, 14, 4, 'Well organized, good leadership.', '2026-01-31 14:30:00'),
(6, 15, 5, 'Creek is much cleaner now.', '2026-02-03 18:15:00'),
(6, 16, 4, 'Good event, muddy but fun.', '2026-02-03 20:30:00'),
(6, 17, 5, 'Great to see the creek cared for.', '2026-02-04 10:45:00'),
(6, 18, 5, 'Found lots of plastic unfortunately.', '2026-02-04 16:20:00'),
(6, 19, 4, 'Well organized creek cleanup.', '2026-02-05 09:30:00'),
(6, 20, 5, 'Beautiful day for creek cleaning!', '2026-02-05 15:40:00'),
(7, 1, 5, 'Mountain views AND helping environment!', '2026-02-09 17:30:00'),
(7, 2, 5, 'Challenging hike but worth it.', '2026-02-09 19:45:00'),
(7, 3, 4, 'Great workout for a good cause.', '2026-02-10 11:15:00'),
(7, 4, 5, 'Summit looks pristine now.', '2026-02-10 16:30:00'),
(7, 5, 5, 'Amazing what we collected!', '2026-02-11 09:50:00'),
(7, 6, 4, 'Well organized mountain cleanup.', '2026-02-11 14:20:00'),
(8, 7, 5, 'Garden looks ready for spring!', '2026-02-15 17:20:00'),
(8, 8, 4, 'Good garden prep day.', '2026-02-15 19:30:00'),
(8, 9, 5, 'Love our community garden!', '2026-02-16 10:45:00'),
(8, 10, 5, 'Great to prepare for planting.', '2026-02-16 15:50:00'),
(8, 11, 4, 'Well organized garden day.', '2026-02-17 09:15:00'),
(8, 12, 5, 'New compost bin is great!', '2026-02-17 16:30:00'),
(9, 13, 5, 'Railway walk is beautiful now.', '2026-02-19 18:00:00'),
(9, 14, 4, 'Good cleanup along the path.', '2026-02-19 20:15:00'),
(9, 15, 5, 'Love this historic railway!', '2026-02-20 11:30:00'),
(9, 16, 5, 'Benches look great repaired.', '2026-02-20 16:45:00'),
(9, 17, 4, 'Well organized path cleanup.', '2026-02-21 10:10:00'),
(9, 18, 5, 'Great community effort!', '2026-02-21 15:20:00'),
(10, 19, 5, 'Sunset Beach is pristine!', '2026-02-23 17:40:00'),
(10, 20, 5, 'Protected nesting areas carefully.', '2026-02-23 19:50:00'),
(10, 1, 4, 'Good beach cleanup event.', '2026-02-24 11:25:00'),
(10, 2, 5, 'Beautiful day at the beach!', '2026-02-24 15:30:00'),
(10, 3, 5, 'Found lots of plastic unfortunately.', '2026-02-25 09:45:00'),
(10, 4, 5, 'Great team, great results!', '2026-02-25 14:10:00');

-- Verify counts
SELECT 'users' as table_name, COUNT(*) as count FROM users UNION ALL
SELECT 'events', COUNT(*) FROM events UNION ALL
SELECT 'eventregistrations', COUNT(*) FROM eventregistrations UNION ALL
SELECT 'feedback', COUNT(*) FROM feedback UNION ALL
SELECT 'eventoutcomes', COUNT(*) FROM eventoutcomes;