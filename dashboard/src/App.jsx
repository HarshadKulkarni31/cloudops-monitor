import { useEffect, useState } from "react";
import {
  Activity,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Clock,
  Server,
  RefreshCw,
} from "lucide-react";

const API_URL = "http://localhost:8004";

function App() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchServices = async () => {
    try {
      const response = await fetch(`${API_URL}/services`);

      if (!response.ok) {
        throw new Error("Failed to fetch services");
      }

      const data = await response.json();

      setServices(data);
    } catch (error) {
      console.error("Monitoring API error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();

    const interval = setInterval(fetchServices, 10000);

    return () => clearInterval(interval);
  }, []);

  const healthy = services.filter(
    (service) => service.status === "healthy",
  ).length;

  const degraded = services.filter(
    (service) => service.status === "degraded",
  ).length;

  const down = services.filter((service) => service.status === "down").length;

  const getStatusIcon = (status) => {
    if (status === "healthy") {
      return <CheckCircle size={18} />;
    }

    if (status === "degraded") {
      return <AlertTriangle size={18} />;
    }

    return <XCircle size={18} />;
  };

  return (
    <div className="app">
      {/* Header */}

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

      {/* Overview */}

      <section className="overview">
        <div className="stat-card">
          <Server size={22} />
          <div>
            <span>Total Services</span>
            <strong>{services.length}</strong>
          </div>
        </div>

        <div className="stat-card healthy">
          <CheckCircle size={22} />
          <div>
            <span>Healthy</span>
            <strong>{healthy}</strong>
          </div>
        </div>

        <div className="stat-card degraded">
          <AlertTriangle size={22} />
          <div>
            <span>Degraded</span>
            <strong>{degraded}</strong>
          </div>
        </div>

        <div className="stat-card down">
          <XCircle size={22} />
          <div>
            <span>Down</span>
            <strong>{down}</strong>
          </div>
        </div>
      </section>

      {/* Services */}

      <section className="services-section">
        <div className="section-header">
          <div>
            <h2>Service Health</h2>
            <p>Real-time status of your cloud services</p>
          </div>

          <button onClick={fetchServices}>
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="loading">Loading monitoring data...</div>
        ) : services.length === 0 ? (
          <div className="empty-state">
            <Server size={40} />
            <h3>No monitoring data</h3>
            <p>Make sure the health checker is running.</p>
          </div>
        ) : (
          <div className="service-grid">
            {services.map((service) => (
              <div
                className={`service-card ${service.status}`}
                key={service.service}
              >
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

                  <div className={`status ${service.status}`}>
                    {getStatusIcon(service.status)}

                    <span>{service.status}</span>
                  </div>
                </div>

                <div className="metrics">
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

                  <div className="metric">
                    <Activity size={17} />

                    <div>
                      <span>HTTP Status</span>

                      <strong>{service.http_status ?? "N/A"}</strong>
                    </div>
                  </div>
                </div>

                <div className="last-check">
                  Last checked
                  <span>{service.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
