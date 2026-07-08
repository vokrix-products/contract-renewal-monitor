import { useEffect, useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { Search } from '@/components/search'
import { ThemeSwitch } from '@/components/theme-switch'
import { JobsCard } from '@/features/jobs/components/jobs-card'
import { PRODUCT_ARCHETYPE } from '@/product-config'
import { ReportCard } from './components/report-card'
import { Overview } from './components/overview'
import { RecentActivity } from './components/recent-activity'
import { UpcomingExpirations } from './components/upcoming-expirations'
import { useDashboardStats } from './data/dashboard'
import { supabase } from '@/lib/supabase'

// PRODUCT_CUSTOMIZE: card titles/icons below describe generic record
// tracking. Rename "Records" / "Needs Attention" to match this product's
// domain (e.g. "Certificates" / "Expired").
export function Dashboard() {
  const { data, isLoading } = useDashboardStats()
  const [showUpgradeBanner, setShowUpgradeBanner] = useState(false)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    if (params.get('upgraded') === 'true') {
      setShowUpgradeBanner(true)
      // clean URL without reload
      window.history.replaceState({}, '', window.location.pathname)
    }
  }, [])

  async function handleRefreshSession() {
    await supabase.auth.refreshSession()
    window.location.reload()
  }

  return (
    <>
      {/* ===== Top Heading ===== */}
      <Header>
        <Search />
        <ThemeSwitch />
        <ProfileDropdown />
      </Header>

      {/* ===== Main ===== */}
      <Main>
        <div className='mb-2 flex items-center justify-between space-y-2'>
          <h1 className='text-2xl font-bold tracking-tight'>Dashboard</h1>
        </div>
        <div className='space-y-4'>
          {showUpgradeBanner && (
            <div className='flex items-center justify-between rounded-lg border border-green-500 bg-green-50 px-4 py-3 text-sm text-green-800 dark:bg-green-950 dark:text-green-200'>
              <span>
                🎉 Payment successful! Refresh your session to activate unlimited contracts.
              </span>
              <button
                className='ml-4 font-medium underline'
                onClick={handleRefreshSession}
              >
                Refresh now
              </button>
            </div>
          )}
          <JobsCard />
          {PRODUCT_ARCHETYPE === 'report' && <ReportCard />}
          <div className='grid gap-4 sm:grid-cols-3'>
            <Card>
              <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                <CardTitle className='text-sm font-medium'>
                  Total Records
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className='text-2xl font-bold'>
                  {isLoading ? '—' : (data?.total ?? 0)}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                <CardTitle className='text-sm font-medium'>
                  Needs Attention
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className='text-2xl font-bold'>
                  {isLoading ? '—' : (data?.needsAttention ?? 0)}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                <CardTitle className='text-sm font-medium'>
                  Added This Week
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className='text-2xl font-bold'>
                  {isLoading ? '—' : (data?.addedThisWeek ?? 0)}
                </div>
              </CardContent>
            </Card>
          </div>
          <div className='grid grid-cols-1 gap-4 lg:grid-cols-7'>
            <Card className='col-span-1 lg:col-span-4'>
              <CardHeader>
                <CardTitle>Status Breakdown</CardTitle>
              </CardHeader>
              <CardContent className='ps-2'>
                <Overview />
              </CardContent>
            </Card>
            <Card className='col-span-1 lg:col-span-3'>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest records added</CardDescription>
              </CardHeader>
              <CardContent>
                <RecentActivity />
              </CardContent>
            </Card>
          </div>
          {/* PRODUCT_CUSTOMIZE: remove this card for products where records
              have no expiration/renewal/deadline dates */}
          <Card>
            <CardHeader>
              <CardTitle>Upcoming Expirations</CardTitle>
              <CardDescription>Records expiring in the next 90 days</CardDescription>
            </CardHeader>
            <CardContent>
              <UpcomingExpirations />
            </CardContent>
          </Card>
        </div>
      </Main>
    </>
  )
}
