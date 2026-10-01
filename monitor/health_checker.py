import httpx
import time
from datetime import datetime

from database import (
    init_db,
    save_result,
    save_incident,
    get_connection
)


# =========================
# CONFIGURATION
# =========================

CHECK_INTERVAL = 30
DEGRADED_THRESHOLD = 2000


# =========================
# SERVICE MANAGEMENT
# =========================

def get_services():
    """
    Get all enabled services from the database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, url
        FROM services
        WHERE enabled = 1
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "name": row[0],
            "url": row[1]
        }
        for row in rows
    ]


# =========================
# PREVIOUS STATUS
# =========================

def get_previous_status(service_name):
    """
    Get the most recent status recorded
    for a service.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM health_checks
        WHERE service = ?
        ORDER BY id DESC
        LIMIT 1
    """, (service_name,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


# =========================
# HEALTH CHECK
# =========================

def check_service(service):

    start_time = time.perf_counter()

    try:

        response = httpx.get(
            service["url"],
            timeout=5
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        # Debug information
        print(
            f"{service['name']} | "
            f"HTTP {response.status_code} | "
            f"{response_time} ms"
        )

        # Determine service status
        if response.status_code >= 500:

            status = "down"

        elif response_time > DEGRADED_THRESHOLD:

            status = "degraded"

        elif response.status_code >= 400:

            status = "degraded"

        else:

            status = "healthy"

        return {
            "service": service["name"],
            "status": status,
            "http_status": response.status_code,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }

    except httpx.TimeoutException:

        return {
            "service": service["name"],
            "status": "down",
            "http_status": None,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "error": "Request timed out"
        }

    except httpx.RequestError as error:

        return {
            "service": service["name"],
            "status": "down",
            "http_status": None,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "error": str(error)
        }


# =========================
# CHECK ALL SERVICES
# =========================

def check_all_services():

    services = get_services()

    results = []

    for service in services:

        result = check_service(service)

        results.append(result)

    return results


# =========================
# DISPLAY RESULTS
# =========================

def display_results(results):

    print("\n" + "=" * 60)

    print("           CLOUDOPS MONITOR")

    print("=" * 60)

    print(
        f"Checked at: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print()

    for result in results:

        status_icon = {
            "healthy": "🟢",
            "degraded": "🟡",
            "down": "🔴"
        }.get(
            result["status"],
            "⚪"
        )

        latency = result["response_time_ms"]

        if latency is not None:

            latency_text = f"{latency} ms"

        else:

            latency_text = "N/A"

        print(
            f"{status_icon} "
            f"{result['service']:<20} "
            f"{result['status']:<10} "
            f"{latency_text}"
        )

    print("=" * 60)


# =========================
# MAIN MONITOR
# =========================

def monitor():

    # Make sure database tables exist
    init_db()

    print("CloudOps Monitor started.")

    print(
        f"Checking services every "
        f"{CHECK_INTERVAL} seconds."
    )

    print("Press CTRL+C to stop.")

    try:

        while True:

            # Check all enabled services
            results = check_all_services()

            # Process each result
            for result in results:

                # Get previous status
                previous_status = get_previous_status(
                    result["service"]
                )

                current_status = result["status"]

                # Detect status transition
                if (
                    previous_status is not None
                    and previous_status != current_status
                ):

                    save_incident(
                        result["service"],
                        previous_status,
                        current_status,
                        result["timestamp"]
                    )

                    print(
                        f"🚨 INCIDENT: "
                        f"{result['service']} "
                        f"{previous_status} → "
                        f"{current_status}"
                    )

                # Save health check
                save_result(result)

            # Display current monitoring status
            display_results(results)

            # Wait before next cycle
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:

        print("\nCloudOps Monitor stopped.")


# =========================
# APPLICATION ENTRY POINT
# =========================

if __name__ == "__main__":
    monitor()