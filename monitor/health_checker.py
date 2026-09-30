import httpx
import time
from datetime import datetime


SERVICES = [
    {
        "name": "Payment API",
        "url": "http://3.109.152.73:8000/health"
    },
    {
        "name": "Auth API",
        "url": "http://43.205.115.230:8000/health"
    },
    {
        "name": "Product API",
        "url": "http://localhost:8003/health"
    }
]

CHECK_INTERVAL = 30
DEGRADED_THRESHOLD = 3000


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


def check_all_services():

    results = []

    for service in SERVICES:
        result = check_service(service)
        results.append(result)

    return results


def display_results(results):

    print("\n" + "=" * 60)
    print("           CLOUDOPS MONITOR")
    print("=" * 60)

    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    for result in results:

        status_icon = {
            "healthy": "🟢",
            "degraded": "🟡",
            "down": "🔴"
        }.get(result["status"], "⚪")

        latency = result["response_time_ms"]

        if latency is not None:
            latency_text = f"{latency} ms"
        else:
            latency_text = "N/A"

        print(
            f"{status_icon} "
            f"{result['service']:<15} "
            f"{result['status']:<10} "
            f"{latency_text}"
        )

    print("=" * 60)


def monitor():

    print("CloudOps Monitor started.")
    print(f"Checking services every {CHECK_INTERVAL} seconds.")
    print("Press CTRL+C to stop.")

    try:

        while True:

            results = check_all_services()

            display_results(results)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:

        print("\nCloudOps Monitor stopped.")


if __name__ == "__main__":
    monitor()