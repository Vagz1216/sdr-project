PRAGMA foreign_keys = ON;

-- Sample campaigns
INSERT OR IGNORE INTO campaigns (id, name, value_proposition, cta, status) VALUES
  (1, 'Outbound Outreach - Q2', 'Increase pipeline with our AI sales assistant', 'Book a quick demo', 'ACTIVE'),
  (2, 'Re-engagement', 'We have new features you might like', 'Learn more', 'PAUSED');

-- Sample leads
INSERT OR IGNORE INTO leads (id, email, name, status, email_opt_out, touch_count) VALUES
  (1, 'alice@example.com', 'Alice Johnson', 'NEW', 0, 0),
  (2, 'bob@example.com', 'Bob Smith', 'CONTACTED', 0, 1),
  (3, 'carol@example.com', 'Carol Chen', 'OPTED_OUT', 1, 0),
  (4, 'lawstands@gmail.com', 'Lawstands', 'NEW', 0, 0),
  (5, 'konnect1795@gmail.com', 'Konnect1795', 'NEW', 0, 0),
  (6, 'martinkam1216@gmail.com', 'Martinkam1216', 'NEW', 0, 0),
  (7, 'obogomaty@gmail.com', 'Obogomaty', 'NEW', 0, 0),
  (8, 'mayowasolomon@gmail.com', 'Mayowasolomon', 'NEW', 0, 0),
  (9, 'nurudeenh@gmail.com', 'Nurudeenh', 'NEW', 0, 0);

-- Link leads to campaign 1
INSERT OR IGNORE INTO campaign_leads (campaign_id, lead_id, emails_sent) VALUES
  (1,1,0),
  (1,2,1);
  -- link newly added leads to campaign 1
  INSERT OR IGNORE INTO campaign_leads (campaign_id, lead_id, emails_sent) VALUES
    (1,4,0),
    (1,5,0),
    (1,6,0),
    (1,7,0),
    (1,8,0),
    (1,9,0);

-- Sample staff
INSERT OR IGNORE INTO staff (id, name, email, timezone, availability) VALUES
  (1, 'Dana Sales', 'dana.sales@example.com', 'UTC', '{"monday": ["09:00-12:00","13:00-17:00"]}'),
  (2, 'Eli Rep', 'eli.rep@example.com', 'America/New_York', '{"tuesday": ["10:00-15:00"]}');
