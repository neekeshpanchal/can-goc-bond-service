
### Local Kubernetes Deployment of a Bond Pricing API
Fully containerized API running in a local Kubernetes cluster, accessible externally, and ready for scaling—a hands-on exploration of the full deployment workflow.

* **Python API Development**

  * Built a bond pricing API (zero-coupon and coupon bonds) with Flask.
  * Tested API functionality with direct HTTP requests.

* **Containerization**

  * Created a Docker image using Gunicorn as the WSGI server.
  * Verified container runs independently.

* **Kubernetes Deployment (Minikube)**

  * Set up a local Minikube cluster.
  * Deployed API via a Deployment with multiple replicas.
  * Exposed pods internally using a ClusterIP Service.

* **Ingress and Routing**

  * Configured NGINX Ingress for external access (`can-gov-bonds.local`).
  * Updated hosts file for local DNS resolution.
  * Verified external API access through Ingress.

* **Scaling and High Availability**

  * Explored Horizontal Pod Autoscaler for CPU-based scaling.
  * Ensured multiple pods handle load for service availability.

* **Debugging and Validation**

  * Resolved service selector mismatches and networking issues.
  * Confirmed API accessibility via Ingress endpoint.

