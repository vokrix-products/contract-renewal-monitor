import {
  ArrowDown,
  ArrowRight,
  ArrowUp,
  CheckCircle,
  AlertCircle,
  Timer,
  HelpCircle,
  CircleOff,
  Clock,
} from 'lucide-react'

export const labels = [
  {
    value: 'bug',
    label: 'Bug',
  },
  {
    value: 'feature',
    label: 'Feature',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
]

// Severity tiers drive badge color. Every status maps to exactly one tier:
//   critical -> red (destructive)   e.g. expired, denied, failed
//   warning  -> amber (warning)     e.g. expiring soon, needs review
//   good     -> green (success)     e.g. valid, approved, done
//   neutral  -> gray (secondary)    e.g. pending, queued, n/a
export type Severity = 'critical' | 'warning' | 'good' | 'neutral'

export const severityToBadgeVariant: Record<
  Severity,
  'destructive' | 'warning' | 'success' | 'secondary'
> = {
  critical: 'destructive',
  warning: 'warning',
  good: 'success',
  neutral: 'secondary',
}

// PRODUCT_CUSTOMIZE: replace this list with the real statuses this product
// produces (must match exactly what the backend poller writes to
// records.status). Every status must declare a severity tier above. Default
// values below are generic placeholders only — do not ship as-is.
export const statuses: {
  label: string
  value: string
  icon: typeof HelpCircle
  severity: Severity
}[] = [
  { label: 'Expired',        value: 'expired',     icon: AlertCircle, severity: 'critical' },
  { label: 'Expiring (30d)', value: 'expiring_30', icon: AlertCircle, severity: 'critical' },
  { label: 'Expiring (60d)', value: 'expiring_60', icon: Timer,       severity: 'warning'  },
  { label: 'Expiring (90d)', value: 'expiring_90', icon: Clock,       severity: 'warning'  },
  { label: 'Valid',          value: 'valid',        icon: CheckCircle, severity: 'good'     },
  { label: 'Missing',        value: 'missing',      icon: CircleOff,   severity: 'critical' },
  { label: 'Unknown',        value: 'unknown',      icon: HelpCircle,  severity: 'neutral'  },
]

export const priorities = [
  {
    label: 'Low',
    value: 'low' as const,
    icon: ArrowDown,
  },
  {
    label: 'Medium',
    value: 'medium' as const,
    icon: ArrowRight,
  },
  {
    label: 'High',
    value: 'high' as const,
    icon: ArrowUp,
  },
  {
    label: 'Critical',
    value: 'critical' as const,
    icon: AlertCircle,
  },
]
