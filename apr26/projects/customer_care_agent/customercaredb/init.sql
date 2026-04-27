-- ============================================================
-- Customer Care Database - Queries & Resolutions
-- Includes Electronics product support data
-- ============================================================

-- ─────────────────────────────────────────────
-- ENUMS
-- ─────────────────────────────────────────────
CREATE TYPE ticket_status AS ENUM ('open', 'in_progress', 'resolved', 'closed', 'escalated');
CREATE TYPE ticket_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE ticket_category AS ENUM (
    'product_defect',
    'warranty_claim',
    'installation_support',
    'software_issue',
    'shipping_damage',
    'returns_refunds',
    'billing',
    'general_inquiry'
);
CREATE TYPE channel AS ENUM ('email', 'phone', 'chat', 'in_store', 'social_media');

-- ─────────────────────────────────────────────
-- PRODUCT CATALOG (Electronics)
-- ─────────────────────────────────────────────
CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    sku             VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(255) NOT NULL,
    category        VARCHAR(100) NOT NULL,
    brand           VARCHAR(100) NOT NULL,
    model_number    VARCHAR(100),
    warranty_months INT DEFAULT 12,
    price           NUMERIC(10, 2),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO products (sku, name, category, brand, model_number, warranty_months, price) VALUES
('TV-SAM-65Q80C',    'Samsung 65" QLED 4K Smart TV',          'Television',     'Samsung',  'QN65Q80C',   24, 129999.00),
('TV-LG-55C3',       'LG 55" OLED evo C3 4K TV',              'Television',     'LG',       'OLED55C3PSA',24,  99999.00),
('LAP-DEL-XPS15',    'Dell XPS 15 Laptop (i9, 32GB, 1TB)',     'Laptop',         'Dell',     'XPS9530',    12,  189999.00),
('LAP-APL-MBP14',    'Apple MacBook Pro 14" M3 Pro',           'Laptop',         'Apple',    'MBP14M3',    12,  219999.00),
('PHN-SAM-S24U',     'Samsung Galaxy S24 Ultra 256GB',         'Smartphone',     'Samsung',  'SM-S928B',   12,  129999.00),
('PHN-APL-IP15P',    'Apple iPhone 15 Pro 256GB',              'Smartphone',     'Apple',    'A3101',      12,  134900.00),
('HDP-SNY-WH1000',   'Sony WH-1000XM5 Wireless Headphones',   'Audio',          'Sony',     'WH-1000XM5', 12,   29999.00),
('HDP-BOZ-QC45',     'Bose QuietComfort 45 Headphones',        'Audio',          'Bose',     'QC45',       12,   32999.00),
('TAB-APL-IPADP13',  'Apple iPad Pro 13" M4 WiFi 256GB',       'Tablet',         'Apple',    'MXFQ3HN/A',  12,  119900.00),
('TAB-SAM-S9P',      'Samsung Galaxy Tab S9+ 256GB',           'Tablet',         'Samsung',  'SM-X810',    12,   89999.00),
('WCH-APL-AW9',      'Apple Watch Series 9 45mm GPS',          'Wearable',       'Apple',    'MR9A3HN/A',  12,   45900.00),
('WCH-SAM-GW6',      'Samsung Galaxy Watch 6 Classic 47mm',    'Wearable',       'Samsung',  'SM-R960',    12,   34999.00),
('CAM-SNY-A7M4',     'Sony Alpha A7 IV Full Frame Mirrorless', 'Camera',         'Sony',     'ILCE-7M4',   24,  259999.00),
('RTR-ASS-AX6000',   'ASUS RT-AX6000 WiFi 6 Router',           'Networking',     'ASUS',     'RT-AX6000',  12,   19999.00),
('SSD-SAM-T7',       'Samsung T7 Portable SSD 2TB',            'Storage',        'Samsung',  'MU-PC2T0T',  36,   12999.00);

-- ─────────────────────────────────────────────
-- CUSTOMERS
-- ─────────────────────────────────────────────
CREATE TABLE customers (
    customer_id   SERIAL PRIMARY KEY,
    full_name     VARCHAR(255) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    phone         VARCHAR(20),
    city          VARCHAR(100),
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO customers (full_name, email, phone, city) VALUES
('Arjun Sharma',     'arjun.sharma@email.com',   '+91-9876543210', 'Hyderabad'),
('Priya Nair',       'priya.nair@email.com',      '+91-9823456789', 'Bangalore'),
('Rahul Mehta',      'rahul.mehta@email.com',     '+91-9712345678', 'Mumbai'),
('Sneha Reddy',      'sneha.reddy@email.com',      '+91-9645321870', 'Hyderabad'),
('Vikram Patel',     'vikram.patel@email.com',    '+91-9534218760', 'Ahmedabad'),
('Anjali Iyer',      'anjali.iyer@email.com',     '+91-9421987650', 'Chennai'),
('Kiran Rao',        'kiran.rao@email.com',        '+91-9398765430', 'Pune'),
('Deepak Gupta',     'deepak.gupta@email.com',    '+91-9287654320', 'Delhi'),
('Meena Krishnan',   'meena.krishnan@email.com',  '+91-9176543210', 'Kochi'),
('Suresh Babu',      'suresh.babu@email.com',     '+91-9065432100', 'Vizag');

-- ─────────────────────────────────────────────
-- AGENTS (Customer Care Staff)
-- ─────────────────────────────────────────────
CREATE TABLE agents (
    agent_id    SERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    department  VARCHAR(100) DEFAULT 'Customer Care',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO agents (full_name, email, department) VALUES
('Ravi Kumar',      'ravi.kumar@support.com',     'Tier 1 Support'),
('Lakshmi Devi',    'lakshmi.devi@support.com',   'Tier 1 Support'),
('Naveen Raj',      'naveen.raj@support.com',      'Tier 2 Support'),
('Pooja Menon',     'pooja.menon@support.com',    'Tier 2 Support'),
('Aditya Singh',    'aditya.singh@support.com',   'Escalations');

-- ─────────────────────────────────────────────
-- SUPPORT TICKETS
-- ─────────────────────────────────────────────
CREATE TABLE tickets (
    ticket_id       SERIAL PRIMARY KEY,
    ticket_ref      VARCHAR(20) UNIQUE NOT NULL,   -- e.g. TKT-2024-00001
    customer_id     INT REFERENCES customers(customer_id),
    product_id      INT REFERENCES products(product_id),
    agent_id        INT REFERENCES agents(agent_id),
    channel         channel NOT NULL DEFAULT 'email',
    category        ticket_category NOT NULL,
    priority        ticket_priority NOT NULL DEFAULT 'medium',
    status          ticket_status NOT NULL DEFAULT 'open',
    subject         VARCHAR(500) NOT NULL,
    description     TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    resolved_at     TIMESTAMPTZ
);

-- ─────────────────────────────────────────────
-- RESOLUTIONS
-- ─────────────────────────────────────────────
CREATE TABLE resolutions (
    resolution_id       SERIAL PRIMARY KEY,
    ticket_id           INT UNIQUE REFERENCES tickets(ticket_id),
    resolved_by         INT REFERENCES agents(agent_id),
    resolution_summary  TEXT NOT NULL,
    root_cause          TEXT,
    action_taken        TEXT NOT NULL,
    refund_issued       BOOLEAN DEFAULT FALSE,
    refund_amount       NUMERIC(10, 2),
    replacement_issued  BOOLEAN DEFAULT FALSE,
    customer_rating     SMALLINT CHECK (customer_rating BETWEEN 1 AND 5),
    resolved_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- TICKET COMMENTS / ACTIVITY LOG
-- ─────────────────────────────────────────────
CREATE TABLE ticket_comments (
    comment_id  SERIAL PRIMARY KEY,
    ticket_id   INT REFERENCES tickets(ticket_id),
    agent_id    INT REFERENCES agents(agent_id),  -- NULL = customer comment
    is_internal BOOLEAN DEFAULT FALSE,             -- internal agent notes
    body        TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- SEED: SUPPORT TICKETS (Electronics)
-- ─────────────────────────────────────────────
INSERT INTO tickets
    (ticket_ref, customer_id, product_id, agent_id, channel, category, priority, status, subject, description, created_at, resolved_at)
VALUES
-- 1: TV dead pixels
('TKT-2024-00001', 1, 1, 1, 'email', 'product_defect', 'high', 'resolved',
 'Dead pixels appearing on Samsung 65" QLED TV',
 'I purchased the Samsung 65" QLED 4K Smart TV 3 weeks ago. I noticed a cluster of dead pixels in the centre of the screen that are very distracting during movies. The TV is used normally and has not been dropped or damaged.',
 NOW() - INTERVAL '30 days', NOW() - INTERVAL '25 days'),

-- 2: MacBook battery drain
('TKT-2024-00002', 2, 4, 2, 'chat', 'product_defect', 'medium', 'resolved',
 'MacBook Pro 14" M3 Pro battery draining very fast',
 'My MacBook Pro 14" M3 Pro is only 2 months old. Battery life has dropped from 18 hours to under 4 hours after the latest macOS update. I have tried resetting SMC but the issue persists.',
 NOW() - INTERVAL '20 days', NOW() - INTERVAL '15 days'),

-- 3: Samsung S24 Ultra overheating
('TKT-2024-00003', 3, 5, 3, 'phone', 'product_defect', 'high', 'resolved',
 'Galaxy S24 Ultra overheating during normal use',
 'My Samsung Galaxy S24 Ultra gets uncomfortably hot even when browsing the web or watching YouTube. The back of the phone becomes very warm to touch. Battery is also draining faster than expected.',
 NOW() - INTERVAL '15 days', NOW() - INTERVAL '10 days'),

-- 4: Sony headphones not pairing
('TKT-2024-00004', 4, 7, 1, 'chat', 'software_issue', 'medium', 'resolved',
 'Sony WH-1000XM5 headphones not pairing with laptop',
 'The Sony WH-1000XM5 headphones are not pairing with my Dell laptop. They connect fine with my phone. I have cleared all Bluetooth devices and tried re-pairing from scratch multiple times.',
 NOW() - INTERVAL '10 days', NOW() - INTERVAL '7 days'),

-- 5: iPad Pro screen crack on delivery
('TKT-2024-00005', 5, 9, 4, 'email', 'shipping_damage', 'critical', 'resolved',
 'iPad Pro 13" delivered with cracked screen',
 'I received the Apple iPad Pro 13" M4 today. When I opened the box, the screen had a visible crack running from the top-right corner diagonally across. The box appeared undamaged on the outside. I have photos of the packaging and device.',
 NOW() - INTERVAL '8 days', NOW() - INTERVAL '5 days'),

-- 6: LG OLED burn-in concern
('TKT-2024-00006', 6, 2, 2, 'email', 'general_inquiry', 'low', 'resolved',
 'Concerned about OLED burn-in on LG 55" C3',
 'I have been using the LG OLED C3 for 4 months. I am concerned about burn-in as I sometimes leave news channels with static logos on for extended periods. Can you advise on settings to prevent this and whether my usage has caused any damage?',
 NOW() - INTERVAL '7 days', NOW() - INTERVAL '4 days'),

-- 7: Dell XPS 15 warranty claim
('TKT-2024-00007', 7, 3, 5, 'phone', 'warranty_claim', 'high', 'escalated',
 'Dell XPS 15 motherboard failure - warranty replacement request',
 'My Dell XPS 15 (purchased 8 months ago) stopped powering on completely yesterday. No physical damage has occurred. I suspect a motherboard failure. I am requesting a warranty replacement as this is clearly a manufacturing defect.',
 NOW() - INTERVAL '5 days', NULL),

-- 8: Apple Watch not tracking heart rate
('TKT-2024-00008', 8, 11, 1, 'chat', 'software_issue', 'medium', 'in_progress',
 'Apple Watch Series 9 heart rate not tracking accurately',
 'My Apple Watch Series 9 has been showing wildly inaccurate heart rate readings for the past week. During a run it showed 210 BPM when I was barely jogging. I have updated to the latest watchOS and the issue continues.',
 NOW() - INTERVAL '3 days', NULL),

-- 9: Bose QC45 one side not working
('TKT-2024-00009', 9, 8, 3, 'phone', 'product_defect', 'high', 'in_progress',
 'Bose QC45 left ear cup producing no sound',
 'The left ear cup of my Bose QuietComfort 45 headphones stopped producing audio suddenly. I have tried different cables, devices, and audio sources. The right ear works perfectly. The headphones are 5 months old and well within warranty.',
 NOW() - INTERVAL '2 days', NULL),

-- 10: Samsung T7 SSD not recognised
('TKT-2024-00010', 10, 15, 2, 'email', 'product_defect', 'medium', 'open',
 'Samsung T7 2TB SSD not detected on Windows 11',
 'My brand new Samsung T7 Portable SSD 2TB is not being recognised by my Windows 11 PC. It does not appear in Device Manager or Disk Management. I have tried multiple USB ports and two different cables. The LED on the drive blinks once and then nothing.',
 NOW() - INTERVAL '1 day', NULL);

-- ─────────────────────────────────────────────
-- SEED: RESOLUTIONS
-- ─────────────────────────────────────────────
INSERT INTO resolutions
    (ticket_id, resolved_by, resolution_summary, root_cause, action_taken, refund_issued, refund_amount, replacement_issued, customer_rating, resolved_at)
VALUES
-- TKT-2024-00001: Dead pixels → replacement
(1, 1,
 'Panel replaced under warranty after dead pixel cluster confirmed during remote diagnostics.',
 'Manufacturing defect in LCD panel — dead pixel cluster identified in central zone.',
 'Technician visit arranged within 48 hours. Replacement panel installed on-site. Full functionality verified post-repair.',
 FALSE, NULL, FALSE, 5, NOW() - INTERVAL '25 days'),

-- TKT-2024-00002: MacBook battery drain → software fix
(2, 2,
 'Battery drain caused by macOS Sonoma 14.2 background process bug. Issue resolved after Apple released patch 14.2.1.',
 'Known macOS bug causing kernel_task to consume excessive CPU and drain battery after wake from sleep.',
 'Guided customer to install macOS 14.2.1 patch. Advised to reset NVRAM. Battery performance restored to 16+ hours. Followed up after 3 days — customer confirmed resolution.',
 FALSE, NULL, FALSE, 4, NOW() - INTERVAL '15 days'),

-- TKT-2024-00003: S24 Ultra overheating → settings + patch
(3, 3,
 'Overheating traced to aggressive background app refresh and pre-release carrier settings. Resolved after factory settings reset and Samsung firmware update.',
 'Combination of third-party app running background location services continuously and outdated baseband firmware causing CPU throttling to malfunction.',
 'Remote session conducted. Identified rogue app consuming background resources. Uninstalled app, updated firmware to latest build, adjusted thermal management settings in Developer Options. Customer monitored device for 5 days — no further issues.',
 FALSE, NULL, FALSE, 5, NOW() - INTERVAL '10 days'),

-- TKT-2024-00004: Sony headphones pairing issue → driver fix
(4, 1,
 'Bluetooth pairing issue resolved by updating Windows Bluetooth driver and clearing Sony headphone firmware cache.',
 'Incompatibility between Sony WH-1000XM5 firmware v2.2.1 and Microsoft Bluetooth stack update KB5032189.',
 'Guided customer to roll back Windows Bluetooth driver to version 22.90.0. Also performed headphone factory reset (hold power button 7 seconds). Successfully paired on first attempt thereafter.',
 FALSE, NULL, FALSE, 4, NOW() - INTERVAL '7 days'),

-- TKT-2024-00005: iPad cracked screen on delivery → replacement
(5, 4,
 'Full replacement unit dispatched after shipping damage confirmed via customer-provided photos.',
 'Inadequate padding in courier packaging during last-mile delivery resulted in screen crack.',
 'Customer photos reviewed and damage verified within 2 hours. Replacement iPad Pro 13" M4 256GB dispatched same day with priority courier. Return pickup of damaged unit arranged. Courier partner notified for packaging review.',
 FALSE, NULL, TRUE, 5, NOW() - INTERVAL '5 days'),

-- TKT-2024-00006: OLED burn-in concern → education + settings
(6, 2,
 'No burn-in detected. Customer educated on OLED care and optimal settings configured remotely.',
 'Customer was unaware of built-in OLED Care features and had disabled pixel refresher.',
 'Ran remote diagnostics — no burn-in detected (uniform panel response across all zones). Walked customer through enabling Pixel Refresher (runs every 4 hours), setting Logo Luminance Adjustment to High, enabling Screen Saver after 2 minutes, and reducing peak brightness on static content. Shared LG OLED care guide PDF.',
 FALSE, NULL, FALSE, 5, NOW() - INTERVAL '4 days');

-- ─────────────────────────────────────────────
-- SEED: TICKET COMMENTS
-- ─────────────────────────────────────────────
INSERT INTO ticket_comments (ticket_id, agent_id, is_internal, body, created_at) VALUES
-- TKT-2024-00007: Dell XPS escalation notes
(7, 3, TRUE,  'Initial diagnosis: customer performed power drain (hold power 30s). No response. Suspect mobo failure. Escalating to Tier 2.', NOW() - INTERVAL '5 days'),
(7, 5, TRUE,  'Tier 2 review: confirmed out-of-scope for remote fix. Initiating warranty claim with Dell service centre. Awaiting Dell case number.', NOW() - INTERVAL '4 days'),
(7, 5, FALSE, 'Hi, we have raised a warranty claim with Dell (Case #DL-2024-88421). A Dell technician will contact you within 2 business days to arrange pickup and inspection. We will keep you updated.', NOW() - INTERVAL '4 days'),

-- TKT-2024-00008: Apple Watch in_progress
(8, 1, FALSE, 'Thank you for reaching out. Could you confirm which wrist you wear the watch on and whether you have a tattoo on that wrist? Some tattoos can interfere with optical heart rate sensors.', NOW() - INTERVAL '3 days'),
(8, 1, TRUE,  'Customer confirmed no tattoos. Watch worn on left wrist. Advising sensor cleaning and watchOS reinstall next.', NOW() - INTERVAL '2 days'),

-- TKT-2024-00009: Bose QC45 in_progress
(9, 3, FALSE, 'Thank you for contacting us. We have confirmed your Bose QC45 is within the 1-year warranty period. We are arranging a replacement pair to be dispatched. You will receive a tracking number within 24 hours.', NOW() - INTERVAL '2 days'),
(9, 3, TRUE,  'Replacement unit reserved in warehouse. Awaiting logistics confirmation before sending tracking to customer.', NOW() - INTERVAL '1 day');

-- ─────────────────────────────────────────────
-- USEFUL VIEWS
-- ─────────────────────────────────────────────

-- Full ticket overview with customer and product info
CREATE VIEW v_ticket_overview AS
SELECT
    t.ticket_ref,
    c.full_name        AS customer_name,
    c.email            AS customer_email,
    p.name             AS product_name,
    p.brand,
    p.category         AS product_category,
    a.full_name        AS assigned_agent,
    t.channel,
    t.category,
    t.priority,
    t.status,
    t.subject,
    t.created_at,
    t.resolved_at,
    CASE
        WHEN t.resolved_at IS NOT NULL
        THEN EXTRACT(EPOCH FROM (t.resolved_at - t.created_at)) / 3600
        ELSE NULL
    END                AS resolution_hours
FROM tickets t
JOIN customers c  ON t.customer_id = c.customer_id
JOIN products  p  ON t.product_id  = p.product_id
LEFT JOIN agents a ON t.agent_id   = a.agent_id;

-- Resolution summary with ratings
CREATE VIEW v_resolution_summary AS
SELECT
    t.ticket_ref,
    t.subject,
    p.name             AS product,
    r.resolution_summary,
    r.root_cause,
    r.action_taken,
    r.refund_issued,
    r.refund_amount,
    r.replacement_issued,
    r.customer_rating,
    a.full_name        AS resolved_by,
    r.resolved_at
FROM resolutions r
JOIN tickets  t ON r.ticket_id   = t.ticket_id
JOIN products p ON t.product_id  = p.product_id
JOIN agents   a ON r.resolved_by = a.agent_id;

-- Agent performance summary
CREATE VIEW v_agent_performance AS
SELECT
    a.full_name      AS agent,
    a.department,
    COUNT(t.ticket_id)                                           AS total_tickets,
    COUNT(r.resolution_id)                                       AS resolved_tickets,
    ROUND(AVG(r.customer_rating), 2)                             AS avg_rating,
    ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at)) / 3600), 1) AS avg_resolution_hours
FROM agents a
LEFT JOIN tickets     t ON t.agent_id      = a.agent_id
LEFT JOIN resolutions r ON r.ticket_id     = t.ticket_id
GROUP BY a.agent_id, a.full_name, a.department;