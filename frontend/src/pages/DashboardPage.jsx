import React, { useEffect, useMemo, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, Area, AreaChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import api from '../services/api'
import StatCard from '../components/StatCard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import SeverityBadge from '../components/SeverityBadge'
import { getSeverityTone } from '../utils/severity'
import LoadingSkeleton from '../components/LoadingSkeleton'
import PageHeader from '../components/PageHeader'

function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [severityData, setSeverityData] = useState([])
  const [iocTypeData, setIocTypeData] = useState([])
  const [activityData, setActivityData] = useState([])
  const [sourceData, setSourceData] = useState([])
  const [threats, setThreats] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/dashboard/stats'),
      api.get('/dashboard/severity-distribution'),
      api.get('/dashboard/ioc-types'),
      api.get('/dashboard/activity'),
      api.get('/dashboard/sources'),
      api.get('/threats'),
    ]).then(([statsRes, severityRes, typeRes, activityRes, sourceRes, threatsRes]) => {
      setStats(statsRes.data)
      setSeverityData(severityRes.data)
      setIocTypeData(typeRes.data)
      setActivityData(activityRes.data)
      setSourceData(sourceRes.data)
      setThreats(threatsRes.data.slice(0, 8))
    }).finally(() => setLoading(false))
  }, [])

  const severityChart = useMemo(
    () => severityData.map((item) => ({ ...item, color: getSeverityTone(item.name) })),
    [severityData],
  )

  const chartAxisColor = '#6b7f98'
  const chartGridColor = '#d8e5f5'
  const chartBlue = '#2f80ed'
  const chartBlueSoft = 'rgba(47,128,237,0.16)'
  const chartTeal = '#1d9bf0'
  const chartViolet = '#6d8cff'

  return (
    <div className="page-stack">
      <PageHeader
        title={`Good ${new Date().getHours() < 12 ? 'Morning' : new Date().getHours() < 18 ? 'Afternoon' : 'Evening'}, analyst`}
        subtitle="Monitor and analyze your cybersecurity threat intelligence in one place."
      />

      {loading ? (
        <section className="stats-grid">
          <LoadingSkeleton className="stat-skeleton" lines={1} height={82} />
          <LoadingSkeleton className="stat-skeleton" lines={1} height={82} />
          <LoadingSkeleton className="stat-skeleton" lines={1} height={82} />
          <LoadingSkeleton className="stat-skeleton" lines={1} height={82} />
        </section>
      ) : null}

      <section className="stats-grid">
        <StatCard title="Total IOCs" value={stats ? stats.total_iocs.toLocaleString() : '...'} helper="Normalized indicators in the database" accent="#60a5fa" />
        <StatCard title="Critical Threats" value={stats ? stats.critical_threats.toLocaleString() : '...'} helper="Immediate attention required" accent="#ef4444" />
        <StatCard title="High Risk Threats" value={stats ? stats.high_risk_threats.toLocaleString() : '...'} helper="Elevated-risk indicators" accent="#fb923c" />
        <StatCard title="Active Alerts" value={stats ? stats.active_alerts.toLocaleString() : '...'} helper="Open detections requiring review" accent="#a78bfa" />
      </section>

      <section className="chart-grid">
        <ChartCard title="Threat Severity Distribution" subtitle="Low, medium, high, and critical breakdown">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={severityChart} dataKey="value" nameKey="name" innerRadius={72} outerRadius={110} paddingAngle={3}>
                {severityChart.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="IOC Type Distribution" subtitle="Threat indicators grouped by type">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={iocTypeData}>
              <CartesianGrid strokeDasharray="3 3" stroke={chartGridColor} />
              <XAxis dataKey="name" stroke={chartAxisColor} />
              <YAxis stroke={chartAxisColor} />
              <Tooltip />
              <Bar dataKey="value" radius={[8, 8, 0, 0]} fill={chartBlue} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Threat Activity Trend" subtitle="Recent IOC creation activity over time">
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={activityData}>
              <CartesianGrid strokeDasharray="3 3" stroke={chartGridColor} />
              <XAxis dataKey="date" stroke={chartAxisColor} />
              <YAxis stroke={chartAxisColor} />
              <Tooltip />
              <Area type="monotone" dataKey="value" stroke={chartTeal} fill={chartBlueSoft} strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Threat Sources" subtitle="IOC counts grouped by intelligence source">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sourceData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke={chartGridColor} />
              <XAxis type="number" stroke={chartAxisColor} />
              <YAxis dataKey="name" type="category" width={120} stroke={chartAxisColor} />
              <Tooltip />
              <Bar dataKey="value" radius={[0, 8, 8, 0]} fill={chartViolet} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h3>Recent Threats</h3>
            <p>Latest normalized IOC records from the seed dataset</p>
          </div>
        </div>

        <DataTable
          columns={[
            { key: 'ioc_value', label: 'IOC' },
            { key: 'ioc_type', label: 'Type' },
            { key: 'source', label: 'Source' },
            { key: 'risk_score', label: 'Risk Score', render: (row) => Math.round(row.risk_score) },
            { key: 'severity', label: 'Severity', render: (row) => <SeverityBadge severity={row.severity} /> },
            { key: 'last_seen', label: 'Last Seen', render: (row) => new Date(row.last_seen).toLocaleDateString() },
          ]}
          rows={threats}
          emptyMessage="Threat records are loading or unavailable."
          onRowClick={() => {}}
        />
      </section>
    </div>
  )
}

export default DashboardPage
