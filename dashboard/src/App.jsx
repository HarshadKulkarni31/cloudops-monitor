import { useCallback, useEffect, useState } from "react";
import {
  Activity,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Clock,
  Server,
  RefreshCw,
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const API_URL = "http://localhost:8004";

function App() {
  const [services, setServices] = useState([]);
  const [checks, setChecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uptime, setUptime] = useState([]);

  // Fetch monitoring data
  const fetchData = useCallback(async () => {
    try {
      const [servicesResponse, checksResponse, uptimeResponse] =
        await Promise.all([
          fetch(`${API_URL}/services`),
          fetch(`${API_URL}/checks?limit=60`),
          fetch(`${API_URL}/uptime`),
        ]);

      if (!servicesResponse.ok || !checksResponse.ok || !uptimeResponse.ok) {
        throw new Error("Failed to fetch monitoring data");
      }

      const servicesData = await servicesResponse.json();
      const checksData = await checksResponse.json();
      const uptimeData = await uptimeResponse.json();

      setServices(servicesData);
      setChecks(checksData);
      setUptime(uptimeData);
    } catch (error) {
      console.error("Monitoring API error:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial fetch + automatic refresh every 10 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchData();
    }, 0);

    const interval = setInterval(() => {
      fetchData();
    }, 10000);

    return () => {
      clearTimeout(timer);
      clearInterval(interval);
    };
  }, [fetchData]);

  // Service statistics
  const healthy = services.filter(
    (service) => service.status === "healthy",
  ).length;

  const degraded = services.filter(
    (service) => service.status === "degraded",
  ).length;

  const down = services.filter((service) => service.status === "down").length;

  // Status icons
  const getStatusIcon = (status) => {
    if (status === "healthy") {
      return <CheckCircle size={18} />;
    }

    if (status === "degraded") {
      return <AlertTriangle size={18} />;
    }

    return <XCircle size={18} />;
  };

  // Convert database records into chart data
  const chartData = [...checks].reverse().map((check) => ({
    time: new Date(check.timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }),

    service: check.service,

    latency:
      check.response_time_ms !== null ? Number(check.response_time_ms) : null,
  }));

  return (
    <div className="app">
      {/* ================= HEADER ================= */}

      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Activity size={24} />
          </div>

          <div>
            <h1>CloudOps Monitor</h1>
            <p>Cloud service observability platform</p>
          </div>
        </div>

        <div className="monitoring-status">
          <span className="live-dot"></span>
          Monitoring Active
        </div>
      </header>

      {/* ================= OVERVIEW ================= */}

      <section className="overview">
        {/* Total Services */}

        <div className="stat-card">
          <Server size={22} />

          <div>
            <span>Total Services</span>
            <strong>{services.length}</strong>
          </div>
        </div>

        {/* Healthy */}

        <div className="stat-card healthy">
          <CheckCircle size={22} />

          <div>
            <span>Healthy</span>
            <strong>{healthy}</strong>
          </div>
        </div>

        {/* Degraded */}

        <div className="stat-card degraded">
          <AlertTriangle size={22} />

          <div>
            <span>Degraded</span>
            <strong>{degraded}</strong>
          </div>
        </div>

        {/* Down */}

        <div className="stat-card down">
          <XCircle size={22} />

          <div>
            <span>Down</span>
            <strong>{down}</strong>
          </div>
        </div>
      </section>

      {/* ================= SERVICES ================= */}

      <section className="services-section">
        <div className="section-header">
          <div>
            <h2>Service Health</h2>
            <p>Real-time status of your cloud services</p>
          </div>

          {/* Manual Refresh */}

          <button onClick={fetchData}>
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {/* Loading */}

        {loading ? (
          <div className="loading">Loading monitoring data...</div>
        ) : services.length === 0 ? (
          /* Empty state */

          <div className="empty-state">
            <Server size={40} />

            <h3>No monitoring data</h3>

            <p>Make sure the health checker is running.</p>
          </div>
        ) : (
          /* Service Cards */

          <div className="service-grid">
            {services.map((service) => {
              const serviceUptime = uptime.find(
                (item) => item.service === service.service,
              );

              return (
                <div
                  className={`service-card ${service.status}`}
                  key={service.service}
                >
                  {/* Service Header */}

                  <div className="service-header">
                    <div className="service-title">
                      <div className="service-icon">
                        <Server size={20} />
                      </div>

                      <div>
                        <h3>{service.service}</h3>
                        <span>Microservice</span>
                      </div>
                    </div>

                    {/* Status */}

                    <div className={`status ${service.status}`}>
                      {getStatusIcon(service.status)}

                      <span>{service.status}</span>
                    </div>
                  </div>

                  {/* Metrics */}

                  <div className="metrics">
                    {/* Latency */}

                    <div className="metric">
                      <Clock size={17} />

                      <div>
                        <span>Latency</span>

                        <strong>
                          {service.response_time_ms !== null
                            ? `${service.response_time_ms} ms`
                            : "N/A"}
                        </strong>
                      </div>
                    </div>

                    {/* HTTP Status */}

                    <div className="metric">
                      <Activity size={17} />

                      <div>
                        <span>HTTP Status</span>

                        <strong>{service.http_status ?? "N/A"}</strong>
                      </div>
                    </div>
                  </div>

                  {/* Availability */}

                  <div className="uptime">
                    <div>
                      <span>Availability</span>

                      <strong>
                        {serviceUptime
                          ? `${serviceUptime.uptime_percentage}%`
                          : "0%"}
                      </strong>
                    </div>
                  </div>

                  {/* Last Check */}

                  <div className="last-check">
                    Last checked
                    <span>{service.timestamp}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* ================= LATENCY CHART ================= */}

      <section className="chart-section">
        <div className="section-header">
          <div>
            <h2>Response Latency</h2>

            <p>Historical response time across monitored services</p>
          </div>
        </div>

        <div className="chart-card">
          {checks.length === 0 ? (
            <div className="loading">Waiting for monitoring data...</div>
          ) : (
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

                <XAxis
                  dataKey="time"
                  stroke="#64748b"
                  tick={{ fontSize: 11 }}
                />

                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} unit=" ms" />

                <Tooltip
                  contentStyle={{
                    background: "#0f172a",
                    border: "1px solid #1e293b",
                    borderRadius: "8px",
                  }}
                />

                <Line
                  type="monotone"
                  dataKey="latency"
                  stroke="#60a5fa"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
}

export default App;
