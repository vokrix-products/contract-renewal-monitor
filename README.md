# Contract Renewal Monitor

Track vendor and subscription contract renewal dates. Upload PDFs, get alerts before deadlines.

## Archetype
extraction — buyer uploads contract PDFs, poller extracts dates, dashboard shows renewal status.

## What it does
- Buyer uploads vendor contract PDFs via the dashboard
- Poller extracts key dates (contract end, auto-renewal, notice deadline) using Claude Haiku
- Records table populated with status per vendor (expired/expiring_30/expiring_60/expiring_90/valid/missing)
- Dashboard shows upcoming expirations with severity coloring

## Poller input
- One or more PDF files uploaded to the jobs queue
- Vendor name derived from filename

## Poller output (records table)
- title: vendor name
- status: expired | expiring_30 | expiring_60 | expiring_90 | valid | missing | unknown
- details: jsonb with contract_end_date, auto_renewal_date, notice_deadline, contract_value, key_terms
- source_file_path: path in uploads bucket
- due_date: earliest critical date (notice_deadline > auto_renewal_date > contract_end_date)

## Env vars (Railway poller)
- SUPABASE_URL
- SUPABASE_SERVICE_KEY
- PRODUCT_ID=contract-renewal-monitor
- ANTHROPIC_API_KEY
